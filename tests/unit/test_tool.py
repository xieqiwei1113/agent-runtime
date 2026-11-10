from agent_runtime import RulePlanner, Task, Tool, ToolRegistry


def test_tool_registry_executes_registered_tool():
    registry = ToolRegistry(
        [Tool("uppercase", "Convert text to uppercase", lambda data: data["text"].upper())]
    )

    assert registry.execute("uppercase", {"text": "hello"}) == "HELLO"


def test_rule_planner_creates_tool_action():
    action = RulePlanner("uppercase")(type("State", (), {"task": Task("hello")})())[0]

    assert action.name == "uppercase"
    assert action.input == {"text": "hello"}
