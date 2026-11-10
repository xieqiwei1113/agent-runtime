from agent_runtime import Action, AgentRuntime, Task, TaskStatus


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
    assert [event["step"] for event in state.history] == [0, 0, 1, 1]


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


def test_m2_executes_actions_and_creates_checkpoints():
    def planner(_state):
        return [
            Action("collect", {"source": "notes"}),
            Action("summarize"),
            Action("report"),
        ]

    def executor(action, state):
        if action.name == "collect":
            return "raw notes"
        if action.name == "summarize":
            return f"summary of {state.variables['collect']}"
        return f"report: {state.variables['summarize']}"

    state = AgentRuntime(planner, executor).run(Task("create report"))

    assert state.status is TaskStatus.COMPLETED
    assert state.result == "report: summary of raw notes"
    assert state.variables == {
        "collect": "raw notes",
        "summarize": "summary of raw notes",
        "report": "report: summary of raw notes",
    }
    assert len(state.checkpoints) == 3
    assert [cp.action_index for cp in state.checkpoints] == [0, 1, 2]
    assert state.checkpoints[-1].variables["summarize"] == "summary of raw notes"


def test_m2_stops_on_failed_action_and_checkpoints_failure():
    def planner(_state):
        return [Action("first"), Action("second")]

    def executor(action, _state):
        if action.name == "second":
            raise ValueError("tool failed")
        return "ok"

    state = AgentRuntime(planner, executor).run(Task("demo"))

    assert state.status is TaskStatus.FAILED
    assert state.error == "tool failed"
    assert state.actions[0].status == "completed"
    assert state.actions[1].status == "failed"
    assert len(state.checkpoints) == 2
    assert state.checkpoints[-1].status == "failed"
