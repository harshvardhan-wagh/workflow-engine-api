from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.models import UserRole, InstanceStatus, Decision


# ---------- Auth ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.employee


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Workflows ----------

class WorkflowCreate(BaseModel):
    name: str
    steps: List[str]  # ordered list of approver roles


class WorkflowOut(BaseModel):
    id: int
    name: str
    steps: List[str]
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Workflow Instances ----------

class InstanceOut(BaseModel):
    id: int
    workflow_id: int
    current_step: int
    status: InstanceStatus
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class ApprovalOut(BaseModel):
    id: int
    step_number: int
    approver_id: int
    decision: Decision
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class InstanceDetailOut(InstanceOut):
    approvals: List[ApprovalOut] = []


class DecisionRequest(BaseModel):
    decision: Decision
    comment: Optional[str] = None
