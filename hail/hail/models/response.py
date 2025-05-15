import logging
from pydantic import BaseModel, ConfigDict
from typing import Union, Optional, List, Dict, Any
from datetime import datetime


class QueryResult(BaseModel):
    present: float | None
    future: float
    unit: str | None


class InputResult(BaseModel):
    default: float | int
    user: Optional[float | int] = None
    max: float | int
    min: float | int
    unit: str
    share_group: Optional[str] = None
    disabled: Optional[bool] = None
    disabled_by: Optional[str] = None
    coupling_groups: Optional[str] = None

    model_config = ConfigDict(extra="allow")

    # this field allows us to store the user value from the initial context
    user_from_initial_context: Optional[float | int] = None

    @property
    def user_original(self) -> Optional[float | int]:
        # if we are in the initial context, the user value is returned
        # if not, the value should be inserted from the inital context
        # otherwise we enter a loop we don't want to be in

        if self.user_from_initial_context is not None:
            return self.user_from_initial_context
        elif self.user is not None:
            return self.user
        elif self.default is not None:
            return self.default
        else:
            raise ValueError(
                f"No user value found. Please check the input data (one of ShareGroup: {self.share_group})."
            )


class ScenarioData(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    user_values: Dict[str, Union[str, int, float]]
    end_year: int
    keep_compatible: bool
    private: bool
    area_code: str
    source: str | None
    balanced_values: Dict[str, Union[str, int, float]]
    metadata: Dict[str, Union[str, int, float]]
    start_year: int
    coupling: Optional[bool] = None
    users: Optional[Union[List[Any], List[str]]] = None
    scaling: Optional[Union[str, int, float]]
    template: Optional[Union[str, int, float]]
    url: str


class APIResponse(BaseModel):
    scenario: ScenarioData
    gqueries: Optional[Dict[str, QueryResult]] = None
    inputs: Optional[Dict[str, InputResult]] = None
