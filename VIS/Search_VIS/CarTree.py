import ast
import pygame
import os

def parse_state(state_vars):
    """
    Parses all agent-specific car state variables from stringified keys.

    Args:
        state_vars (dict): Dict with keys like "['v', 'car1']" and float/bool values.

    Returns:
        dict: Per-agent state dictionary.
    """
    agents = {}

    for raw_key, value in state_vars.items():
        key_parts = ast.literal_eval(raw_key)  # convert string to list
        if isinstance(key_parts, (list, tuple)) and len(key_parts) == 2:
            predicate, agent = key_parts

            if agent not in agents:
                agents[agent] = {
                    "velocity": 0.0,
                    "acceleration": 0.0,
                    "distance": 0.0,
                    "running": False,
                    "engine_blown": False,
                    "goal_reached": False,
                    "running_time": 0.0
                }

            if predicate == "v":
                agents[agent]["velocity"] = value
            elif predicate == "a":
                agents[agent]["acceleration"] = value
            elif predicate == "d":
                agents[agent]["distance"] = value
            elif predicate == "running":
                agents[agent]["running"] = value
            elif predicate == "engineblown":
                agents[agent]["engine_blown"] = value
            elif predicate == "goal_reached":
                agents[agent]["goal_reached"] = value
            elif predicate == "running_time":
                agents[agent]["running_time"] = value

    return agents

def render_domain(node, surface, font, res_dir, width, height):
    # Load images
    road_img = pygame.image.load(os.path.join(res_dir, "road-2.jpg"))
    road_img = pygame.transform.scale(road_img, (width, height))
    car_img = pygame.image.load(os.path.join(res_dir, "car.png"))
    car_img = pygame.transform.scale(car_img, (150, 60))

    surface.blit(road_img, (0, 0))  # draw background

    # Parse the car states for all agents
    state_vars = getattr(node.state, "state_vars", [])
    car_states = parse_state(state_vars)

    max_distance = 1000  # adjust based on your domain scale

    for i, (agent, state) in enumerate(car_states.items()):
        distance = state.get("distance", 0.0)
        x_pos = int((distance / max_distance) * (width - 200))

        # Updated: align cars to road lanes at the bottom half
        lane_y_start = height * 0.5  # start of road area
        lane_spacing = 80  # vertical space between lanes
        y_pos = int(lane_y_start + i * lane_spacing)

        surface.blit(car_img, (x_pos, y_pos))

        # Draw agent name
        label = font.render(agent, True, (255, 255, 255))
        surface.blit(label, (x_pos + 10, y_pos - 20))

        # Draw status: velocity & acceleration
        status = f"v: {state['velocity']:.1f}, a: {state['acceleration']:.1f}"
        status_text = font.render(status, True, (255, 255, 0))
        surface.blit(status_text, (x_pos + 160, y_pos + 20))
