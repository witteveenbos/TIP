from __future__ import annotations
import logging
from abc import abstractmethod
from hail.models.calculate import GraphMeta, GraphCurveElement, GraphCurveMeta, GraphCurveResponse, NullReponse
from hail.result.base import AbstractResult
from typing import TYPE_CHECKING

from hail.context import ContextProvider
from hail.models.matrix import Matrix
from hail.models.curve import Curve
from hail.util import id_to_region_map, region_to_id_map
import plotly.graph_objects as go
from hail.result.helpers import hourly_datetime_objects


if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class AbstractResultCurveGraph(AbstractResult):
    _BASELOAD_ELECTRICITY_DEMAND_NAME = "Basislast elektriciteitsvraag"
    _LAST_GROUP_NAME = "Overige flexibiliteit"

    @property
    @abstractmethod
    def graph(self, var: Var) -> list[GraphCurveElement]:
        pass

    @property
    @abstractmethod
    def graph_aggregate(self, var: Var) -> list[GraphCurveElement] | GraphCurveElement:
        pass

    @property
    @abstractmethod
    def meta(self) -> GraphMeta:
        pass

    @staticmethod
    def _group_elements(gces: list[GraphCurveElement]) -> list[GraphCurveElement]:
        """Group elements by their group attribute and sum their values"""
        groups = {}
        for gce in gces:
            group_name = gce.group
            if group_name not in groups:
                groups[group_name] = []
            groups[group_name].append(gce)
        
        grouped_elements = []
        for group_name, group_elements in groups.items():
            aggregated_value = group_elements[0].value

            for gce in group_elements[1:]:

                    if isinstance(aggregated_value, Curve) and isinstance(gce.value, Curve):
                        aggregated_value = aggregated_value + gce.value
                    elif isinstance(aggregated_value, list) and isinstance(gce.value, list):
                        aggregated_value = [
                            (
                                left + right
                                if left is not None and right is not None
                                else left if left is not None else right
                            )
                            for left, right in zip(aggregated_value, gce.value)
                        ]
                    else:
                        raise TypeError("Expected grouped curve values to use matching list or Curve types")
            
            representative_element = group_elements[0]
            if AbstractResultCurveGraph._is_all_zero_values(aggregated_value):
                continue

            grouped_element = GraphCurveElement(
                name=group_name,
                group=representative_element.group,
                demandSupply=representative_element.demandSupply,
                color=representative_element.color,
                value=aggregated_value,
            )
            grouped_elements.append(grouped_element)
        
        return grouped_elements

    @staticmethod
    def _is_all_zero_values(values: list | Curve) -> bool:
        if isinstance(values, Curve):
            return all(AbstractResultCurveGraph._is_all_zero_values(row) for row in values)

        for value in values:
            if value is None:
                continue
            if value != 0:
                return False
        return True

    @staticmethod
    def _negative_values(values: list | Curve) -> list:
        return [(-value if value is not None else None) for value in values]

    @staticmethod
    def _split_storage_trace(gce: GraphCurveElement) -> list[GraphCurveElement]:
        """Split mixed-sign storage values into charge (vraag) and discharge (aanbod)."""
        discharging_values: list[float | int | None] = []
        charging_values: list[float | int | None] = []

        for value in gce.value:
            if value is None:
                discharging_values.append(None)
                charging_values.append(None)
                continue

            discharging_values.append(value if value > 0 else 0)
            charging_values.append(-value if value < 0 else 0)

        split_elements: list[GraphCurveElement] = []

        if not AbstractResultCurveGraph._is_all_zero_values(discharging_values):
            split_elements.append(
                GraphCurveElement(
                    name="Opslag (ontladen)",
                    group=gce.group,
                    demandSupply="Aanbod",
                    color=gce.color,
                    value=discharging_values,
                )
            )

        if not AbstractResultCurveGraph._is_all_zero_values(charging_values):
            split_elements.append(
                GraphCurveElement(
                    name="Opslag (laden)",
                    group=gce.group,
                    demandSupply="Vraag",
                    color=gce.color,
                    value=charging_values,
                )
            )

        return split_elements
    
    @staticmethod
    def _make_plotly_graph(gces: list[GraphCurveElement]) -> go.Figure:
        """Make a plotly graph with datetime objects on the x-axis.
        Datetime objects are automatically serialized to ISO 8601 strings by fig.to_dict(),
        and the plotly React frontend understands them natively for proper date formatting.
        """
        fig = go.Figure()
        from hail.result.helpers import hourly_datetime_objects

        expanded_gces: list[GraphCurveElement] = []
        for gce in gces:
            if gce.group == "Opslag" and isinstance(gce.value, list):
                expanded_gces.extend(AbstractResultCurveGraph._split_storage_trace(gce))
            else:
                expanded_gces.append(gce)

        aanbod_traces = [gce for gce in expanded_gces if gce.demandSupply.lower() == "aanbod"]
        vraag_traces = [gce for gce in expanded_gces if gce.demandSupply.lower() != "aanbod"]

        ordered_traces = aanbod_traces + vraag_traces
        ordered_traces = [ # plot last the "Overige flexibiliteit" group if it exists, so it appears on top in the graph (above the baseload demand)
            trace for trace in ordered_traces if trace.group != AbstractResultCurveGraph._LAST_GROUP_NAME
        ] + [
            trace for trace in ordered_traces if trace.group == AbstractResultCurveGraph._LAST_GROUP_NAME
        ]

        for gce in ordered_traces:
            stackgroup = 'one' if gce.demandSupply.lower() == "aanbod" else 'two'
            is_baseload_electricity_demand = gce.name == AbstractResultCurveGraph._BASELOAD_ELECTRICITY_DEMAND_NAME

            y_values = gce.value
            if stackgroup == 'two':
                y_values = AbstractResultCurveGraph._negative_values(gce.value)

            line = dict(color=gce.color)
            trace_kwargs = {
                "y": y_values,
                "mode": "lines",
                "line": line,
                "name": gce.name,
                "legendgroup": "Aanbod" if stackgroup == "one" else "Vraag",
                "legendgrouptitle": {"text": "Aanbod" if stackgroup == "one" else "Vraag"},
            }

            if is_baseload_electricity_demand:
                line["dash"] = "dot"
                trace_kwargs["fill"] = "none"
            else:
                trace_kwargs["stackgroup"] = stackgroup

            fig.add_trace(go.Scatter(**trace_kwargs)) # x-axis data is put in metadata to avoid redundant info on every trace to save data.
        return fig

    @classmethod
    def _make_metadata(cls) -> GraphCurveMeta:
        exst_meta: GraphMeta = cls.meta
        return GraphCurveMeta(
            title=cls.name if exst_meta.title == "default" else exst_meta.title,
            unit=cls.unit if exst_meta.unit == "default" else exst_meta.unit,
            xTickLabels=hourly_datetime_objects(),
            **exst_meta.model_dump(exclude={"title", "unit", "xTickLabels"}),
        )

    @classmethod
    def make_graph(cls, context: ContextProvider, resample_hours: int = 24) -> GraphCurveResponse:
        """Make a curve graph for a specific filtered municipality based on the graph focus in the context
        
        Args:
            context: ContextProvider with scenario data
            resample_hours: Number of hours to aggregate data into (default: 1 for hourly data)
        """
        region_to_id = region_to_id_map(request=context.request)

        if context.request.viewSettings.graphFocus is not None:
            filter_region = context.request.viewSettings.graphFocus.value
            filter_id = region_to_id[filter_region]
            graph_index = context.scenario_ids.index(filter_id)
            all_graphs: list[GraphCurveElement] = cls.graph(context)
            grouped_graph = cls._group_elements(all_graphs)
            filtered_graph = [ge.filter_on_index(graph_index) for ge in grouped_graph]

            # graph_data = cls.transform_data_for_frontend(filtered_graph, resample_hours)
            graph_meta_data = cls._make_metadata()
            graph_data = cls._make_plotly_graph(filtered_graph).to_dict()

            response = GraphCurveResponse(
                graphData=graph_data,
                graphMeta=graph_meta_data,
            )

            logging.info(f"Returning curve bottomlevel (municipality) response: {response}")

            return response

        else:
            return NullReponse(
                msg="Graph focus not set in request (viewSettings.graphFocus). Cannot make (yet) make aggregate graph.",
                component="graph",
            )
