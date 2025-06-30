import yaml
from crewai import Agent, Crew, Process, Task, LLM

def load_yaml(path):
  with open(path, 'r') as f:
    return yaml.safe_load(f)

def load_agents(agent_config_path):
  config = load_yaml(agent_config_path)
  central = config["central"]
  crew = config["crew"]

  central = Agent(
    role=central["role"],
    goal=central["goal"],
    backstore=central.get("backstore"),
    verbose=True,
    allow_delegation=True
  )

  crew_agents = []
  for member in crew:
    agent = Agent(
      role=member["role"],
      goal=member["goal"],
      backstore=member.get("backstore"),
      verbose=True
    )
    crew_agents.append((member["name"], agent))
  return central, crew_agents