from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .action import Action
from .task import Task


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentState:
    """Execution state shared across the M1 and M2 runtime."""

    task: Task
    status: TaskStatus = TaskStatus.PENDING
    step: int = 0
    history: list[dict[str, Any]] = field(default_factory=list)
    result: Any = None
    error: str | None = None
    actions: list[Action] = field(default_factory=list)
    variables: dict[str, Any] = field(default_factory=dict)
    checkpoints: list[Any] = field(default_factory=list)

    def record(self, event: str, **data: Any) -> None:
        self.history.append({"event": event, "step": self.step, **data})
