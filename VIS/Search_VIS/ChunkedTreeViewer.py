import pickle
import os
import random
import pygame
import ast

# TODO: generic way for all domains
DOMAIN = "car"
# DOMAIN = "blocks"

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
    file_path = os.path.join(directory, filename)

    # Print file path and size for debugging
    print(f"📂 Trying to open file: {file_path}")
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

# TODO: implement visualization for state

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
    """Parses car state where conditions are in nested lists and extracts numeric and boolean values."""
    parsed_state = {
        "velocity": "Unknown",
        "acceleration": "Unknown",
        "distance": "Unknown",
        "engine_blown": False,
        "running": False,
        "transmission_fine": True,
        "goal_reached": False
    }

    for condition in state_vars:
        try:
            parsed_condition = ast.literal_eval(condition)  # Convert string to list
            if isinstance(parsed_condition, list) and len(parsed_condition) == 2:
                key, value = parsed_condition

                # Convert value to appropriate type
                if isinstance(value, str) and value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                elif isinstance(value, (int, float)):
                    value = float(value)

                if key in parsed_state:
                    parsed_state[key] = value
        except (ValueError, SyntaxError):
            continue  # Skip invalid entries

    return parsed_state

def random_color():
    """Generate a random RGB color."""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def show_node_info(node):
    """Generate an overlay with structured state information, keeping the table as the background."""

    info_width, info_height = WIDTH + 50, HEIGHT * 0.5
    info_surface = pygame.Surface((info_width, info_height))
    info_surface.fill((200, 200, 200))  # Default background in case image fails
    font = pygame.font.Font(None, 24)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESOURCES_DIR = os.path.join(BASE_DIR, "resources")

    if DOMAIN == "blocks":
        state_vars = getattr(node.state, "state_vars", [])
        parsed_state = parse_block_state(state_vars)

        # Load the table as the full background
        table_img = pygame.image.load(os.path.join(RESOURCES_DIR, "table.png"))
        table_img = pygame.transform.scale(table_img, (info_width, info_height))  # Full size background

        # Load the hand image
        hand_img = pygame.image.load(os.path.join(RESOURCES_DIR, "hand.png"))
        hand_img = pygame.transform.scale(hand_img, (80, 80))  # Adjust hand size

        # Set the table as the background
        info_surface.blit(table_img, (0, 0))

        block_positions = {}
        x_pos = 50
        y_pos = info_height - 120  # Blocks above the table

        # Position blocks on the table
        for block in parsed_state["ontable"]:
            block_positions[block] = (x_pos, y_pos)
            x_pos += 60  # Better spacing

        # Position stacked blocks
        for top, bottom in parsed_state["on"].items():
            if bottom in block_positions:
                block_positions[top] = (block_positions[bottom][0], block_positions[bottom][1] - 60)

        # Draw blocks
        for block, (x, y) in block_positions.items():
            pygame.draw.rect(info_surface, random_color(), (x, y, 50, 50))
            text_surface = font.render(block, True, (255, 255, 255))
            info_surface.blit(text_surface, (x + 10, y + 10))

        # Hand Placement Logic (Show All Agents)
        agents = []
        # Process holding agents
        if "holding" in parsed_state:
            for agent, held_block in parsed_state["holding"].items():  # Iterate over key-value pairs
                held_block = held_block.strip() if held_block != "False" else None
                agents.append((agent.strip(), held_block))  # Ensure clean formatting

        # Process hand-empty agents
        if "handempty" in parsed_state:
            for agent in parsed_state["handempty"]:  # Iterate over agents with empty hands
                agents.append((agent.strip(), None))  # Append agent with no block held

        # Show hands for every agent
        hand_x = 200  # Start position for agents
        for agent, held_block in agents:
            hand_y = 50  # Position hands at the top
            info_surface.blit(hand_img, (hand_x, hand_y))  # Place hand image
            text_surface = font.render(agent, True, (255, 255, 255))
            info_surface.blit(text_surface, (hand_x + 20, hand_y - 10))  # Label the agent

            if held_block:
                pygame.draw.rect(info_surface, random_color(), (hand_x + 10, hand_y + 40, 40, 40))  # Draw block
                text_surface = font.render(held_block, True, (255, 255, 255))
                info_surface.blit(text_surface, (hand_x + 20, hand_y + 50))

            hand_x += 100  # Space hands evenly

    return info_surface  # Return the surface to be drawn


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


def main():
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
    main()