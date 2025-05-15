from __future__ import annotations
from abc import abstractmethod
from hail.models.calculate import GraphElement, GraphMeta, GraphResponse, NullReponse
from hail.result.base import AbstractResult
from typing import TYPE_CHECKING

from hail.context import ContextProvider
from hail.models.matrix import Matrix
from hail.util import id_to_region_map, region_to_id_map


if TYPE_CHECKING:
    from hail.reference import RefersTo
    from hail.context import ContextProvider

    Var = RefersTo | ContextProvider


class AbstractResultGraph(AbstractResult):
    @property
    @abstractmethod
    def graph(self, var: Var) -> list[GraphElement]:
        pass

    @property
    @abstractmethod
    def graph_aggregate(self, var: Var) -> list[GraphElement] | GraphElement:
        pass

    @property
    @abstractmethod
    def meta(self) -> GraphMeta:
        pass

    @classmethod
    def _make_metadata(cls) -> GraphMeta:
        exst_meta: GraphMeta = cls.meta
        return GraphMeta(
            title=cls.name if exst_meta.title == "default" else exst_meta.title,
            unit=cls.unit if exst_meta.unit == "default" else exst_meta.unit,
            **exst_meta.model_dump(exclude={"title", "unit"}),
        )

    @classmethod
    def make_graph(cls, context: ContextProvider) -> GraphResponse:
        region_to_id = region_to_id_map(request=context.request)

        if context.request.viewSettings.graphFocus is not None:
            filter_region = context.request.viewSettings.graphFocus.value
            filter_id = region_to_id[filter_region]
            graph_index = context.scenario_ids.index(filter_id)
            all_graphs: list[GraphElement] = cls.graph(var=context)
            filtered_graph = [ge.filter_on_index(graph_index) for ge in all_graphs]

            return GraphResponse(
                graphData=filtered_graph,
                metaData=cls._make_metadata(),
            )

        else:
            return NullReponse(
                msg="Graph focus not set in request (viewSettings.graphFocus). Cannot make (yet) make aggregate graph.",
                component="graph",
            )

    @classmethod
    def make_graph_toplevel(cls, context: ContextProvider) -> GraphResponse:
        """Make a top level graph, summing all graphs in the context"""
        # TODO: This is a temporary solution, we need to make a proper aggregate graph but that is currently out of scope
        all_graphs: list[GraphElement] = cls.graph(var=context)
        summed_graphs = [
            GraphElement(
                value=ge.value.sum_element_wise(),
                **ge.model_dump(exclude={"value"}),
            )
            for ge in all_graphs
        ]
        return GraphResponse(
            graphData=summed_graphs,
            metaData=cls._make_metadata(),
        )
