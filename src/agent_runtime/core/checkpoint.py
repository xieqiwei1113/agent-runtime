from dataclasses import dataclass
from typing import Any
from .state import AgentState

@dataclass(frozen=True)
class StateCheckpoint:
    step: int
    status: str
    result: Any
    error: str | None
    history_size: int

def create_checkpoint(state: AgentState) -> StateCheckpoint:
    return StateCheckpoint(state.step, state.status.value, state.result, state.error, len(state.history))
