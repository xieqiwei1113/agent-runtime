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
    task: Task
    status: TaskStatus = TaskStatus.PENDING
    step: int = 0
    history: list[dict[str, Any]] = field(default_factory=list)
    result: Any = None
    error: str | None = None
    plan: list[Any] = field(default_factory=list)
    current_action: dict[str, Any] | None = None
    variables: dict[str, Any] = field(default_factory=dict)
    checkpoints: list[Any] = field(default_factory=list)

    def record(self, event: str, **data: Any) -> None:
        self.history.append({"event": event, "step": self.step, **data})
