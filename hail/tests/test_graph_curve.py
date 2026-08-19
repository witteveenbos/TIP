from hail.models.calculate import GraphCurveElement
from hail.models.curve import Curve
from hail.result.graph_curve import AbstractResultCurveGraph


def test_group_elements_uses_curve_addition_before_filtering_on_index():
    """
    GIVEN two GraphCurveElements in the same group, each with Curve values across two scenarios.
    WHEN _group_elements is called.
    THEN the curves are summed element-wise across scenarios before any per-scenario filtering,
    so that filtering on an index afterwards returns the correctly aggregated values.
    """
    grouped_elements = AbstractResultCurveGraph._group_elements(
        [
            GraphCurveElement(
                name="Solar rooftop",
                group="Zon",
                demandSupply="Aanbod",
                color="#fed976",
                value=Curve([[1.0, None, 3.0], [10.0, 20.0, 30.0]]),
            ),
            GraphCurveElement(
                name="Solar field",
                group="Zon",
                demandSupply="Aanbod",
                color="#fed976",
                value=Curve([[2.5, 4.0, None], [1.0, None, 5.0]]),
            ),
        ]
    )

    assert len(grouped_elements) == 1
    assert grouped_elements[0].group == "Zon"
    filtered_group = grouped_elements[0].filter_on_index(0)
    assert filtered_group.value == [3.5, 4.0, 3.0]


def test_group_elements_sum_list_values_elementwise():
    """
    GiVEN two GraphCurveElements in the same group, each with plain list values.
    WHEN _group_elements is called.
    THEN corresponding list positions are summed, treating None as zero on either side,
    and the result is a single element with the merged values.
    """
    grouped_elements = AbstractResultCurveGraph._group_elements(
        [
            GraphCurveElement(
                name="Solar rooftop",
                group="Zon",
                demandSupply="Aanbod",
                color="#fed976",
                value=[1.0, None, 3.0],
            ),
            GraphCurveElement(
                name="Solar field",
                group="Zon",
                demandSupply="Aanbod",
                color="#fed976",
                value=[2.5, 4.0, None],
            ),
        ]
    )

    assert len(grouped_elements) == 1
    assert grouped_elements[0].value == [3.5, 4.0, 3.0]
    assert len(grouped_elements[0].value) == 3


def test_make_plotly_graph_splits_opslag_into_charging_and_discharging():
    """
    GIVEN a single GraphCurveElement in the Opslag group with mixed positive and negative values.
    WHEN _make_plotly_graph is called.
    THEN the trace is split into two separate traces: one for discharging (Aanbod, positive values)
    and one for charging (Vraag, negated values), each assigned to the correct stack group.
    """
    fig = AbstractResultCurveGraph._make_plotly_graph(
        [
            GraphCurveElement(
                name="Opslag",
                group="Opslag",
                demandSupply="Aanbod",
                color="#385ba6",
                value=[10.0, -5.0, 0.0, None, -2.0, 3.0],
            )
        ]
    )

    traces = {trace["name"]: trace for trace in fig.to_dict()["data"]}

    assert set(traces) == {"Opslag (ontladen)", "Opslag (laden)"}

    discharge_trace = traces["Opslag (ontladen)"]
    assert discharge_trace["stackgroup"] == "one"
    assert discharge_trace["legendgroup"] == "Aanbod"
    assert discharge_trace["legendgrouptitle"]["text"] == "Aanbod"
    assert discharge_trace["y"] == [10.0, 0, 0, None, 0, 3.0]

    charge_trace = traces["Opslag (laden)"]
    assert charge_trace["stackgroup"] == "two"
    assert charge_trace["legendgroup"] == "Vraag"
    assert charge_trace["legendgrouptitle"]["text"] == "Vraag"
    assert charge_trace["y"] == [0, -5.0, 0, None, -2.0, 0]


# Tests for _is_all_zero_values
def test_is_all_zero_values_with_all_zeros_list():
    """
    GIVEN a list containing only zeros.
    WHEN _is_all_zero_values is called.
    THEN it returns True.
    """
    assert AbstractResultCurveGraph._is_all_zero_values([0, 0, 0]) is True


def test_is_all_zero_values_with_all_zeros_curve():
    """
    GIVEN a Curve containing only zero rows.
    WHEN _is_all_zero_values is called.
    THEN it recursively validates and returns True.
    """
    curve = Curve([[0, 0], [0, 0]])
    assert AbstractResultCurveGraph._is_all_zero_values(curve) is True


def test_is_all_zero_values_with_mixed_zero_and_nonzero():
    """
    GIVEN a list with both zero and non-zero values.
    WHEN _is_all_zero_values is called.
    THEN it returns False.
    """
    assert AbstractResultCurveGraph._is_all_zero_values([0, 1, 0]) is False


def test_is_all_zero_values_with_all_none():
    """
    GIVEN a list containing only None values.
    WHEN _is_all_zero_values is called.
    THEN it returns True (treats None as "don't care").
    """
    assert AbstractResultCurveGraph._is_all_zero_values([None, None]) is True


def test_is_all_zero_values_with_none_and_zeros():
    """
    GIVEN a list with None and zero values.
    WHEN _is_all_zero_values is called.
    THEN it returns True.
    """
    assert AbstractResultCurveGraph._is_all_zero_values([None, 0, None]) is True


def test_is_all_zero_values_with_none_and_nonzero():
    """
    GIVEN a list with None and non-zero values.
    WHEN _is_all_zero_values is called.
    THEN it returns False.
    """
    assert AbstractResultCurveGraph._is_all_zero_values([None, 1, None]) is False


def test_is_all_none_values_with_none_and_zero():
    """
    GIVEN a list containing None and zero values.
    WHEN _is_all_none_values is called.
    THEN it returns False because zero is a valid curve value.
    """
    assert AbstractResultCurveGraph._is_all_none_values([None, 0, None]) is False


def test_is_all_none_values_with_all_none():
    """
    GIVEN a list containing only None values.
    WHEN _is_all_none_values is called.
    THEN it returns True.
    """
    assert AbstractResultCurveGraph._is_all_none_values([None, None]) is True


# Tests for _negative_values
def test_negative_values_inverts_list():
    """
    GIVEN a list of positive and negative values.
    WHEN _negative_values is called.
    THEN all values are negated.
    """
    result = AbstractResultCurveGraph._negative_values([1.0, -2.5, 3.0])
    assert result == [-1.0, 2.5, -3.0]


def test_negative_values_preserves_none():
    """
    GIVEN a list with None values.
    WHEN _negative_values is called.
    THEN None values are preserved.
    """
    result = AbstractResultCurveGraph._negative_values([1.0, None, -2.0])
    assert result == [-1.0, None, 2.0]


def test_negative_values_with_all_none():
    """
    GIVEN a list containing only None.
    WHEN _negative_values is called.
    THEN all None values are preserved.
    """
    result = AbstractResultCurveGraph._negative_values([None, None])
    assert result == [None, None]


# Tests for _split_storage_trace
def test_split_storage_trace_all_positive_creates_only_discharging():
    """
    GIVEN a storage element with only positive values.
    WHEN _split_storage_trace is called.
    THEN only a discharging trace (Aanbod) is created.
    """
    element = GraphCurveElement(
        name="Opslag",
        group="Opslag",
        demandSupply="Aanbod",
        color="#385ba6",
        value=[5.0, 10.0, 3.0],
    )
    split = AbstractResultCurveGraph._split_storage_trace(element)

    assert len(split) == 1
    assert split[0].name == "Opslag (ontladen)"
    assert split[0].demandSupply == "Aanbod"
    assert split[0].value == [5.0, 10.0, 3.0]


def test_split_storage_trace_all_negative_creates_only_charging():
    """
    GIVEN a storage element with only negative values.
    WHEN _split_storage_trace is called.
    THEN only a charging trace (Vraag) is created with negated values.
    """
    element = GraphCurveElement(
        name="Opslag",
        group="Opslag",
        demandSupply="Aanbod",
        color="#385ba6",
        value=[-5.0, -10.0, -3.0],
    )
    split = AbstractResultCurveGraph._split_storage_trace(element)

    assert len(split) == 1
    assert split[0].name == "Opslag (laden)"
    assert split[0].demandSupply == "Vraag"
    assert split[0].value == [5.0, 10.0, 3.0]


def test_split_storage_trace_all_zeros_creates_no_traces():
    """
    GIVEN a storage element with only zero values.
    WHEN _split_storage_trace is called.
    THEN no traces are created (zero values filtered out).
    """
    element = GraphCurveElement(
        name="Opslag",
        group="Opslag",
        demandSupply="Aanbod",
        color="#385ba6",
        value=[0.0, 0.0, 0.0],
    )
    split = AbstractResultCurveGraph._split_storage_trace(element)

    assert len(split) == 0


def test_split_storage_trace_with_none_values():
    """
    GIVEN a storage element with None values mixed in.
    WHEN _split_storage_trace is called.
    THEN None values are preserved in both traces.
    """
    element = GraphCurveElement(
        name="Opslag",
        group="Opslag",
        demandSupply="Aanbod",
        color="#385ba6",
        value=[5.0, None, -3.0],
    )
    split = AbstractResultCurveGraph._split_storage_trace(element)

    assert len(split) == 2
    discharge = next(t for t in split if t.name == "Opslag (ontladen)")
    charge = next(t for t in split if t.name == "Opslag (laden)")
    assert discharge.value == [5.0, None, 0.0]
    assert charge.value == [0.0, None, 3.0]


# Tests for _group_elements edge cases
def test_group_elements_empty_list():
    """
    GIVEN an empty list of elements.
    WHEN _group_elements is called.
    THEN an empty list is returned.
    """
    result = AbstractResultCurveGraph._group_elements([])
    assert result == []


def test_group_elements_multiple_distinct_groups():
    """
    GIVEN elements from different groups.
    WHEN _group_elements is called.
    THEN each group is aggregated separately.
    """
    grouped = AbstractResultCurveGraph._group_elements(
        [
            GraphCurveElement(
                name="Solar",
                group="Zon",
                demandSupply="Aanbod",
                color="#fed976",
                value=[5.0],
            ),
            GraphCurveElement(
                name="Wind",
                group="Wind",
                demandSupply="Aanbod",
                color="#e7ba52",
                value=[10.0],
            ),
        ]
    )

    assert len(grouped) == 2
    groups = {g.group: g for g in grouped}
    assert groups["Zon"].value == [5.0]
    assert groups["Wind"].value == [10.0]


def test_group_elements_single_element_per_group():
    """
    GIVEN a single element in a group.
    WHEN _group_elements is called.
    THEN it is returned as-is.
    """
    element = GraphCurveElement(
        name="Solar",
        group="Zon",
        demandSupply="Aanbod",
        color="#fed976",
        value=[5.0],
    )
    grouped = AbstractResultCurveGraph._group_elements([element])

    assert len(grouped) == 1
    assert grouped[0].name == "Zon"
    assert grouped[0].value == [5.0]


def test_group_elements_keeps_groups_that_sum_to_zero():
    """
    GIVEN elements that sum to all zeros.
    WHEN _group_elements is called.
    THEN the group is retained because zero is a valid curve value.
    """
    grouped = AbstractResultCurveGraph._group_elements(
        [
            GraphCurveElement(
                name="Solar 1",
                group="Zon",
                demandSupply="Aanbod",
                color="#fed976",
                value=[5.0, -5.0],
            ),
            GraphCurveElement(
                name="Solar 2",
                group="Zon",
                demandSupply="Aanbod",
                color="#fed976",
                value=[-5.0, 5.0],
            ),
        ]
    )

    assert len(grouped) == 1
    assert grouped[0].value == [0.0, 0.0]


def test_group_elements_filters_out_all_none_groups():
    """
    GIVEN elements whose values are all None.
    WHEN _group_elements is called.
    THEN the group is filtered out because it has no data.
    """
    grouped = AbstractResultCurveGraph._group_elements(
        [
            GraphCurveElement(
                name="Solar 1",
                group="Zon",
                demandSupply="Aanbod",
                color="#fed976",
                value=[None, None],
            ),
            GraphCurveElement(
                name="Solar 2",
                group="Zon",
                demandSupply="Aanbod",
                color="#fed976",
                value=[None, None],
            ),
        ]
    )

    assert grouped == []


# Tests for _make_plotly_graph trace ordering
def test_make_plotly_graph_aanbod_before_vraag():
    """
    GIVEN elements with both Aanbod and Vraag values.
    WHEN _make_plotly_graph is called.
    THEN Aanbod traces appear before Vraag traces in the figure.
    """
    fig = AbstractResultCurveGraph._make_plotly_graph(
        [
            GraphCurveElement(
                name="Supply",
                group="Energy",
                demandSupply="Aanbod",
                color="#1f77b4",
                value=[10.0],
            ),
            GraphCurveElement(
                name="Demand",
                group="Energy",
                demandSupply="Vraag",
                color="#ff7f0e",
                value=[5.0],
            ),
        ]
    )

    traces = [t["name"] for t in fig.to_dict()["data"]]
    supply_idx = traces.index("Supply")
    demand_idx = traces.index("Demand")
    assert supply_idx < demand_idx


def test_make_plotly_graph_last_group_at_end():
    """
    GIVEN elements including one in _LAST_GROUP_NAME.
    WHEN _make_plotly_graph is called.
    THEN the last group traces appear at the end (layered on top).
    """
    fig = AbstractResultCurveGraph._make_plotly_graph(
        [
            GraphCurveElement(
                name="Regular",
                group="Regular Group",
                demandSupply="Aanbod",
                color="#1f77b4",
                value=[10.0],
            ),
            GraphCurveElement(
                name="Flexibility",
                group="Overige flexibiliteit",  # _LAST_GROUP_NAME
                demandSupply="Aanbod",
                color="#2ca02c",
                value=[5.0],
            ),
        ]
    )

    traces = [t["name"] for t in fig.to_dict()["data"]]
    regular_idx = traces.index("Regular")
    flexibility_idx = traces.index("Flexibility")
    assert regular_idx < flexibility_idx


def test_make_plotly_graph_baseload_has_dashed_line_and_no_stackgroup():
    """
    GIVEN a baseload electricity demand element.
    WHEN _make_plotly_graph is called.
    THEN the trace has a dashed line, fill=none, and no stackgroup.
    """
    fig = AbstractResultCurveGraph._make_plotly_graph(
        [
            GraphCurveElement(
                name="Basislast elektriciteitsvraag",
                group="Demand",
                demandSupply="Vraag",
                color="#d62728",
                value=[5.0, 5.0],
            ),
        ]
    )

    traces = {t["name"]: t for t in fig.to_dict()["data"]}
    baseload = traces["Basislast elektriciteitsvraag"]
    assert baseload["line"]["dash"] == "dot"
    assert baseload["fill"] == "none"
    assert "stackgroup" not in baseload or baseload.get("stackgroup") is None


def test_make_plotly_graph_non_opslag_preserves_values():
    """
    GIVEN a non-Opslag element with positive and negative values.
    WHEN _make_plotly_graph is called.
    THEN the values are preserved as-is (not split).
    """
    fig = AbstractResultCurveGraph._make_plotly_graph(
        [
            GraphCurveElement(
                name="Mixed Energy",
                group="Energy",
                demandSupply="Aanbod",
                color="#1f77b4",
                value=[10.0, -5.0, 3.0],
            ),
        ]
    )

    traces = {t["name"]: t for t in fig.to_dict()["data"]}
    assert len(traces) == 1
    assert traces["Mixed Energy"]["y"] == [10.0, -5.0, 3.0]
