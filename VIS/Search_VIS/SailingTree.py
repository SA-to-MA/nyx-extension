import pygame
import os
import ast

GRID_SCALE = 30
OFFSET_X = 100
OFFSET_Y = 100

def parse_state(state_vars):
    parsed = {
        "boats": {},
        "people": {}
    }

    for key, val in state_vars.items():
        try:
            fact = ast.literal_eval(key)
            if fact[0] == "x" and len(fact) == 2:
                parsed["boats"].setdefault(fact[1], {})["x"] = int(val)
            elif fact[0] == "y" and len(fact) == 2:
                parsed["boats"].setdefault(fact[1], {})["y"] = int(val)
            elif fact[0] == "saved" and len(fact) == 2:
                # Any 'saved' key means the person exists; ignore value
                parsed["people"].setdefault(fact[1], {})
        except:
            continue
    return parsed

def safe_coords(x, y, screen_w, screen_h):
    screen_x = x * GRID_SCALE + OFFSET_X
    screen_y = -y * GRID_SCALE + screen_h - OFFSET_Y
    screen_x = min(max(10, screen_x), screen_w - 70)
    screen_y = min(max(10, screen_y), screen_h - 70)
    return screen_x, screen_y

def render_domain(node, surface, font, res_dir, width, height):
    state_vars = getattr(node.state, "state_vars", {})
    parsed_state = parse_state(state_vars)

    background = pygame.transform.scale(
        pygame.image.load(os.path.join(res_dir, "background.png")),
        (width, height)
    )
    boat_img = pygame.transform.scale(
        pygame.image.load(os.path.join(res_dir, "boat.png")),
        (60, 60)
    )
    person_img = pygame.transform.scale(
        pygame.image.load(os.path.join(res_dir, "man.png")),
        (40, 40)
    )

    surface.blit(background, (0, 0))

    # Draw boats
    for name, pos in parsed_state["boats"].items():
        if "x" not in pos or "y" not in pos:
            continue
        x, y = safe_coords(pos["x"], pos["y"], width, height)
        surface.blit(boat_img, (x, y))
        label = font.render(name, True, (255, 255, 255))
        surface.blit(label, (x + 5, y + 60))

    # Draw people even if they don't have x/y — just place them on left
    for i, (name, pos) in enumerate(parsed_state["people"].items()):
        # Synthesize positions for people on the left shore
        person_x = -5  # far left (negative logical coord)
        person_y = i * 3  # vertical spacing

        x, y = safe_coords(person_x, person_y, width, height)
        surface.blit(person_img, (x, y))
        label = font.render(name, True, (0, 0, 0))
        surface.blit(label, (x, y - 15))
