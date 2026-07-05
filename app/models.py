import enum
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Enum, JSON
)
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(str, enum.Enum):
    employee = "employee"
    manager = "manager"
    senior_manager = "senior_manager"
    admin = "admin"


class InstanceStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Decision(str, enum.Enum):
    approved = "approved"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.employee, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # steps = ordered list of approver roles, e.g. ["manager", "senior_manager"]
    steps = Column(JSON, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    instances = relationship("WorkflowInstance", back_populates="workflow")


class WorkflowInstance(Base):
    __tablename__ = "workflow_instances"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    current_step = Column(Integer, default=0, nullable=False)
    status = Column(Enum(InstanceStatus), default=InstanceStatus.pending, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    workflow = relationship("Workflow", back_populates="instances")
    approvals = relationship("Approval", back_populates="instance")


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer, ForeignKey("workflow_instances.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    decision = Column(Enum(Decision), nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    instance = relationship("WorkflowInstance", back_populates="approvals")
