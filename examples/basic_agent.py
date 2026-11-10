from agent_runtime import AgentRuntime, Task


def planner(state):
    return f"Completed: {state.task.goal}"


if __name__ == "__main__":
    state = AgentRuntime(planner).run(Task("summarize today's work"))
    print("status:", state.status.value)
    print("result:", state.result)
    print("history:", state.history)
