from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .state import AgentState


@dataclass(frozen=True)
class StateCheckpoint:
    """Immutable snapshot of runtime state after an action boundary."""

    step: int
    status: str
    result: Any
    error: str | None
    variables: dict[str, Any]
    action_index: int
    history_size: int


def create_checkpoint(state: AgentState, action_index: int) -> StateCheckpoint:
    return StateCheckpoint(
        step=state.step,
        status=state.status.value,
        result=deepcopy(state.result),
        error=state.error,
        variables=deepcopy(state.variables),
        action_index=action_index,
        history_size=len(state.history),
    )
