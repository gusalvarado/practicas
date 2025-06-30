from simulation.game_state import GameState
from crew.loader import load_agents
from tools.assign_task_tool import AssignTaskTool

state = GameState()
central, crew_agents = load_agents("config/agents.yaml")

assign_tool = AssignTaskTool(state)
central.add_tools([assign_tool])

assignments = assign_tool.run({
    "agents": [(name, agent.role) for name, agent in crew_agents]
})