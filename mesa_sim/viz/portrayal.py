"""
mesa_sim/viz/portrayal.py

PURPOSE:
    Defines how each agent type is visually represented in SolaraViz.
    Called by SolaraViz per agent per rendered frame.

WHAT THIS MODULE DOES:
    - Returns a portrayal dict for each agent type (HumanAgent, RobotAgent)
    - Uses agent state (carrying, current_task) to adjust appearance
    - Domain-independent: works for any scenario

WHAT THIS MODULE DOES NOT DO:
    - Does NOT define positions or sizes — those come from agent.pos
    - Does NOT draw static environment objects — that is space_drawer.py
    - Does NOT hardcode factory-specific logic

USED BY:
    - mesa_sim/run_mesa.py  → passed to SolaraViz as agent_portrayal
"""

from mesa_sim.agents import HumanAgent, RobotAgent

AGENT_DISPLAY_SIZE = 20  # TODO: read from mesa_configs.yaml if needed


def agent_portrayal(agent):
    if isinstance(agent, RobotAgent):
        return _robot_portrayal(agent)
    elif isinstance(agent, HumanAgent):
        return _human_portrayal(agent)
    return {"text": "?", "font_size": 10, "color": "gray", "Layer": 1}


def _robot_portrayal(agent: RobotAgent) -> dict:
    text = f"🤖({agent.carrying})" if agent.carrying else "🤖"
    return {"text": text, "font_size": AGENT_DISPLAY_SIZE, "color": "blue", "Layer": 3}


def _human_portrayal(agent: HumanAgent) -> dict:
    text = f"👷({agent.carrying})" if agent.carrying else "👷"
    return {"text": text, "font_size": AGENT_DISPLAY_SIZE, "color": "green", "Layer": 3}