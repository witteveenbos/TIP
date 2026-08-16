import json
from itertools import product
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from scipy import sparse
from shapely.prepared import prep

from constants import DATA_DIR

PROJECTED_CRS = "EPSG:28992"


def shapes_to_shapes(orig: gpd.GeoSeries, dest: gpd.GeoSeries) -> sparse.lil_matrix:
    """Calculate the fraction of each destination shape covered by source shapes."""
    orig_prepared = list(map(prep, orig))
    transfer = sparse.lil_matrix((len(dest), len(orig)), dtype=float)

    for destination_index, destination in enumerate(dest):
        destination_area = destination.area
        if destination_area == 0:
            continue

        for origin_index, origin in enumerate(orig_prepared):
            if origin.intersects(destination):
                overlap_area = orig.iloc[origin_index].intersection(destination).area
                transfer[destination_index, origin_index] = overlap_area / destination_area

    return transfer


def _load_inputs(
    municipalities_path: Path,
    substations_path: Path,
    capacity_path: Path,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    municipalities = gpd.read_file(municipalities_path)
    if "label" not in municipalities.columns and "index" in municipalities.columns:
        municipalities["label"] = municipalities["index"]
    substations = gpd.read_file(substations_path).to_crs(municipalities.crs)

    capacities = pd.DataFrame(json.loads(capacity_path.read_text())).T.rename(
        columns={
            "invoeding": "totaleCapaciteitInvoedingMva",
            "afname": "totaleCapaciteitAfnameMva",
        }
    )
    substations = substations.join(capacities, on="label")
    substations["station"] = substations["label"]

    missing_municipality_columns = {"identificatie", "geometry"} - set(municipalities.columns)
    if missing_municipality_columns:
        raise ValueError(f"Municipality data is missing columns: {sorted(missing_municipality_columns)}")

    required_station_columns = {
        "label",
        "station",
        "totaleCapaciteitInvoedingMva",
        "totaleCapaciteitAfnameMva",
        "geometry",
    }
    missing_station_columns = required_station_columns - set(substations.columns)
    if missing_station_columns:
        raise ValueError(f"Station data is missing columns: {sorted(missing_station_columns)}")

    return municipalities, substations


def _save_station_validation(
    municipalities: gpd.GeoDataFrame,
    substations: gpd.GeoDataFrame,
    station_to_municipality: dict[str, dict[str, float]],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    municipalities_projected = municipalities.to_crs(PROJECTED_CRS)
    substations_projected = substations.to_crs(PROJECTED_CRS)

    for station_name, relation_to_municipalities in station_to_municipality.items():
        this_station = substations_projected[substations_projected["station"] == station_name]
        ax = this_station.plot()
        for municipality_id, fraction in relation_to_municipalities.items():
            if fraction <= 0.01:
                continue

            this_municipality = municipalities_projected[municipalities_projected["identificatie"] == municipality_id]
            this_municipality.plot(
                ax=ax,
                color="red",
                alpha=0.5,
                linewidth=0.5,
                edgecolor="black",
            )
            centroid = this_municipality.geometry.centroid.iloc[0]
            ax.annotate(f"{fraction:.2f}", (centroid.x, centroid.y))

        ax.axis("off")
        ax.set_title(station_name)
        figure = ax.get_figure()
        figure.savefig(output_dir / f"{station_name}.png")
        plt.close(figure)


def pmiek_substation_mapper(
    municipalities_path: Path = DATA_DIR / "municipalities.geojson",
    substations_path: Path = DATA_DIR / "hsms.geojson",
    capacity_path: Path = DATA_DIR / "hsms_capacity.json",
    *,
    save_mapper: bool = False,
    visual_validation: bool = False,
    validation_dir: Path = Path("visual_checks/per_station"),
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Map substation capacities to municipalities by geometric overlap."""
    municipalities, substations = _load_inputs(
        Path(municipalities_path),
        Path(substations_path),
        Path(capacity_path),
    )
    substations = substations.clip(municipalities)
    if substations.empty:
        raise ValueError(
            "No substations overlap the municipality layer. "
            "Check that both files describe the same province and CRS."
        )

    municipalities_projected = municipalities.to_crs(PROJECTED_CRS)
    substations_projected = substations.to_crs(PROJECTED_CRS)
    transfer = shapes_to_shapes(
        municipalities_projected.geometry,
        substations_projected.geometry,
    )

    municipalities["invoeding"] = transfer.T.dot(substations["totaleCapaciteitInvoedingMva"].to_numpy())
    municipalities["afname"] = transfer.T.dot(substations["totaleCapaciteitAfnameMva"].to_numpy())

    transfer_matrix = shapes_to_shapes(
        substations_projected.geometry,
        municipalities_projected.geometry,
    ).toarray()
    municipality_to_station = {}
    for municipality_index, row in enumerate(transfer_matrix):
        municipality_id = municipalities.iloc[municipality_index]["identificatie"]
        municipality_to_station[municipality_id] = {
            station_id: float(value) for station_id, value in zip(substations["station"], row)
        }

    for municipality_id, station_fractions in municipality_to_station.items():
        if round(sum(station_fractions.values()), 1) > 1.0:
            raise ValueError(f"Station overlap fractions exceed 1 for municipality {municipality_id}")

    station_to_municipality = {}
    for municipality_id, station_fractions in municipality_to_station.items():
        for station_id, fraction in station_fractions.items():
            station_to_municipality.setdefault(station_id, {})[municipality_id] = fraction

    station_to_municipality = {
        station_id: municipality_fractions
        for station_id, municipality_fractions in station_to_municipality.items()
        if sum(municipality_fractions.values()) > 0.02
    }

    if visual_validation:
        _save_station_validation(
            municipalities,
            substations,
            station_to_municipality,
            Path(validation_dir),
        )

    if save_mapper:
        (DATA_DIR / "municipal_load_to_station_map.json").write_text(json.dumps(station_to_municipality))

    return municipalities, substations


if __name__ == "__main__":
    pmiek_substation_mapper(
        municipalities_path=DATA_DIR / "base_data/gemeenten_nh.geojson",
        save_mapper=True,
        visual_validation=True,
    )
