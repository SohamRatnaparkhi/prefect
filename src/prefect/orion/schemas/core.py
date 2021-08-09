import datetime
from typing import List, Dict
from uuid import UUID

from pydantic import Field

from prefect.orion.utilities.functions import ParameterSchema
from prefect.orion.utilities.schemas import PrefectBaseModel, APIBaseModel


class Flow(APIBaseModel):
    name: str = Field(..., example="my-flow")
    tags: List[str] = Field(default_factory=list, example=["tag-1", "tag-2"])
    parameters: ParameterSchema = Field(default_factory=ParameterSchema)


class FlowRunDetails(PrefectBaseModel):
    is_subflow: bool = True
    parent_task_run_id: UUID = None


class FlowRun(APIBaseModel):
    flow_id: UUID
    flow_version: str = Field(None, example="1.0")
    parameters: dict = Field(default_factory=dict)
    context: dict = Field(default_factory=dict, example={"my_var": "my_val"})
    empirical_policy: dict = Field(default_factory=dict)
    empirical_config: dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list, example=["tag-1", "tag-2"])
    flow_run_details: FlowRunDetails = Field(default_factory=FlowRunDetails)


class TaskRunDetails(PrefectBaseModel):
    is_subflow: bool = False
    subflow_run_id: UUID = None


class TaskRun(APIBaseModel):
    flow_run_id: UUID
    task_key: str
    dynamic_key: str = None
    cache_key: str = None
    cache_expiration: datetime.datetime = None
    task_version: str = None
    empirical_policy: dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list, example=["tag-1", "tag-2"])
    task_inputs: ParameterSchema = Field(default_factory=ParameterSchema)
    upstream_task_run_ids: Dict[str, UUID] = Field(default_factory=dict)
    task_run_details: TaskRunDetails = Field(default_factory=TaskRunDetails)
