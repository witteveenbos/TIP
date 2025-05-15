import logging
import random
from hail.models.matrix import Matrix
from hail.context import ContextProvider
from hail.models.response import InputResult, QueryResult


class FallbackMatrix(Matrix):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, _):
        return Matrix(self.data)


class MockMultiScenarioDataWrapper:

    MODEL_FIELDS = InputResult.model_fields.keys() | QueryResult.model_fields.keys()
    KWARGS = [
        "is_input_result",
        "name",
    ]

    def __init__(self, num_scenarios: int, actual_ids=None, **kwargs):
        self._scenario_ids = [i for i in range(num_scenarios)]
        self._actual_ids = actual_ids  # store for reinitialization

        self.data = {}
        for kwarg in kwargs:
            if kwarg not in self.KWARGS:
                logging.warning(f"Unknown kwarg: {kwarg}")
            else:
                self.data[kwarg] = kwargs[kwarg]

        if actual_ids is not None:  # overwrite scenario_ids if actual_ids are provided
            self._scenario_ids = actual_ids

    def __getattr__(self, item):

        if item in self.KWARGS:
            return self.data.get(item, None)

        if item in self.MODEL_FIELDS:
            return Matrix([1 for _ in range(len(self._scenario_ids))])
        if item == "ui":
            return FallbackMatrix([1 for _ in range(len(self._scenario_ids))])

        if item == "etm_key":
            return "etm_key_test_case" + str(random.randint(0, 1000))

        else:
            # return as if we are actually a level deeper (actual object would return a FilterList of InputResults)
            # we check this using the is_input_result flag
            return MockMultiScenarioDataWrapper(
                len(self._scenario_ids),
                self._actual_ids,
                is_input_result=True,
                name=item,
            )

    @property
    def scenario_ids(self):
        return self._scenario_ids

    @classmethod
    def from_actual_ids(cls, actual_ids):
        return cls(len(actual_ids), actual_ids)


mock_context_provider = ContextProvider(MockMultiScenarioDataWrapper(10))
