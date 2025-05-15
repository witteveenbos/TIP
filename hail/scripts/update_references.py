# %%
import logging
import requests
from hail.development import AbstractDevelopment
from hail.result import AbstractResultMap
from hail.result.graph import AbstractResultGraph
from hail.util import render_template
from hail.generate import import_all_classes_from_folder
from pathlib import Path
import argparse


def main():

    CONFIG = Path(__file__).parent.parent / "config"
    SCENARIO_ID = 1149070
    BASE_URL = "https://beta.engine.energytransitionmodel.com/api/v3"
    TO_DROP = ["1990_in_co2_emissions", "1990_in_co2_emissions_bunkers"]
    REFERENCE_LOCATION = Path(__file__).parent.parent / "hail" / "reference"

    parser = argparse.ArgumentParser(
        description="Update references in the project. Based on the ETM API and local configuration."
    )
    parser.add_argument(
        "--results",
        "-r",
        action="store_true",
        help="Use this flag to update (only) the results reference [used to determine what results are available]",
    )
    parser.add_argument(
        "--etm",
        "-e",
        action="store_true",
        help="Use this flag to update (only) the references to the ETM API [used for valid gqueries and input elements in configuration]",
    )
    parser.add_argument(
        "--devs",
        "-d",
        action="store_true",
        help="Use this flag to update (only) the developments reference [used for valid groups based on configuration]",
    )
    parser.add_argument(
        "--etm-scenario-id",
        type=int,
        help="Use this flag to update the scenarioID for the ETM API, default is 1149070",
        required=False,
    )

    args = parser.parse_args()

    if not any([args.results, args.etm, args.devs]):
        results = True
        etm = True
        devs = True
    else:
        results = args.results
        etm = args.etm
        devs = args.devs

    if args.etm_scenario_id:
        SCENARIO_ID = args.etm_scenario_id

    if etm:
        logging.info(f"▶️   Getting valid inputs and gqueries from ETM API...")
        gqueries = requests.get(url=BASE_URL + "/gqueries").json()
        inputs = requests.get(url=BASE_URL + f"/scenarios/{SCENARIO_ID}/inputs").json()

        logging.info(f"▶️   Dropping {TO_DROP} from gqueries...")
        gqueries_keys = [l["key"] for l in gqueries if l["key"] not in TO_DROP]
        inputs_keys = list(inputs.keys())

        logging.info(f"▶️   Getting UI valid inputs from config folder...")
        userinputs_keys = []
        for cls in import_all_classes_from_folder(CONFIG, AbstractDevelopment):
            cls: AbstractDevelopment
            userinputs_keys.append(cls.key)
        userinputs_keys = sorted(userinputs_keys)

        logging.info(f"▶️   Rendering template for etm.py...")
        template_fp = REFERENCE_LOCATION / "etm.py.jinja"
        rendered = render_template(
            template_fp,
            gqueries=gqueries_keys,
            inputs=inputs_keys,
            userinputs=userinputs_keys,
        )
        target = REFERENCE_LOCATION / "etm.py"
        with open(target, "w") as f:
            f.write(rendered)

        logging.info(f"🥳🥳  Success!  🥳🥳 Updated '{target}'.")

    if devs:

        logging.info(f"▶️   Getting UI valid inputs from config folder...")
        userinputs_keys = []
        for cls in import_all_classes_from_folder(CONFIG, AbstractDevelopment):
            cls: AbstractDevelopment
            userinputs_keys.append(cls.key)
        userinputs_keys = sorted(userinputs_keys)

        target = REFERENCE_LOCATION / "groupfields.py"
        template_fp = REFERENCE_LOCATION / "groupfields.py.jinja"
        rendered = render_template(
            template_fp,
            userinputs=userinputs_keys,
        )

        with open(target, "w") as f:
            f.write(rendered)

        logging.info(f"🥳🥳  Success!  🥳🥳 Updated '{target}'.")

    if results:
        ### MAPS ###
        logging.info(f"▶️   Getting map inputs from config folder...")
        valid_map_types = []
        for cls in import_all_classes_from_folder(CONFIG, AbstractResultMap):
            cls: AbstractResultMap
            cls.key
            valid_map_types.append(cls.key)

        valid_map_types = sorted(valid_map_types)
        maps = [(m.upper(), m) for m in valid_map_types]
        logging.info(f"▶️   Rendering template for maps.py...")
        template_fp = REFERENCE_LOCATION / "maps.py.jinja"
        rendered = render_template(
            template_fp,
            maps=maps,
        )
        target = REFERENCE_LOCATION / "maps.py"
        with open(target, "w") as f:
            f.write(rendered)

        logging.info(f"🥳🥳  Success!  🥳🥳 Updated '{target}'.")

        ### GRAPHS ###
        logging.info(f"▶️   Getting graph inputs from config folder...")
        valid_graph_types = []
        for cls in import_all_classes_from_folder(CONFIG, AbstractResultGraph):
            cls: AbstractResultGraph
            cls.key
            valid_graph_types.append(cls.key)
        valid_graph_types = sorted(valid_graph_types)
        graphs = [(g.upper(), g) for g in valid_graph_types]
        template_fp = REFERENCE_LOCATION / "graphs.py.jinja"
        rendered = render_template(
            template_fp,
            graphs=graphs,
        )
        target = REFERENCE_LOCATION / "graphs.py"
        with open(target, "w") as f:
            f.write(rendered)

        logging.info(f"🥳🥳  Success!  🥳🥳 Updated '{target}'.")


if __name__ == "__main__":
    main()
