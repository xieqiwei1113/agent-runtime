from agent_runtime import AgentRuntime, Task


def planner(state):
    return f"Completed: {state.task.goal}"


if __name__ == "__main__":
    state = AgentRuntime(planner).run(Task("summarize today's work"))
    print(state.status, state.result)
