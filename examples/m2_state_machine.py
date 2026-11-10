from agent_runtime import Action, AgentRuntime, Task


def planner(_state):
    return [
        Action("collect_information"),
        Action("generate_summary"),
        Action("generate_report"),
    ]


def executor(action, state):
    if action.name == "collect_information":
        return "meeting notes"
    if action.name == "generate_summary":
        return f"summary from: {state.variables['collect_information']}"
    return f"report from: {state.variables['generate_summary']}"


if __name__ == "__main__":
    state = AgentRuntime(planner, executor).run(Task("create a meeting report"))

    print("status:", state.status.value)
    print("result:", state.result)
    print("variables:", state.variables)
    print("steps:", state.step)
    print("checkpoints:", len(state.checkpoints))
