from pydantic import BaseModel
from typing import Any, Dict, Optional, Callable
from temporalio import workflow

def define_event(
    name: str, handler: Optional[Callable], *, validator: Optional[Callable] = None
) -> None:
    return workflow.set_update_handler(name, handler, validator)

def on_event(name: str) -> Optional[Callable]:
    return workflow.get_update_handler(name)

class WorkflowEvent(BaseModel):
    name: str
    input: Optional[Dict[str, Any]] = None

class SendWorkflowEvent(BaseModel):
    event: WorkflowEvent
    workflow: Optional[str] = None  # Adjust type as needed for workflow execution info