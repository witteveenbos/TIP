import pytest
from hail.development import AbstractDevelopment, Group
from hail.context import ContextProvider
from hail.models.matrix import Matrix
from mock_context import MockMultiScenarioDataWrapper
from mock_config import TestDevelopment1, TestDevelopment2, TestDevelopment3

import logging


def test_group_total_fundamental():
    group = Group(name="Test Group", key="test_group")
    member1 = TestDevelopment1
    member2 = TestDevelopment2
    member3 = TestDevelopment3

    mock_context = ContextProvider(MockMultiScenarioDataWrapper(10))
    group.add_context(mock_context)
    group._add_member(member1)
    group._add_member(member2)
    group._add_member(member3)

    logging.debug(f"Group total: {group.TOTAL}")
    logging.debug(f"Group sum: {sum(group.TOTAL)}")
    assert isinstance(group.TOTAL, Matrix), "Group total is not a Matrix"
    assert sum(group.TOTAL) == 30, "Group total is not correct"
    assert len(group.TOTAL) == 10, "Group total length is not correct"
