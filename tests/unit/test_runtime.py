from agent_runtime import AgentRuntime, Task, TaskStatus


def test_success_lifecycle():
    runtime = AgentRuntime(lambda state: "ok")
    state = runtime.run(Task("demo"))

    assert state.status is TaskStatus.COMPLETED
    assert state.result == "ok"
    assert [e["event"] for e in state.history] == [
        "task_started", "plan_created", "task_completed"
    ]


def test_failure_lifecycle():
    def planner(_state):
        raise ValueError("boom")

    state = AgentRuntime(planner).run(Task("demo"))

    assert state.status is TaskStatus.FAILED
    assert state.error == "boom"
    assert state.history[-1]["event"] == "task_failed"
