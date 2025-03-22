import pickle
import os
import random
import pygame
import ast

# TODO: leave empty
DOMAIN = ""

# Constants
pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
WIDTH, HEIGHT = int(SCREEN_WIDTH * 0.9), int(SCREEN_HEIGHT * 0.9)
NODE_RADIUS = 25
BACKGROUND_COLOR = (255, 255, 255)
NODE_COLOR = (173, 216, 230)
EDGE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 165, 0)
FONT_SIZE = 16
CHUNK_SIZE = 100  # Increase chunk size to 100 nodes

directory = "search_tree"
parent_references = {}  # Stores references for all parent-child relationships across chunks


def get_chunk_files():
    """Retrieve and sort the chunk files."""
    files = [f for f in os.listdir(directory) if f.startswith("tree_chunk_") and f.endswith(".pkl")]
    return sorted(files, key=lambda x: int(x.split("_")[-1].split(".")[0]))


def preload_parent_references():
    """Load all parent-child relationships across chunks to track missing parents."""
    global parent_references
    chunks = get_chunk_files()
    for chunk_file in chunks:
        nodes = load_chunk(chunk_file)
        for node in nodes:
            if node.parent:
                parent_references[node] = node.parent


def load_chunk(filename):
    """Load a specific chunk."""
    with open(os.path.join(directory, filename), "rb") as file:
        return pickle.load(file)


def compute_node_positions(nodes):
    """Compute positions for nodes and track missing parents."""
    levels = {}
    node_positions = {}
    missing_parents = {}  # Store missing parent references

    if not nodes:
        return node_positions, missing_parents

    for idx, node in enumerate(nodes):
        depth = node.state.depth if hasattr(node.state, "depth") else 0
        if depth not in levels:
            levels[depth] = []
        levels[depth].append((idx, node))

    max_depth = max(levels.keys()) if levels else 1
    y_spacing = HEIGHT // (max_depth + 2)

    for depth, level_nodes in levels.items():
        x_spacing = WIDTH // (len(level_nodes) + 2)
        for i, (idx, node) in enumerate(level_nodes):
            x = (i + 1) * x_spacing
            y = (depth + 1) * y_spacing
            node_positions[node] = (x, y, idx)

    for node in nodes:
        if node.parent and node.parent not in node_positions:
            missing_parents[node] = parent_references.get(node, None)

    return node_positions, missing_parents


def parse_block_state(state_vars):
    """Parses block state where conditions are in nested lists and extracts only TRUE conditions."""
    parsed_state = {
        "on": {},  # Block relationships (e.g., 'a' is on 'b')
        "ontable": [],  # Blocks directly on the table
        "holding": {},  # The block currently being held
        "handempty": [],  # agents with empty hand
    }

    for action, val in state_vars.items():
        if not val:
            continue
        try:
            parsed_condition = ast.literal_eval(action)  # Convert string to list
            if isinstance(parsed_condition, list) and len(parsed_condition) > 1:
                key = parsed_condition  # Everything except the last part

                if isinstance(val, bool) and val:  # Keep only True conditions
                    if key[0] == "on" and len(key) == 3:
                        _, top, bottom = key
                        parsed_state["on"][top] = bottom
                    elif key[0] == "ontable" and len(key) == 2:
                        parsed_state["ontable"].append(key[1])
                    elif key[0] == "holding" and len(key) == 3:
                        _, agent, block = key
                        parsed_state["holding"][agent] = block
                    elif key[0] == "handempty":
                        parsed_state["handempty"].append(key[1])
        except (ValueError, SyntaxError):
            continue  # Skip invalid entries

    return parsed_state


def parse_car_state(state_vars):
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

def random_color():
    """Generate a random RGB color."""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def show_node_info(node):
    """Generate an overlay with structured state information, keeping the table as the background."""

    info_width, info_height = WIDTH + 25, HEIGHT * 0.3
    info_surface = pygame.Surface((info_width, info_height))
    info_surface.fill((200, 200, 200))  # Default background in case image fails
    font = pygame.font.Font(None, 24)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESOURCES_DIR = os.path.join(BASE_DIR, "resources")

    if DOMAIN == "blocks":
        render_blocks_domain(node, info_surface, font, RESOURCES_DIR, info_width, info_height)
    elif DOMAIN == "car":
        render_car_domain(node, info_surface, font, RESOURCES_DIR, info_width, info_height)

    return info_surface  # Return the surface to be drawn

def render_car_domain(node, surface, font, res_dir, width, height):
    # Load images
    road_img = pygame.image.load(os.path.join(res_dir, "road-2.jpg"))
    road_img = pygame.transform.scale(road_img, (width, height))
    car_img = pygame.image.load(os.path.join(res_dir, "car.png"))
    car_img = pygame.transform.scale(car_img, (150, 60))

    surface.blit(road_img, (0, 0))  # draw background

    # Parse the car states for all agents
    state_vars = getattr(node.state, "state_vars", [])
    car_states = parse_car_state(state_vars)

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


def render_blocks_domain(node, surface, font, res_dir, width, height):
    state_vars = getattr(node.state, "state_vars", [])
    parsed_state = parse_block_state(state_vars)

    table_img = pygame.image.load(os.path.join(res_dir, "table.png"))
    table_img = pygame.transform.scale(table_img, (width, height))
    surface.blit(table_img, (0, 0))

    hand_img = pygame.image.load(os.path.join(res_dir, "hand.png"))
    hand_img = pygame.transform.scale(hand_img, (80, 80))

    block_positions = {}
    x_pos = 40
    y_pos = height - 120

    for block in parsed_state.get("ontable", []):
        block_positions[block] = (x_pos, y_pos)
        x_pos += 60

    for top, bottom in parsed_state.get("on", {}).items():
        if bottom in block_positions:
            block_positions[top] = (block_positions[bottom][0], block_positions[bottom][1] - 40)

    for block, (x, y) in block_positions.items():
        pygame.draw.rect(surface, random_color(), (x, y, 40, 40))
        text_surface = font.render(block, True, (255, 255, 255))
        surface.blit(text_surface, (x + 10, y + 10))

    # Agent hands logic
    agents = []
    for agent, held_block in parsed_state.get("holding", {}).items():
        held_block = held_block.strip() if held_block != "False" else None
        agents.append((agent.strip(), held_block))

    for agent in parsed_state.get("handempty", []):
        agents.append((agent.strip(), None))

    hand_x = 200
    for agent, held_block in agents:
        hand_y = 50
        surface.blit(hand_img, (hand_x, hand_y))
        text_surface = font.render(agent, True, (255, 255, 255))
        surface.blit(text_surface, (hand_x + 20, hand_y - 10))

        if held_block:
            pygame.draw.rect(surface, random_color(), (hand_x + 10, hand_y + 40, 40, 40))
            text_surface = font.render(held_block, True, (255, 255, 255))
            surface.blit(text_surface, (hand_x + 20, hand_y + 50))

        hand_x += 100


def draw_buttons(screen):
    font = pygame.font.Font(None, 24)
    next_button = pygame.Rect(WIDTH - 120, HEIGHT - 50, 100, 40)
    back_button = pygame.Rect(WIDTH - 240, HEIGHT - 50, 100, 40)
    pygame.draw.rect(screen, (200, 200, 200), next_button)
    pygame.draw.rect(screen, (200, 200, 200), back_button)
    screen.blit(font.render("Next", True, (0, 0, 0)), (WIDTH - 95, HEIGHT - 40))
    screen.blit(font.render("Back", True, (0, 0, 0)), (WIDTH - 215, HEIGHT - 40))
    return next_button, back_button


def draw_tree(screen, nodes, selected_node, node_positions, missing_parents):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, FONT_SIZE)

    for node, (x, y, idx) in node_positions.items():
        if node.parent and node.parent in node_positions:
            parent_x, parent_y, _ = node_positions[node.parent]
            pygame.draw.line(screen, EDGE_COLOR, (x, y - NODE_RADIUS), (parent_x, parent_y + NODE_RADIUS), 2)
        elif node in missing_parents and missing_parents[node] is not None:
            pygame.draw.line(screen, EDGE_COLOR, (x, y - NODE_RADIUS), (x, 50), 2)  # Placeholder for external parent

    for node, (x, y, idx) in node_positions.items():
        color = SELECTED_COLOR if node == selected_node else NODE_COLOR
        pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(screen, EDGE_COLOR, (x, y), NODE_RADIUS, 2)
        text = font.render(str(idx), True, TEXT_COLOR)
        screen.blit(text, (x - NODE_RADIUS // 2, y - NODE_RADIUS // 2))


def main(domain_name):
    global DOMAIN
    DOMAIN = domain_name
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Search Tree Viewer")
    clock = pygame.time.Clock()

    preload_parent_references()  # Load all parent relationships
    chunks = get_chunk_files()
    if not chunks:
        print("No chunks found.")
        return

    current_chunk_index = 0
    nodes = load_chunk(chunks[current_chunk_index])[:CHUNK_SIZE]  # Load up to CHUNK_SIZE nodes
    node_positions, missing_parents = compute_node_positions(nodes)
    selected_node = None
    node_info_surface = None  # Holds the state info overlay
    state_window_position = (WIDTH - 520, 50)  # Move state overlay to the right

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_tree(screen, nodes, selected_node, node_positions, missing_parents)
        next_button, back_button = draw_buttons(screen)

        # If a node is selected, display its info at the correct position
        if selected_node:
            if node_info_surface is None:
                node_info_surface = show_node_info(selected_node)  # Generate info overlay
            screen.blit(node_info_surface, state_window_position)  # Draw overlay at correct position

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if next_button.collidepoint(mx, my) and current_chunk_index < len(chunks) - 1:
                    current_chunk_index += 1
                    nodes = load_chunk(chunks[current_chunk_index])[:CHUNK_SIZE]
                    node_positions, missing_parents = compute_node_positions(nodes)
                    selected_node = None
                    node_info_surface = None  # Reset state window
                elif back_button.collidepoint(mx, my) and current_chunk_index > 0:
                    current_chunk_index -= 1
                    nodes = load_chunk(chunks[current_chunk_index])[:CHUNK_SIZE]
                    node_positions, missing_parents = compute_node_positions(nodes)
                    selected_node = None
                    node_info_surface = None  # Reset state window
                else:
                    for node, (x, y, idx) in node_positions.items():
                        if (x - mx) ** 2 + (y - my) ** 2 <= NODE_RADIUS ** 2:
                            selected_node = node
                            node_info_surface = show_node_info(selected_node)  # Generate new overlay
                            break

        clock.tick(30)

    pygame.quit()



if __name__ == "__main__":
    main("blocks")