from agent_runtime import AgentRuntime, Task, TaskStatus


def test_success_lifecycle():
    runtime = AgentRuntime(lambda state: f"done: {state.task.goal}")
    state = runtime.run(Task("demo"))

    assert state.status is TaskStatus.COMPLETED
    assert state.result == "done: demo"
    assert state.error is None
    assert [event["event"] for event in state.history] == [
        "task_started",
        "planning_started",
        "plan_completed",
        "task_completed",
    ]


def test_planner_receives_runtime_state():
    def planner(state):
        assert state.task.goal == "demo"
        assert state.status is TaskStatus.RUNNING
        return "ok"

    state = AgentRuntime(planner).run(Task("demo"))

    assert state.result == "ok"


def test_failure_lifecycle():
    def planner(_state):
        raise ValueError("boom")

    state = AgentRuntime(planner).run(Task("demo"))

    assert state.status is TaskStatus.FAILED
    assert state.result is None
    assert state.error == "boom"
    assert state.history[-1]["event"] == "task_failed"
