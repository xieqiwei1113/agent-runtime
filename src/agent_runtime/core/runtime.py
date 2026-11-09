from collections.abc import Callable
from typing import Any
from .action import Action
from .checkpoint import create_checkpoint
from .state import AgentState, TaskStatus
from .task import Task

Planner = Callable[[AgentState], list[Action] | Any]

class AgentRuntime:
    """M1 runtime with explicit state, multi-step actions, and checkpoints."""
    def __init__(self, planner: Planner) -> None:
        self.planner = planner

    def run(self, task: Task) -> AgentState:
        state = AgentState(task=task, status=TaskStatus.RUNNING)
        state.record("task_started", goal=task.goal)
        try:
            plan = self.planner(state)
            state.plan = plan if isinstance(plan, list) else [Action(name="finish", output=plan)]
            state.record("plan_created", actions=[a.name for a in state.plan])
            for action in state.plan:
                state.step += 1
                state.current_action = {"name": action.name, "input": action.input}
                action.status = "running"
                state.record("action_started", action=action.name)
                result = action.output if action.output is not None else action.input.get("result")
                action.output = result
                action.status = "completed"
                state.variables[action.name] = result
                state.record("action_completed", action=action.name, output=result)
                state.checkpoints.append(create_checkpoint(state))
            state.result = state.variables.get(state.plan[-1].name) if state.plan else None
            state.current_action = None
            state.status = TaskStatus.COMPLETED
            state.record("task_completed")
        except Exception as exc:
            state.status = TaskStatus.FAILED
            state.error = str(exc)
            state.record("task_failed", error=state.error)
            state.checkpoints.append(create_checkpoint(state))
        return state
