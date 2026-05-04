from __future__ import annotations
import logging
from abc import abstractmethod
from hail.models.calculate import GraphMeta, GraphCurveElement, GraphCurveMeta, GraphCurveResponse, NullReponse
from hail.result.base import AbstractResult
from typing import TYPE_CHECKING

from hail.context import ContextProvider
from hail.models.matrix import Matrix
from hail.util import id_to_region_map, region_to_id_map
import plotly.graph_objects as go
from hail.result.helpers import hourly_datetime_objects


if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class AbstractResultCurveGraph(AbstractResult):
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
            aggregated_value = None
            for gce in group_elements:
                if aggregated_value is None:
                    aggregated_value = gce.value
                else:
                    aggregated_value += gce.value
            
            representative_element = group_elements[0]
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
    def _make_plotly_graph(gces: list[GraphCurveElement]) -> go.Figure:
        """Make a plotly graph with datetime objects on the x-axis.
        Datetime objects are automatically serialized to ISO 8601 strings by fig.to_dict(),
        and the plotly React frontend understands them natively for proper date formatting.
        """
        fig = go.Figure()
        from hail.result.helpers import hourly_datetime_objects
        for gce in gces:
            fig.add_trace(go.Scatter(y=gce.value, mode='lines', line=dict(color=gce.color), name=gce.name, stackgroup='one' if gce.demandSupply.lower() == "aanbod" else 'two'))
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
            filtered_graph = [ge.filter_on_index(graph_index) for ge in all_graphs]

            # graph_data = cls.transform_data_for_frontend(filtered_graph, resample_hours)
            graph_meta_data = cls._make_metadata()
            grouped_data = cls._group_elements(filtered_graph)
            graph_data = cls._make_plotly_graph(grouped_data).to_dict()

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

    @classmethod
    def make_graph_toplevel(cls, context: ContextProvider, resample_hours: int = 24) -> GraphCurveResponse:
        """Make a top level (province) curve graph, summing all graph curve elements (municipalities) in the context
        
        Args:
            context: ContextProvider with scenario data
            resample_hours: Number of hours to aggregate data into (default: 1 for hourly data)
        """
        # TODO: This is a temporary solution, we need to make a proper aggregate graph but that is currently out of scope
        all_graphs: list[GraphCurveElement] = cls.graph(context)

        summed_graphs = []
        for gce in all_graphs:
            graph = GraphCurveElement(
                value=gce.value.sum_element_wise(),
                **gce.model_dump(exclude={"value"}),
            )
            summed_graphs.append(graph)

        logging.info(f"Summed graph curve elements for toplevel graph: {summed_graphs}")

        graph_data = cls.transform_data_for_frontend(summed_graphs, resample_hours)
        graph_meta_data = cls._make_metadata()
        
        response = GraphCurveResponse(
            graphData=graph_data,
            graphMeta=graph_meta_data,
        )
        logging.info(f"Returning curve toplevel response: {response}")

        return response
    