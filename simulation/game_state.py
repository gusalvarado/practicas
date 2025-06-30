class GameState:
  def __init__(self):
    self.rooms = {
      "Reactor": {"status": "damaged", "crew": []},
      "MedBay": {"status": "operational", "crew": []},
      "Bridge": {"status": "operational", "crew": []},
    }
    self.tick = 0

  def get_status_report(self):
    return {room: data["status"] for room, data in self.rooms.items()}

  def update_room(self, room, new_status):
    if room in self.rooms:
      self.rooms[room]["status"] = new_status
    else:
      raise ValueError(f"Room {room} does not exist.")

  def assign_agent_to_room(self, agent, room):
    for r in self.rooms:
      self.rooms[r]["crew"] = [a for a in self.rooms[r]["crew"] if a != agent]
    self.rooms[room]["crew"].append(agent)

  def advance_tick(self):
    self.tick += 1