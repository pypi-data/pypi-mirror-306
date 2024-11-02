from typing import Optional, Callable
from temporalio import workflow

def define_memory(
    name: str, handler: Optional[Callable], *, validator: Optional[Callable] = None
) -> None:
    return workflow.set_query_handler(name, handler, validator)

def handle_memory(name: str) -> Optional[Callable]:
    return workflow.get_query_handler(name)
