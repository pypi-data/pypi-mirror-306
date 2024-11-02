from typing import Optional, Callable
from temporalio import workflow

def define_memory(
    name: str, handler: Optional[Callable], *, validator: Optional[Callable] = None
) -> None:
    return workflow.set_query_handler(name, handler, validator)
