from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .task import Task


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentState:
    """Execution state for the minimal M1 runtime."""

    task: Task
    status: TaskStatus = TaskStatus.PENDING
    step: int = 0
    history: list[dict[str, Any]] = field(default_factory=list)
    result: Any = None
    error: str | None = None

    def record(self, event: str, **data: Any) -> None:
        self.history.append({"event": event, "step": self.step, **data})
