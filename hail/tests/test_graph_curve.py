from hail.models.calculate import GraphCurveElement
from hail.models.curve import Curve
from hail.result.graph_curve import AbstractResultCurveGraph


def test_group_elements_uses_curve_addition_before_filtering_on_index():
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


def test_group_elements_still_sums_list_values_elementwise():
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

    ontladen_trace = traces["Opslag (ontladen)"]
    assert ontladen_trace["stackgroup"] == "one"
    assert ontladen_trace["legendgroup"] == "Aanbod"
    assert ontladen_trace["legendgrouptitle"]["text"] == "Aanbod"
    assert ontladen_trace["y"] == [10.0, 0, 0, None, 0, 3.0]

    laden_trace = traces["Opslag (laden)"]
    assert laden_trace["stackgroup"] == "two"
    assert laden_trace["legendgroup"] == "Vraag"
    assert laden_trace["legendgrouptitle"]["text"] == "Vraag"
    assert laden_trace["y"] == [0, -5.0, 0, None, -2.0, 0]