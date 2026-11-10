from collections.abc import Callable
from typing import Any

from .state import AgentState, TaskStatus
from .task import Task

Planner = Callable[[AgentState], Any]


class AgentRuntime:
    """Minimal M1 runtime: Task -> Planner -> Result -> Finish."""

    def __init__(self, planner: Planner) -> None:
        self.planner = planner

    def run(self, task: Task) -> AgentState:
        state = AgentState(task=task, status=TaskStatus.RUNNING)
        state.record("task_started", goal=task.goal)

        try:
            state.record("planning_started")
            result = self.planner(state)
            state.result = result
            state.record("plan_completed", result=result)
            state.status = TaskStatus.COMPLETED
            state.record("task_completed")
        except Exception as exc:
            state.status = TaskStatus.FAILED
            state.error = str(exc)
            state.record("task_failed", error=state.error)

        return state
