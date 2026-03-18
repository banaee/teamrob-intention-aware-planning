"""
mesa_sim/viz/space_drawer.py

PURPOSE:
    Draws the simulation environment as a Plotly figure for SolaraViz.
    Reads all geometry from model — nothing hardcoded.

WHAT THIS MODULE DOES:
    - Draws static env objects from model.env_objects (shelves, tables,
      coffee machines, ac switches, obstacles) using positions and sizes
      from domain1.json
    - Draws zone boundaries from model.zone_map
    - Draws dynamic elements: agents (human, robot) and items
    - Draws planned paths if available on agents

WHAT THIS MODULE DOES NOT DO:
    - Does NOT hardcode any positions, sizes, or colors per object id
    - Does NOT know about factory vs any other domain — reads from model
    - Does NOT define agent appearance — that is portrayal.py

GEOMETRY:
    All coordinates are center-origin matching domain1.json.
    Plotly axes are set to match the model's ContinuousSpace bounds.

USED BY:
    - mesa_sim/run_mesa.py → passed to SolaraViz as space_drawer
"""

import solara
import plotly.graph_objects as go

from mesa_sim.agents import HumanAgent, RobotAgent


OBJ_COLORS = {
    "shelf": ("orange", 0.5),
    "kitting_table": ("gray", 0.6),
    "coffee_machine": ("saddlebrown", 0.7),
    "ac_switch": ("steelblue", 0.7),
    "obstacle": ("dimgray", 0.4),
}

ZONE_COLORS = {
    "zone_NW": "rgba(200,230,200,0.15)",
    "zone_NE": "rgba(200,200,230,0.15)",
    "zone_SW": "rgba(230,220,200,0.15)",
    "zone_SE": "rgba(230,200,200,0.15)",
}


def space_drawer(model, agent_portrayal):
    fig = go.Figure()
    _draw_zones(model, fig)
    _draw_env_objects(model, fig)
    _draw_items(model, fig)
    _draw_agents(model, fig)
    _draw_paths(model, fig)
    _update_layout(model, fig)
    solara.FigurePlotly(fig)
    return fig


def _draw_zones(model, fig):
    for zone_id, bounds in model.zone_map.items():
        color = ZONE_COLORS.get(zone_id, "rgba(200,200,200,0.1)")
        fig.add_shape(
            type="rect",
            x0=bounds["x_min"], y0=bounds["y_min"],
            x1=bounds["x_max"], y1=bounds["y_max"],
            fillcolor=color,
            line=dict(color="lightgray", width=1, dash="dot"),
            layer="below",
        )
        cx = (bounds["x_min"] + bounds["x_max"]) / 2
        cy = (bounds["y_min"] + bounds["y_max"]) / 2
        fig.add_annotation(
            x=cx, y=cy, text=zone_id,
            font=dict(color="gray", size=10),
            showarrow=False, opacity=0.5,
        )


def _draw_env_objects(model, fig):
    for obj_id, obj in model.env_objects.items():
        if obj.obj_type == "obstacle":
            _draw_rect(fig, obj.position, obj.size, "dimgray", 0.4, label=None)
        else:
            color, opacity = OBJ_COLORS.get(obj.obj_type, ("lightblue", 0.5))
            _draw_rect(fig, obj.position, obj.size, color, opacity, label=obj_id)


def _draw_rect(fig, position, size, color, opacity, label=None):
    x0 = position[0] - size[0] / 2
    y0 = position[1] - size[1] / 2
    x1 = position[0] + size[0] / 2
    y1 = position[1] + size[1] / 2
    fig.add_shape(
        type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
        fillcolor=color, opacity=opacity,
        line=dict(color=color, width=2),
    )
    if label:
        fig.add_annotation(
            x=position[0], y=position[1], text=label,
            font=dict(color="black", size=9),
            showarrow=False,
        )


def _draw_items(model, fig):
    for item_id, item in model.items.items():
        color = "red" if item.held_by else "black"
        x, y = item.position
        fig.add_shape(
            type="circle",
            x0=x - 12, y0=y - 12, x1=x + 12, y1=y + 12,
            line=dict(color=color, width=2),
            fillcolor=color, opacity=0.5,
        )
        fig.add_annotation(
            x=x, y=y, text=item_id,
            font=dict(color="white", size=8),
            showarrow=False,
        )


def _draw_agents(model, fig):
    for agent in model.humans.values():
        text = f"👷({agent.carrying})" if agent.carrying else "👷"
        fig.add_annotation(
            x=agent.pos[0], y=agent.pos[1], text=text,
            font=dict(size=20), showarrow=False,
        )
    for agent in model.robots.values():
        text = f"🤖({agent.carrying})" if agent.carrying else "🤖"
        fig.add_annotation(
            x=agent.pos[0], y=agent.pos[1], text=text,
            font=dict(size=20), showarrow=False,
        )


def _draw_paths(model, fig):
    for agent in list(model.humans.values()) + list(model.robots.values()):
        if not hasattr(agent, "planned_path") or not agent.planned_path:
            continue
        color = "blue" if isinstance(agent, RobotAgent) else "green"
        fig.add_trace(go.Scatter(
            x=[p[0] for p in agent.planned_path],
            y=[p[1] for p in agent.planned_path],
            mode="markers",
            marker=dict(color=color, size=4, opacity=0.4),
            showlegend=False,
        ))


def _update_layout(model, fig):
    fig.update_layout(
        width=800, height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    fig.update_xaxes(
        range=[model.space.x_min, model.space.x_max],
        showline=True, linewidth=2, linecolor="black", mirror=True,
        showgrid=False, showticklabels=True, title_text="",
    )
    fig.update_yaxes(
        range=[model.space.y_min, model.space.y_max],
        showline=True, linewidth=2, linecolor="black", mirror=True,
        showgrid=False, showticklabels=True, title_text="",
    )