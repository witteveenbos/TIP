from __future__ import annotations

import ast
from pathlib import Path
import logging
from hail.models.configuration import AccessedAttributes
from hail.models.fundamental import AttrDict
from hail.models.matrix import Matrix
from hail.models.request import PostUserInputRequest
from hail.util import id_to_region_map, region_to_id_map
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hail.context import ContextProvider

logger = logging.getLogger(__name__)


class AttributeAccessFinder(ast.NodeVisitor):

    def __init__(self, class_name):
        self.class_name = class_name
        self.accessed_attributes = AccessedAttributes()

    def visit_Attribute(self, node):
        # Recursively find the base of the attribute chain
        base = node
        while isinstance(base, ast.Attribute):
            base = base.value

        if isinstance(base, ast.Name) and base.id == self.class_name:
            self.add_to_visited(node)

        self.generic_visit(node)

    def add_to_visited(self, node):

        node_name = self._get_full_attr_name(node)

        try:
            for base in self.accessed_attributes.private_model_fields_names:
                if (
                    base.strip("_") in node_name.split(".")[1]
                ):  # Strip _ from the base because we check for _ui, _inputs, _gqueries
                    getattr(self.accessed_attributes, base).add(node_name.split(".")[2])
        except IndexError:
            # Skipping as we only care for second level attributes
            pass

    def _get_full_attr_name(self, node):
        # Recursively get the full attribute name
        if isinstance(node, ast.Attribute):
            return self._get_full_attr_name(node.value) + "." + node.attr
        elif isinstance(node, ast.Name):
            return node.id
        return ""


def find_accessed_attributes(file_path, class_name: str = "var") -> AccessedAttributes:
    with open(file_path, "r") as file:
        file_content = file.read()

    tree = ast.parse(file_content)
    finder = AttributeAccessFinder(class_name)
    finder.visit(tree)

    return finder.accessed_attributes


def find_all_accessed_attributes(config_folder: Path) -> AccessedAttributes:
    accessed_attributes = AccessedAttributes()
    for file in config_folder.glob("**/*.py"):
        accessed_attributes += find_accessed_attributes(file, "var")
    return accessed_attributes


def parse_user_input_to_data(context: ContextProvider) -> AttrDict[str, Matrix]:

    var = context
    request = context.request
    region_to_id = region_to_id_map(request)

    # init the parsed data with the right fields and matrix lengths
    parsed_ui_data = AttrDict({ui_key: var.Matrix(None) for ui_key in var._ui_fields})

    if request.userSettings.continuousDevelopments is not None:
        for dev in request.userSettings.continuousDevelopments:
            if dev.changes is None:
                continue

            # edits are bundled at the municipality level and group level
            this_scen_id = region_to_id[dev.municipalityID.value]

            for change in dev.changes:
                this_matrix = parsed_ui_data[change.devKey]
                pos_of_scen = var.scenario_ids.index(this_scen_id)
                this_matrix[pos_of_scen] = change.value

    if request.userSettings.sectoralDevelopments:
        for project in request.userSettings.sectoralDevelopments:
            if (project.changes is None) or (project.isDefault is True):
                continue

            this_scen_id = region_to_id[project.municipalityID.value]

            for project_el in project.changes:
                this_matrix = parsed_ui_data[project_el.devKey]
                pos_of_scen = var.scenario_ids.index(this_scen_id)

                # the only difference is that we sum over all projects
                try:
                    this_matrix[pos_of_scen] += project_el.value
                except TypeError:
                    # if this matrix pos is None, we initialize it with the value
                    this_matrix[pos_of_scen] = project_el.value

    return parsed_ui_data
