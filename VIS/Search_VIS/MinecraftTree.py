import os
import random
import pygame


def parse_state(state_vars):
    parsed_state = {
        "agents": {},  # agent current action
        "trees": 0,  # trees on map
        "inventory": {
            "log": 0,
            "plank": 0,
            "stick": 0,
            "sack": 0,
            "tree_tap": 0,
            "pogo_stick": 0
        }
    }
    for key, val in state_vars.items():
        if not val:
            continue  # Skip if value is False or 0
        try:
            # Clean the key string
            if isinstance(key, str):
                clean_key = key.strip().replace('"', "").replace("'", "").replace("[", "").replace("]", "")
                parts = clean_key.split(",")  # Split the parts inside the brackets

                predicate = parts[0].strip()
                agent = parts[1].strip() if len(parts) > 1 else None

                # Agents handling
                if predicate.startswith("agent_") and agent:
                    parsed_state["agents"][agent] = predicate.replace("agent_", "").replace("_", " ").capitalize()

                # Trees in map
                elif predicate == "trees_in_map":
                    parsed_state["trees"] = val

                # Inventory items
                elif predicate.startswith("count_"):
                    item_name = predicate.replace("count_", "").replace("_in_inventory", "").lower()
                    if item_name in parsed_state["inventory"]:
                        parsed_state["inventory"][item_name] = val

        except Exception as e:
            print(f"Error parsing {key}: {e}")
            continue

    return parsed_state

def render_domain(node, surface, font, res_dir, width, height):
    state_vars = getattr(node.state, "state_vars", [])
    parsed_state = parse_state(state_vars)

    background = pygame.image.load(os.path.join(res_dir, "background.jpg"))
    background = pygame.transform.scale(background, (width, height))
    surface.blit(background, (0, 0))

    # Load item icons
    item_icons = {}
    for item in ["log", "plank", "stick", "sack", "tree_tap", "pogo_stick", "tree"]:
        img_path = os.path.join(res_dir, f"{item}.png")
        if os.path.exists(img_path):
            img = pygame.image.load(img_path)
            if item == "tree":
                item_icons[item] = pygame.transform.scale(img, (30, 30))  # Make trees smaller
            else:
                item_icons[item] = pygame.transform.scale(img, (40, 40))

    # Load random agent images
    agent_images_pool = []
    agent_images_dir = os.path.join(res_dir, "skins")

    if os.path.exists(agent_images_dir):
        for filename in os.listdir(agent_images_dir):
            if filename.endswith(".png"):
                path = os.path.join(agent_images_dir, filename)
                try:
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img, (40, 60))  # 40x60 like your original
                    agent_images_pool.append(img)
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")

    # Assign agent images randomly
    agent_icons = {}
    for agent_name in parsed_state["agents"].keys():
        if agent_images_pool:
            agent_icons[agent_name] = random.choice(agent_images_pool)
        else:
            surface_fallback = pygame.Surface((40, 60))
            surface_fallback.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
            agent_icons[agent_name] = surface_fallback

    # Draw agents closer together
    margin = 20
    agent_spacing = 100  # tighter spacing between agents
    x = margin
    y = margin

    for agent_name, action in parsed_state["agents"].items():
        agent_surface = agent_icons.get(agent_name)
        if agent_surface:
            surface.blit(agent_surface, (x, y))

        # Agent name
        name_label = font.render(agent_name, True, (0, 0, 0))
        surface.blit(name_label, (x + 5, y - 20))

        # Action text (above Free status)
        action_text = action.replace("_", " ").capitalize()
        action_label = font.render(action_text, True, (0, 0, 0))
        surface.blit(action_label, (x, y + 65))

        x += agent_spacing

    # Move down to draw inventory in one horizontal line
    inv_start_x = margin
    inv_start_y = y + 140
    x = inv_start_x
    y = inv_start_y

    for item, count in parsed_state["inventory"].items():
        img = item_icons.get(item, None)
        if img:
            surface.blit(img, (x, y))
            count_label = font.render(str(int(count)), True, (0, 0, 0))
            surface.blit(count_label, (x + 45, y + 10))
            x += 70  # next item to the right

    # Move down to draw trees
    tree_icon = item_icons.get("tree", None)
    if tree_icon:
        x = margin
        y += 80  # small gap below inventory

        tree_spacing = 35
        max_x = width - margin
        for i in range(int(parsed_state["trees"])):
            if x + 30 > max_x:
                x = margin
                y += 40  # New line for trees

            surface.blit(tree_icon, (x, y))
            x += tree_spacing

