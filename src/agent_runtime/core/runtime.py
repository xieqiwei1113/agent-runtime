from collections.abc import Callable, Sequence
from typing import Any

from .action import Action
from .checkpoint import create_checkpoint
from .state import AgentState, TaskStatus
from .task import Task

Planner = Callable[[AgentState], Any]
ActionExecutor = Callable[[Action, AgentState], Any]


class AgentRuntime:
    """Agent runtime supporting the M1 single-result loop and M2 action state machine."""

    def __init__(
        self,
        planner: Planner,
        action_executor: ActionExecutor | None = None,
    ) -> None:
        self.planner = planner
        self.action_executor = action_executor

    def run(self, task: Task) -> AgentState:
        state = AgentState(task=task, status=TaskStatus.RUNNING)
        state.record("task_started", goal=task.goal)

        try:
            state.record("planning_started")
            plan = self.planner(state)

            if isinstance(plan, Sequence) and not isinstance(plan, (str, bytes)):
                actions = list(plan)
                if not all(isinstance(action, Action) for action in actions):
                    raise TypeError("M2 planner must return Action objects")
                return self._run_actions(state, actions)

            # M1 compatibility: a planner can still return a direct result.
            state.step += 1
            state.result = plan
            state.record("plan_completed", result=plan)
            state.status = TaskStatus.COMPLETED
            state.record("task_completed")
        except Exception as exc:
            state.status = TaskStatus.FAILED
            state.error = str(exc)
            state.record("task_failed", error=state.error)

        return state

    def _run_actions(self, state: AgentState, actions: list[Action]) -> AgentState:
        if self.action_executor is None:
            raise RuntimeError("action_executor is required for M2 action plans")

        state.actions = actions
        state.record("plan_created", action_count=len(actions))

        for index, action in enumerate(state.actions):
            state.step += 1
            action.status = "running"
            state.record("action_started", action=action.name, action_index=index)

            try:
                output = self.action_executor(action, state)
                action.output = output
                action.status = "completed"
                state.variables[action.name] = output
                state.record("action_completed", action=action.name, action_index=index)
            except Exception as exc:
                action.status = "failed"
                action.error = str(exc)
                state.error = action.error
                state.status = TaskStatus.FAILED
                state.record("action_failed", action=action.name, action_index=index, error=action.error)
                state.checkpoints.append(create_checkpoint(state, index))
                return state

            state.result = action.output
            state.checkpoints.append(create_checkpoint(state, index))
            state.record("checkpoint_created", action_index=index)

        state.status = TaskStatus.COMPLETED
        state.record("task_completed")
        return state
