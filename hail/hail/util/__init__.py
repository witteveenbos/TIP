from __future__ import annotations
import typing
import logging
import yaml
import os
import colorcet as cc
from pathlib import Path
from jinja2 import Template, Environment, meta

if typing.TYPE_CHECKING:
    from hail.models.request import PostUserInputRequest
    from hail.models.calculate import DevelopmentGroup


def load_yaml(f: Path) -> dict:
    """Load a YAML file and return a dictionary using the custom Loader."""

    class Loader(yaml.SafeLoader):
        """Custom YAML loader that supports the !include tag."""

        def __init__(self, stream):

            self._root = os.path.split(stream.name)[0]

            super(Loader, self).__init__(stream)

        def include(self, node):

            filename = os.path.join(self._root, self.construct_scalar(node))

            with open(filename, "r") as f:
                return yaml.load(f, Loader)

    Loader.add_constructor("!include", Loader.include)
    with open(f, "r") as f:
        return yaml.load(f, Loader)


def filter_dict(d: dict, keys: list[str]) -> dict:
    """Filter a dictionary by a list of keys."""
    return {key: d[key] for key in keys if key in d}


def open_template(fp: Path) -> Template:
    with open(fp) as file_:
        return Template(file_.read())


def get_template_variables(fp: Path) -> set[str]:
    env = Environment()
    with open(fp) as file_:
        return meta.find_undeclared_variables(env.parse(file_.read()))


def render_template(fp: Path, **args) -> str:
    t = open_template(fp)
    return t.render(**args)


def merge_developments(
    one_dict: dict[str, list[DevelopmentGroup]],
    other_dict: dict[str, list[DevelopmentGroup]],
):
    merged_dict = {}

    # first we find the first level keys (AreaDivisionIDs)
    all_keys = set(one_dict.keys()) | set(other_dict.keys())

    def merge_development_groups(
        groups: list[DevelopmentGroup],
    ) -> list[DevelopmentGroup]:
        merged_groups = {}
        for group in groups:
            if group in merged_groups:
                merged_groups[group].inputs += group.inputs
            else:
                merged_groups[group] = group

        return list(merged_groups.values())

    for key in all_keys:
        if key in one_dict and key in other_dict:
            merged_dict[key] = merge_development_groups(one_dict[key] + other_dict[key])
        elif key in one_dict:
            merged_dict[key] = one_dict[key]
        elif key in other_dict:
            merged_dict[key] = other_dict[key]

    return merged_dict


def id_to_region_map(
    request: PostUserInputRequest,
) -> dict[int, str]:
    return _create_id_to_region_map(request)


def region_to_id_map(
    request: PostUserInputRequest,
) -> dict[str, int]:
    return _create_id_to_region_map(request, inverse=True)


def _create_id_to_region_map(
    request: PostUserInputRequest, inverse=False
) -> dict[int, str]:

    id_to_region = {
        ms.ETMscenarioID: ms.municipalityID.value
        for ms in request.userSettings.municipalityScenarios
    }
    if inverse:
        return {v: k for k, v in id_to_region.items()}

    return id_to_region


def normalize(value, vmin, vmax):
    if vmin == vmax:
        return int(255 / 2)
    return int((value - vmin) / (vmax - vmin) * 255)


def get_color(
    value,
    cmap_name="b_diverging_protanopic_deuteranopic_bwy_60_95_c32",
    vmin=0,
    vmax=100,
):
    if value is None:
        logging.debug("[colormap]: Value is None, returning white")
        return "#ffffff"

    if value < vmin:
        logging.debug(
            f"[colormap]: Value {value:.2f} is smaller than vmin {vmin} for colormap {cmap_name}"
        )
        value = vmin
    if value > vmax:
        logging.debug(
            f"[colormap]: Value {value:.2f} is larger than vmax {vmax} for colormap {cmap_name}"
        )
        value = vmax

    norm_value = normalize(value, vmin, vmax)
    cmap = getattr(cc, cmap_name)
    color = cmap[norm_value]

    return color


def linspace(start, stop, num=50, decimals=2):
    if num < 2:
        raise ValueError("num must be greater than 1")
    step = (stop - start) / (num - 1)
    ls = [round(start + step * i, decimals) for i in range(num)]
    if decimals == 0:
        return [int(i) for i in ls]
    return ls
