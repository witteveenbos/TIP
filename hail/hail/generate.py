from typing import TYPE_CHECKING, Literal, Optional
from hail.development import AbstractDevelopment
from hail.models.fundamental import Value
from hail.models.calculate import (
    ETMSetter,
    GraphResponse,
    DevelopmentGroup,
    InputResponse,
    MapResponse,
    NullReponse,
)
from hail.models.configuration import ETMScenario
from hail.models.enums import AreaDivisionEnum, DevelomentType
from hail.context import ContextProvider
from hail.models.request import PostUserInputRequest
from hail.util import merge_developments, id_to_region_map


import importlib
import inspect
from pathlib import Path
import sys
import logging


## TODO: Move these functions to a seperate module with util, developments, maps, graphs etc. (refactor)


def import_all_classes_from_folder(
    folder_path: Path, class_or_tuple: tuple[type] | type
) -> list[type]:
    # Add the folder path to the system path
    sys.path.append(str(folder_path.resolve()))

    if class_or_tuple is not tuple:
        class_tuple = (class_or_tuple,)

    classes = []
    for file in folder_path.rglob("*.py"):
        EXCLUDED_FILES = ["__init__.py", "_groups.py", "shared.py"]
        if file.name in EXCLUDED_FILES or file.parent.name == "util":
            # Skipping {file.name}, because shouldn't contain {class_or_tuple}"
            continue

        # Convert file path to module path
        module_path = file.with_suffix("").relative_to(folder_path)
        module_name = ".".join(module_path.parts)

        try:
            module = importlib.import_module(module_name)
            for _, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, class_tuple)
                    and not any([obj is cls for cls in class_tuple])
                ):
                    logging.debug(f"Processing {file.name}")
                    classes.append(obj)
        except ModuleNotFoundError as e:
            logging.error(f"Module not found: {e}")
        except Exception as e:
            logging.error(f"Error importing {module_name}: {e}")

    return classes


def union_and_unpack(
    list_of_setters: list[Optional[ETMSetter]],
) -> dict[str, Value] | None:
    result = {}
    for setter in list_of_setters:
        if isinstance(setter, ETMSetter):
            result.update({setter.key: setter.value})

    if not result:
        return None
    return result


def combine_setters_by_scenario(
    all_etm_setters: list[list[Optional[ETMSetter]]],
    scenario_ids: list[int],
    request: PostUserInputRequest,
) -> list[ETMScenario]:
    scenario_wise = list(zip(*all_etm_setters))

    all_scenarios = []
    for scenario_id, scenario_setters in zip(scenario_ids, scenario_wise):
        scenario = ETMScenario(
            name=id_to_region_map(request=request)[scenario_id],
            etm_id=scenario_id,
            user_values=union_and_unpack(scenario_setters),
            selectedScenario=request.userSettings.selectedScenario,
        )
        all_scenarios.append(scenario)

    return all_scenarios


def compute_all_etm_setters(context: ContextProvider) -> list[ETMScenario]:
    classes = context.preloaded.developmentclasses
    # first make sure we have all the members assigned to the groups
    context.set_groups(classes)

    # get all ETM setters for all classes and stack them vertically over all developments
    # scenarios are columns, setters are rows
    all_etm_setters = []
    for cls in classes:
        try:
            if TYPE_CHECKING:
                cls: AbstractDevelopment
            this_etm_setters = cls.determine_etm_setters(context)
        except NotImplementedError:
            logging.error(f"ETM setters not implemented for {cls}. Skipping.")
            continue
        all_etm_setters.extend(this_etm_setters)

    return combine_setters_by_scenario(
        all_etm_setters=all_etm_setters,
        scenario_ids=context.scenario_ids,
        request=context.request,
    )


async def compute_map_response(context: ContextProvider) -> MapResponse:

    map_response = None
    logging.debug("Computing map response")
    vs = context.request.viewSettings
    maps = context.preloaded.mapclasses
    method = (
        "make_map" if vs.areaDivision == AreaDivisionEnum.GM else "make_map_aggregate"
    )
    e_msg = None

    for mapoption in maps:
        right_balance = mapoption.related_balance == vs.balance
        right_carrier = mapoption.related_carrier == vs.energyCarrier
        matches_area_div = (
            mapoption.related_area_div == vs.areaDivision  # match single value
            or mapoption.related_area_div is None  # not specified is a match
        )

        # match list
        if isinstance(mapoption.related_area_div, list):
            matches_area_div = (
                vs.areaDivision in mapoption.related_area_div
            ) or matches_area_div
        if right_balance and right_carrier and matches_area_div:
            # try:
            map_response = getattr(mapoption, method)(context)
            # except Exception as e:
            # e_msg = f"Error computing map '{mapoption.key}' response for {vs.balance.value}, {vs.energyCarrier.value}, {vs.areaDivision.value}: {e}"
            # we log the error later

    if map_response is None:
        msg = f"MapResponse not found for '{vs.balance.value}', '{vs.energyCarrier.value}' and '{vs.areaDivision.value}'. Returning None."
        if e_msg:
            msg = e_msg
        logging.error(msg)
        map_response = NullReponse(msg=msg, component="map")

    return map_response


async def compute_graph_response(context: ContextProvider) -> GraphResponse:

    graph_response = None
    logging.debug("Computing graph response")
    vs = context.request.viewSettings
    graphs = context.preloaded.graphclasses

    if vs.graphType is None:
        return NullReponse(msg="GraphType is None. Returning None.", component="graph")

    method = (
        "make_graph"
        if vs.areaDivision == AreaDivisionEnum.GM
        else "make_graph_aggregate"
    )

    e_msg = None
    for graphoption in graphs:
        if vs.graphType.value == graphoption.key:
            try:
                graph_response = getattr(graphoption, method)(context)
            except Exception as e:
                e_msg = f"Error computing graph '{graphoption.key}'. Error: {e.with_traceback(None)}"
                # we log the error later

    if graph_response is None:
        msg = f"GraphReponse not found for '{vs.graphType}'. Returning None."
        if e_msg:
            msg = e_msg
        logging.error(msg)
        graph_response = NullReponse(msg=msg, component="graph")

    return graph_response


async def compute_response_post_update(context: ContextProvider) -> tuple[
    InputResponse | None,
    MapResponse | None,
    GraphResponse | None,
    list[NullReponse] | None,
]:
    # TODO: change the name of this variable to develompent fields (inputs are confusing with ETM inputs)
    input_response = await compute_development_response(context)
    map_response = await compute_map_response(context)
    graph_response = await compute_graph_response(context)

    results = [input_response, map_response, graph_response]

    msgs = []
    for i, result in enumerate(results):
        if isinstance(result, NullReponse):
            msgs.append(result)
            results[i] = None

    if not msgs:
        msgs = None

    return *results, msgs


async def compute_development_response(context: ContextProvider) -> InputResponse:

    # if the area division is GM, we do not need to aggregate the input response (we use the pre-updated values)
    # this state is stored in the frontend and represents user input values on developments, so we could actually

    logging.debug("Computing development response")
    vs = context.request.viewSettings

    method = (
        "make_developments"
        if vs.areaDivision == AreaDivisionEnum.GM
        else "make_developments_aggregate"
    )
    if vs.areaDivision == AreaDivisionEnum.HSMS:
        return NullReponse(
            msg="AreaDivision is HSMS. Development response is possible at this level yet.",
            component="developments",
        )

    dev_response = None
    msg = None
    # try:
    dev_response = compute_all_developments(
        method=method,
        context=context,
    )
    # except Exception as e:
    # msg = f"Error computing devs. Error: {e.with_traceback(None)}"

    if dev_response is None:
        dev_response = NullReponse(msg=msg, component="developments")
        logging.error(msg)

    return dev_response


def compute_all_developments(
    method: Literal["make_developments", "make_developments_aggregate"],
    context: ContextProvider,
) -> dict[str, list[DevelopmentGroup]]:

    dev_type = context.request.viewSettings.developmentType
    classes = context.preloaded.developmentclasses

    all_inputs_computed = None
    for cls in classes:
        if cls.dev_type == dev_type or dev_type is None:
            this_input_computed = getattr(cls, method)(context)
            if all_inputs_computed is None:
                all_inputs_computed = this_input_computed
            else:
                all_inputs_computed = merge_developments(
                    all_inputs_computed, this_input_computed
                )
    return all_inputs_computed


def compute_single_file_slider_values(filepath: Path, context: ContextProvider) -> dict:

    # Add the folder path to the system path
    sys.path.append(str(filepath.parent.resolve()))

    module_name = ".".join(
        [filepath.parents[1].stem, filepath.parents[0].stem, filepath.stem]
    )

    try:
        module = importlib.import_module(module_name)

        for _, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, AbstractDevelopment)
                and obj is not AbstractDevelopment
            ):
                return getattr(obj, "compute_slider_values")(context)

    except ModuleNotFoundError as e:
        logging.warning(f"Module not found: {e}")
    except Exception as e:
        logging.error(f"Error importing {module_name}: {e}")
