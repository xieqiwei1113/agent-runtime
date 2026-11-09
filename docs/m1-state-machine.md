# M1: State Machine and Checkpoints

M1 extends M0 from a single planner result to explicit multi-step execution state.

New concepts: Action, plan, current_action, variables, and checkpoints.

Execution: Task -> Plan -> collect_information -> State Update -> generate_summary -> State Update -> generate_report -> Completed.

M1 still does not call an LLM or external tools. It establishes execution semantics first; M2 will make planning model-driven.
