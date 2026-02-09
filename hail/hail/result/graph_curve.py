from __future__ import annotations
import logging
from abc import abstractmethod
from hail.models.calculate import GraphElement, GraphMeta, GraphCurveElement, GraphCurveMeta, GraphResponse, GraphCurveResponse, NullReponse
from hail.result.base import AbstractResult
from typing import TYPE_CHECKING
from hail.result.helpers import hourly_datetime_labels

from hail.context import ContextProvider
from hail.models.matrix import Matrix
from hail.util import id_to_region_map, region_to_id_map


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

    @classmethod
    def _make_metadata(cls, gces: list[GraphCurveElement]) -> GraphCurveMeta:
        exst_meta: GraphCurveMeta = cls.meta

        properties = {}
        for gce in gces:
            properties[gce.name] = {"group": gce.group, "demandSupply": gce.demandSupply, "color": gce.color}

        x_tick_labels = hourly_datetime_labels()
        
        return GraphCurveMeta(
            title=cls.name if exst_meta.title == "default" else exst_meta.title,
            unit=cls.unit if exst_meta.unit == "default" else exst_meta.unit,
            properties=properties,
            xTickLabels=x_tick_labels,
            **exst_meta.model_dump(exclude={"title", "unit", "xTickLabels", "properties"}),
        )

    @staticmethod
    def transform_data_for_frontend(gces: List[GraphCurveElement]) -> List[dict[str, float | int]]:
        """Make a curve graph that can be parsed by Recharts with all curve graphs in the context"""
        # TODO: write transformation and check how metadata can best be generated
        graph_data = [{} for _ in range(len(gces[0].value))]
        for gce in gces:
            for i, val in enumerate(gce.value):
                graph_data[i][gce.name] = val

        return graph_data

    @classmethod
    def make_graph(cls, context: ContextProvider) -> GraphCurveResponse:
        """Make a curve graph for a specific filtered municipality based on the graph focus in the context"""
        region_to_id = region_to_id_map(request=context.request)

        if context.request.viewSettings.graphFocus is not None:
            filter_region = context.request.viewSettings.graphFocus.value
            filter_id = region_to_id[filter_region]
            graph_index = context.scenario_ids.index(filter_id)
            all_graphs: list[GraphCurveElement] = cls.graph(var=context)
            filtered_graph = [ge.filter_on_index(graph_index) for ge in all_graphs]

            graph_data = cls.transform_data_for_frontend(filtered_graph)
            graph_meta_data = cls._make_metadata(filtered_graph)

            response = GraphCurveResponse(
                graphData=graph_data,
                metaData=graph_meta_data,
            )

            logging.info(f"Returning curve bottomlevel (municipality) response: {response}")

            return response

        else:
            return NullReponse(
                msg="Graph focus not set in request (viewSettings.graphFocus). Cannot make (yet) make aggregate graph.",
                component="graph",
            )

    @classmethod
    def make_graph_toplevel(cls, context: ContextProvider) -> GraphCurveResponse:
        """Make a top level (province) curve graph, summing all graph curve elements (municipalities) in the context"""
        # TODO: This is a temporary solution, we need to make a proper aggregate graph but that is currently out of scope
        all_graphs: list[GraphCurveElement] = cls.graph(var=context)

        summed_graphs = []
        for gce in all_graphs:
            graph = GraphCurveElement(
                value=gce.value.sum_element_wise(),
                **gce.model_dump(exclude={"value"}),
            )
            summed_graphs.append(graph)

        logging.info(f"Summed graph curve elements for toplevel graph: {summed_graphs}")

        graph_data = cls.transform_data_for_frontend(summed_graphs)
        graph_meta_data = cls._make_metadata(summed_graphs)
        
        response = GraphCurveResponse(
            graphData=graph_data,
            metaData=graph_meta_data,
        )
        logging.info(f"Returning curve toplevel response: {response}")

        return response
    