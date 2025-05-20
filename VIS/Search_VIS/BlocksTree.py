import random
import ast
import pygame
import os

def random_color():
    """Generate a random RGB color."""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def parse_state(state_vars):
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

def render_domain(node, surface, font, res_dir, width, height):
    import ast

    state_vars = getattr(node.state, "state_vars", [])
    parsed_state = parse_state(state_vars)

    table_img = pygame.image.load(os.path.join(res_dir, "table.png"))
    table_img = pygame.transform.scale(table_img, (width, height))
    surface.blit(table_img, (0, 0))

    hand_img = pygame.image.load(os.path.join(res_dir, "hand.png"))
    hand_img = pygame.transform.scale(hand_img, (80, 80))

    block_positions = {}
    drawn_blocks = set()
    x_pos = 40
    y_pos = height - 120

    # Step 1: Place blocks on table
    for block in parsed_state.get("ontable", []):
        block_positions[block] = (x_pos, y_pos)
        x_pos += 60

    # Step 2: Place blocks on top of other blocks
    for top, bottom in parsed_state.get("on", {}).items():
        if bottom in block_positions:
            bx, by = block_positions[bottom]
            block_positions[top] = (bx, by - 40)

    # Step 3: Agent hands
    agents = []
    for agent, held_block in parsed_state.get("holding", {}).items():
        held_block = held_block.strip() if held_block != "False" else None
        agents.append((agent.strip(), held_block))

    for agent in parsed_state.get("handempty", []):
        agents.append((agent.strip(), None))

    # Step 4: Draw blocks that were placed
    for block, (x, y) in block_positions.items():
        pygame.draw.rect(surface, random_color(), (x, y, 40, 40))
        text_surface = font.render(block, True, (255, 255, 255))
        surface.blit(text_surface, (x + 10, y + 10))
        drawn_blocks.add(block)

    # Step 5: Draw agent hands and held blocks
    hand_x = 200
    for agent, held_block in agents:
        hand_y = 50
        surface.blit(hand_img, (hand_x, hand_y))
        text_surface = font.render(agent, True, (255, 255, 255))
        surface.blit(text_surface, (hand_x + 20, hand_y - 10))

        if held_block and held_block not in drawn_blocks:
            pygame.draw.rect(surface, random_color(), (hand_x + 10, hand_y + 40, 40, 40))
            text_surface = font.render(held_block, True, (255, 255, 255))
            surface.blit(text_surface, (hand_x + 20, hand_y + 50))
            drawn_blocks.add(held_block)

        hand_x += 100

    # Step 6: Ensure missing blocks are drawn on the side (fallback)
    all_blocks = set()
    for key in state_vars:
        try:
            parsed = ast.literal_eval(key)
            if isinstance(parsed, list):
                for item in parsed[1:]:
                    if isinstance(item, str) and len(item) == 1 and item.isalpha():
                        all_blocks.add(item)
        except:
            continue

    all_blocks.update(parsed_state.get("holding", {}).values())

    for block in all_blocks:
        if block not in drawn_blocks:
            block_positions[block] = (x_pos, y_pos)
            pygame.draw.rect(surface, random_color(), (x_pos, y_pos, 40, 40))
            text_surface = font.render(block, True, (255, 255, 255))
            surface.blit(text_surface, (x_pos + 10, y_pos + 10))
            x_pos += 60
