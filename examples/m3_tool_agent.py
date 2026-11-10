from agent_runtime import AgentRuntime, RulePlanner, Task, Tool, ToolRegistry


def uppercase(data):
    return data["text"].upper()


registry = ToolRegistry(
    [Tool("uppercase", "Convert text to uppercase", uppercase)]
)

planner = RulePlanner("uppercase")


def executor(action, _state):
    return registry.execute(action.name, action.input)


if __name__ == "__main__":
    state = AgentRuntime(planner, executor).run(Task("agent runtime is ready"))

    print("status:", state.status.value)
    print("result:", state.result)
    print("tool output:", state.variables["uppercase"])
