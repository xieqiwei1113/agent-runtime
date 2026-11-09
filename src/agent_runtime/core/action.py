from dataclasses import dataclass, field
from typing import Any, Literal

ActionStatus = Literal["pending", "running", "completed", "failed"]

@dataclass
class Action:
    name: str
    input: dict[str, Any] = field(default_factory=dict)
    status: ActionStatus = "pending"
    output: Any = None
    error: str | None = None
