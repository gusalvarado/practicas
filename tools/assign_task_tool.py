from crewai import tool

class AssignTaskTool(tool):
  def __init__(self, game_state):
    super().__init__(
      name="Assign Task Tool",
      description="Assigns the best task for each crew agent based on room statuses and roles.",
      func=self.assign_tasks
    )
    self.game_state = game_state

  def assign_tasks(self, inputs):
    """inputs: dict with 'agents': [(name, role), ...]"""
    assignments = {}
    critical_rooms = [
      room for room, info in self.game_state.rooms.items()
      if info['status'] in ('critical', 'damaged')
    ]
    for i, (agent_name, role) in enumerate(inputs.get("agents", [])):
      if i < len(critical_rooms):
        target_room = critical_rooms[i]
        assignments[agent_name] = f"repair {target_room}"
        self.game_state.assign_agent_to_room(agent_name, target_room)
      else:
        assignments[agent_name] = "standby"
    return assignments