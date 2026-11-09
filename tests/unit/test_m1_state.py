from agent_runtime import Action, AgentRuntime, Task, TaskStatus

def test_multi_step_plan_updates_state():
    state = AgentRuntime(lambda _s: [Action(name="collect", output="data"), Action(name="summarize", output="summary")]).run(Task("prepare report"))
    assert state.status is TaskStatus.COMPLETED
    assert state.step == 2
    assert state.variables == {"collect": "data", "summarize": "summary"}
    assert state.result == "summary"
    assert len(state.checkpoints) == 2

def test_checkpoint_preserves_execution_position():
    state = AgentRuntime(lambda _s: [Action(name="first", output=1), Action(name="second", output=2)]).run(Task("demo"))
    checkpoint = state.checkpoints[0]
    assert checkpoint.step == 1
    assert checkpoint.status == "running"
    assert checkpoint.history_size == 4

def test_planner_failure_is_checkpointed():
    def planner(_s):
        raise RuntimeError("planner failed")
    state = AgentRuntime(planner).run(Task("demo"))
    assert state.status is TaskStatus.FAILED
    assert state.error == "planner failed"
    assert state.checkpoints[-1].status == "failed"
