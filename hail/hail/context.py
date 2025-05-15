from __future__ import annotations
from pydantic import BaseModel
from typing import Any, Optional
from hail.models.fundamental import AttrDict, FilterList
from hail.models.response import QueryResult, InputResult, APIResponse
from typing import TYPE_CHECKING
from hail.models.matrix import Matrix, clamp_el_wise
from hail.models.request import PostUserInputRequest
from hail.parse import parse_user_input_to_data
from hail.reference.groupfields import GroupFields, Value

if TYPE_CHECKING:
    from hail.development import AbstractDevelopment, Group
    from hail.models.state import PreloadedState
    from hail.models.configuration import AggregationConfig


class MultiScenarioData(BaseModel):
    scenario_ids: list[int]
    gqueries: dict[str, list[QueryResult]]
    inputs: dict[str, list[InputResult]]
    ui: dict[str, list[Value]]
    inputs_primitive: Optional[dict[str, list[InputResult]]] = None

    def model_post_init(self, __context: Any) -> None:
        # Convert dictionaries to into AttrDicts
        # Convert lists into FilterLists
        self.gqueries = AttrDict(
            {key: FilterList(value) for key, value in self.gqueries.items()}
        )

        # store the original inputs to use for inserting the original inputs
        self.inputs_primitive = self.inputs
        self.inputs = AttrDict(
            {key: FilterList(value, etm_key=key) for key, value in self.inputs.items()}
        )
        # we don't have nesting in ui, so we can just convert it to a matrix directly
        self.ui = AttrDict({key: Matrix(value) for key, value in self.ui.items()})

    def overwrite_ui_to_none(self) -> None:
        self.ui = AttrDict({key: None for key in self.ui.keys()})

    def insert_inputs_from_original(self, other: MultiScenarioData) -> None:

        # insert the original user values from the initial by updating the InputResult objects
        for key, list_of_inputs in self.inputs_primitive.items():
            for i, input_result in enumerate(list_of_inputs):
                input_result.user_from_initial_context = other.inputs_primitive[key][
                    i
                ].user

        # convert the new inputs objects to FilterLists as needed (unsure if this is necessary due to pointing)
        self.inputs = AttrDict(
            {
                key: FilterList(value, etm_key=key)
                for key, value in self.inputs_primitive.items()
            }
        )


class ContextProvider:

    def __init__(
        self, data: MultiScenarioData, _ui_fields: list[str] = None
    ):  # TODO: can data really be None?
        if data is None:
            data = MultiScenarioData(
                scenario_ids=[],
                gqueries={},
                inputs={},
                ui={},
            )
        self.data = data

        self._ui_fields = _ui_fields
        self._groups = None
        self._ordered_share_matrices = {}

    def update(self, data: MultiScenarioData) -> None:
        """Updates the data in the context"""
        self.data = data

    def add_request(self, request: PostUserInputRequest) -> None:
        """Add the request to the context, triggering the parsing of the user input"""
        self._request = request
        self.set_user_input(context=self)

    def add_preloaded(self, preloaded: Any) -> None:
        """Add the preloaded data to the context"""
        self._preloaded = preloaded

    def add_original_context(self, original_context: ContextProvider) -> None:
        """Inserts the original context into the current context"""
        self.data.insert_inputs_from_original(original_context.data)

    def disable_ui_propagation(self) -> None:
        """Disables the propagation of user input data by overwriting all its matrices with None-values"""
        self.data.overwrite_ui_to_none()

    @property
    def preloaded(self) -> PreloadedState:
        """Returns the preloaded data"""
        try:
            return self._preloaded
        except AttributeError:
            raise AttributeError(
                "No preloaded data has been set. Please set preloaded data (.add_preloaded) before trying to access it."
            )

    @property
    def ordered_share_matrices(self) -> Matrix:
        return self._ordered_share_matrices

    @property
    def aggregator(self) -> AggregationConfig:
        """Returns the aggregation config that matches the area division of the request"""
        for cls in self.preloaded.aggregation_configs:
            if cls.area_division == self.request.viewSettings.areaDivision:
                return cls

    @property
    def request(self) -> PostUserInputRequest:
        """Returns the request"""
        try:
            return self._request
        except AttributeError:
            raise AttributeError(
                "No request has been set. Please set request (.add_request) before trying to access it."
            )

    def set_user_input(self, context: ContextProvider) -> None:
        """Parses the user input from the request and sets it in the context"""
        self.data.ui = parse_user_input_to_data(context)

    def set_groups(self, classes: list[AbstractDevelopment]) -> None:
        """Sets the groups in the context"""
        # get all unique groups
        groups = set([cls.group for cls in classes if cls.group is not None])
        self._groups = AttrDict({group.key: group for group in groups})

        # add the context to all groups
        for group in self._groups.values():
            group: Group = group
            group.add_context(self)

        # add all members to their respective groups
        for cls in classes:
            if cls.group is not None:
                this_group: Group = self._groups[cls.group.key]
                this_group._add_member(cls)

    @property
    def groups(self) -> GroupFields:
        try:
            return self._groups
        except AttributeError:
            raise AttributeError(
                "No groups have been set. Please set groups (.set_groups) before trying to access them."
            )

    @property
    def scenario_ids(self) -> list[int]:
        """Returns a list of scenario ids"""
        return self.data.scenario_ids

    @property
    def gqueries(self) -> AttrDict[str, FilterList["QueryResult"]]:
        """Returns the gqueries objects as defined in the ETM"""
        return self.data.gqueries

    @property
    def inputs(self) -> AttrDict[str, FilterList["InputResult"]]:
        """Returns the input objects as defined in the ETM"""
        return self.data.inputs

    @property
    def ui(self) -> AttrDict[str, Matrix]:
        """Returns the user input data, from the pMIEK tool request"""
        return self.data.ui

    def Matrix(self, value: float | int | None) -> Matrix[float | int]:
        """Returns a matrix with the same length as the scenario_ids, filled with the given value"""
        if not isinstance(value, (int, float, None)):
            raise TypeError(
                f"Value must be an int or float, got {type(value)} instead."
            )
        return Matrix([value for _ in range(len(self.scenario_ids))])

    @staticmethod
    def min(one: Matrix | float | int, other: Matrix | float | int) -> Matrix:
        """
        Performs element-wise minimum comparison between two matrices or a matrix and a scalar.

        For each position, returns the smaller value between the corresponding elements.
        If comparing with a scalar, returns the smaller value between each matrix element
        and the scalar. None values in the matrix are preserved as None.

        Args:
            other (Matrix or float/int): Second operand for comparison. Can be either
                another Matrix instance or a numeric scalar value.

        Returns:
            Matrix: A new Matrix instance containing element-wise minimums.

        Raises:
            ValueError: If neither operand is a Matrix instance.

        Example:
            >>> m1 = Matrix([1, 2, 3])
            >>> m2 = Matrix([2, 1, 4])
            >>> m1.min_el_wise(m2).data
            [1, 1, 3]

            >>> m1.min_el_wise(2).data
            [1, 2, 2]
        """
        return clamp_el_wise(min, one, other)

    @staticmethod
    def max(one: Matrix | float | int, other: Matrix | float | int) -> Matrix:
        """
        Performs element-wise maximum comparison between two matrices or a matrix and a scalar.

        For each position, returns the larger value between the corresponding elements.
        If comparing with a scalar, returns the larger value between each matrix element
        and the scalar. None values in the matrix are preserved as None.

        Args:
            other (Matrix or float/int): Second operand for comparison. Can be either
                another Matrix instance or a numeric scalar value.

        Returns:
            Matrix: A new Matrix instance containing element-wise maximums.

        Raises:
            ValueError: If neither operand is a Matrix instance.

        Example:
            >>> m1 = Matrix([1, 2, 3])
            >>> m2 = Matrix([2, 1, 4])
            >>> m1.max_el_wise(m2).data
            [2, 2, 4]

            >>> m1.max_el_wise(2).data
            [2, 2, 3]
        """
        return clamp_el_wise(max, one, other)

    @classmethod
    def from_response(
        cls, response: list["APIResponse"], accessed_attributes_ui: list[str]
    ) -> "ContextProvider":
        """Creates a context from a list of APIResponses"""
        return ContextProvider(
            MultiScenarioData(
                scenario_ids=[r.scenario.id for r in response],
                gqueries={
                    key: [r.gqueries[key] for r in response]
                    for key in response[0].gqueries.keys()
                },
                inputs={
                    key: [r.inputs[key] for r in response]
                    for key in response[0].inputs.keys()
                },
                ui={},
            ),
            _ui_fields=accessed_attributes_ui,  # TODO: this is a slightly unwieldy way to insert the data
        )
