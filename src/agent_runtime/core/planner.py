from dataclasses import dataclass
from typing import Any

from .action import Action
from .state import AgentState


@dataclass(frozen=True)
class RulePlanner:
    """Small deterministic planner that maps task intent to tool Actions."""

    tool_name: str

    def __call__(self, state: AgentState) -> list[Action]:
        return [Action(self.tool_name, {"text": state.task.goal})]
