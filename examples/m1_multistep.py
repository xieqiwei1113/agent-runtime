from agent_runtime import Action, AgentRuntime, Task

def planner(_state):
    return [Action(name="collect_information", output="meeting notes"), Action(name="generate_summary", output="three key points"), Action(name="generate_report", output="final report")]

state = AgentRuntime(planner).run(Task("整理会议报告"))
print("status:", state.status)
print("result:", state.result)
print("steps:", state.step)
print("variables:", state.variables)
print("checkpoints:", len(state.checkpoints))
