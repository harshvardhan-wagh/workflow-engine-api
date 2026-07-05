from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import (
    WorkflowInstance, Workflow, Approval, User,
    InstanceStatus, Decision,
)
from app.schemas import InstanceDetailOut, DecisionRequest

router = APIRouter(prefix="/instances", tags=["instances"])


@router.get("/{instance_id}", response_model=InstanceDetailOut)
def get_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    instance = db.query(WorkflowInstance).filter(WorkflowInstance.id == instance_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    return instance


@router.post("/{instance_id}/decide", response_model=InstanceDetailOut)
def decide_step(
    instance_id: int,
    decision_in: DecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    instance = db.query(WorkflowInstance).filter(WorkflowInstance.id == instance_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")

    if instance.status != InstanceStatus.pending:
        raise HTTPException(status_code=400, detail="Instance already finalized")

    workflow = db.query(Workflow).filter(Workflow.id == instance.workflow_id).first()
    required_role = workflow.steps[instance.current_step]

    if current_user.role != required_role and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail=f"Step {instance.current_step + 1} requires role '{required_role}'",
        )

    approval = Approval(
        instance_id=instance.id,
        step_number=instance.current_step,
        approver_id=current_user.id,
        decision=decision_in.decision,
        comment=decision_in.comment,
    )
    db.add(approval)

    if decision_in.decision == Decision.rejected:
        instance.status = InstanceStatus.rejected
    else:
        next_step = instance.current_step + 1
        if next_step >= len(workflow.steps):
            instance.status = InstanceStatus.approved
        else:
            instance.current_step = next_step

    db.commit()
    db.refresh(instance)
    return instance
