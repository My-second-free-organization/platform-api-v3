from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class WorkflowStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Workflow(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    status: WorkflowStatus = WorkflowStatus.DRAFT
    version: int = 1
    tenant_id: Optional[str] = None
    created_at: Optional[datetime] = None

class WorkflowInstance(BaseModel):
    id: Optional[str] = None
    workflow_id: str
    status: str = "RUNNING"
    variables: Optional[dict] = None
    started_at: Optional[datetime] = None

class Task(BaseModel):
    id: Optional[str] = None
    name: str
    type: str
    status: TaskStatus = TaskStatus.PENDING
    assignee: Optional[str] = None
    input_data: Optional[dict] = None
    output_data: Optional[dict] = None
