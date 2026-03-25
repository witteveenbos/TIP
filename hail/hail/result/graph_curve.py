from __future__ import annotations
from abc import abstractmethod
from hail.models.calculate import GraphMeta, GraphCurveElement, GraphCurveMeta, GraphCurveResponse, NullReponse
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

    # @classmethod
    # def _make_metadata(cls, gces: list[GraphCurveElement]) -> GraphCurveMeta:
    #     exst_meta: GraphCurveMeta = cls.meta

    #     properties = {}
    #     for gce in gces:
    #         properties[gce.name] = {"group": gce.group, "demandSupply": gce.demandSupply, "color": gce.color}

    #     x_tick_labels = hourly_datetime_labels()
        
    #     return GraphCurveMeta(
    #         title=cls.name if exst_meta.title == "default" else exst_meta.title,
    #         unit=cls.unit if exst_meta.unit == "default" else exst_meta.unit,
    #         properties=properties,
    #         xTickLabels=x_tick_labels,
    #         **exst_meta.model_dump(exclude={"title", "unit", "xTickLabels", "properties"}),
    #     )

    @staticmethod
    def _group_elements(gces: list[GraphCurveElement]) -> dict[str, list[GraphCurveElement]]:
        """Group elements by their group attribute"""
        groups = {}
        for gce in gces:
            group_name = gce.group
            if group_name not in groups:
                groups[group_name] = []
            groups[group_name].append(gce)
        return groups

    @staticmethod
    def transform_data_for_frontend(gces: list[GraphCurveElement], resample_hours: int = 1) -> list[dict[str, float | int]]:
        """Make a curve graph that can be parsed by Recharts with all curve graphs in the context and group them by group attribute.
        The hour within each resampled period with the highest total demand across all graph curve elements will be used as the 
        representative hour for that period, and its values will be used for all groups in that period.
        Demand values will be made negative to ensure they are displayed as negative in the frontend.
        
        Args:
            gces: List of GraphCurveElement objects
            resample_hours: Number of hours to aggregate data into (default: 1 for hourly data)
                           Can be 3, 6, 12, 24 or any arbitrary number of hours
        """
        groups = AbstractResultCurveGraph._group_elements(gces)
        
        # Get original hourly data length
        original_length = len(gces[0].value)
        
        # Calculate resampled length
        resampled_length = (original_length + resample_hours - 1) // resample_hours  # Ceiling division
        
        # Initialize the graph data structure
        graph_data = [{} for _ in range(resampled_length)]
        
        # Aggregate values for each group
        for resampled_index in range(resampled_length):
            # Calculate the range of original indices for this resampled period
            start_hour = resampled_index * resample_hours
            end_hour = min(start_hour + resample_hours, original_length)
            
            # Find the hour within this window with highest total demand across all gces
            max_total_demand = -float('inf')
            peak_hour_index = start_hour
            
            for hour_index in range(start_hour, end_hour):
                total_demand_this_hour = 0
                for gce in gces:
                    # Only consider demand elements for finding peak hour
                    if gce.demandSupply.lower() in ["demand", "vraag"]:
                        total_demand_this_hour += abs(gce.value[hour_index])
                
                if total_demand_this_hour > max_total_demand:
                    max_total_demand = total_demand_this_hour
                    peak_hour_index = hour_index
            
            # Use values from the peak demand hour for all groups
            for group_name, group_elements in groups.items():
                # Determine if this group represents demand (should be negative)
                representative_element = group_elements[0]
                is_demand = representative_element.demandSupply.lower() in ["demand", "vraag"]
                
                # Sum values for all elements in this group at the peak hour
                aggregated_value = 0
                for gce in group_elements:
                    value = gce.value[peak_hour_index]
                    # Make demand values negative
                    if is_demand:
                        value = -1*value
                    aggregated_value += value
                
                graph_data[resampled_index][group_name] = aggregated_value

        return graph_data

    @classmethod
    def _make_metadata(cls, gces: list[GraphCurveElement], resample_hours: int = 1) -> GraphCurveMeta:
        """Transform data for frontend and create metadata in a single operation to avoid redundancy
        
        Args:
            gces: List of GraphCurveElement objects
            resample_hours: Number of hours to aggregate data into (default: 1 for hourly data)
        """
        groups = cls._group_elements(gces)
        
        # Transform data for frontend
        graph_data = [{} for _ in range(len(gces[0].value))]
        for group_name, group_elements in groups.items():
            for i in range(len(gces[0].value)):
                aggregated_value = 0
                for gce in group_elements:
                    aggregated_value += gce.value[i]
                graph_data[i][group_name] = aggregated_value

        # Create metadata for groups
        exst_meta: GraphCurveMeta = cls.meta
        properties = {}
        for group_name, group_elements in groups.items():
            representative_element = group_elements[0]
            properties[group_name] = {
                "demandSupply": representative_element.demandSupply,
                "color": representative_element.color
            }

        # Generate appropriate x-axis labels based on resampling

        # Get original hourly data length and resampled length
        original_length = len(gces[0].value)
        resampled_length = (original_length + resample_hours - 1) // resample_hours  # Ceiling division

        if resample_hours == 1:
            x_tick_labels = hourly_datetime_labels()
        else:
            # Create labels for resampled intervals
            base_labels = hourly_datetime_labels()
            x_tick_labels = []
            for i in range(0, len(base_labels), resample_hours):
                if resample_hours == 24:
                    # For daily aggregation, show date only
                    x_tick_labels.append(base_labels[i].split(' ')[0])  # Extract date part
                else:
                    # For other intervals, show start time of interval
                    x_tick_labels.append(base_labels[i])
            
            # Ensure we don't exceed the resampled length
            x_tick_labels = x_tick_labels[:resampled_length]
        
        metadata = GraphCurveMeta(
            title=cls.name if exst_meta.title == "default" else exst_meta.title,
            unit=cls.unit if exst_meta.unit == "default" else exst_meta.unit,
            properties=properties,
            xTickLabels=x_tick_labels,
            **exst_meta.model_dump(exclude={"title", "unit", "xTickLabels", "properties"}),
        )

        return metadata

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

            graph_data = cls.transform_data_for_frontend(filtered_graph, resample_hours)
            graph_meta_data = cls._make_metadata(filtered_graph, resample_hours)

            response = GraphCurveResponse(
                graphData=graph_data,
                metaData=graph_meta_data,
            )

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


        graph_data = cls.transform_data_for_frontend(summed_graphs, resample_hours)
        graph_meta_data = cls._make_metadata(summed_graphs, resample_hours)
        
        response = GraphCurveResponse(
            graphData=graph_data,
            metaData=graph_meta_data,
        )

        return response
    