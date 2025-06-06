import pygame
import os
import ast
import syntax.constants as constants

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

    # Draw people based on d constant (relative distance)
    for i, key in enumerate(sorted(constants.state_constants)):
        if key.startswith("['d', '"):
            person = key.split(",")[1].strip().strip("']").strip("'")
            d = constants.state_constants[key]

            # Display person horizontally from the left, and vertically based on d
            # This is for clear illustration only
            person_x = GRID_SCALE + OFFSET_X * (i+1)  # space them horizontally
            person_y = height // 2 + int(d * 0.2)  # vertical placement from center
            # Ensure they're within screen bounds
            person_x = max(10, min(person_x, width - 70))
            person_y = max(10, min(person_y, height - 70))

            surface.blit(person_img, (person_x, person_y))
            label = font.render(person, True, (255, 255, 255))
            surface.blit(label, (person_x + 5, person_y + 40))
