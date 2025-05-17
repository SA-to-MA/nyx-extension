import pygame
import time
import os
import random
from VIS.Agent import Agent

class MinecraftWindow:
    def __init__(self, screen, init_obj, agents_actions, functions, goals):
        self.screen = screen
        self.agents_actions = agents_actions

        self.inventory = functions
        self.trees = int(functions.pop('trees_in_map')) # int
        self.agents_state = init_obj # agents state
        self.goal = goals # goal state

        self.agent_icons = {}
        self.item_icons = {}
        self.block_size = 50
        self.margin = 20

        base_path = os.path.dirname(os.path.abspath(__file__))
        resources_dir = os.path.join(base_path, "resources")

        # draw background
        self.background = None
        bg_path = os.path.join(resources_dir, "background.jpg")
        if os.path.exists(bg_path):
            bg_img = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(bg_img, self.screen.get_size())

        # add items images
        for item in ["log", "plank", "stick", "sack", "tree_tap", "pogo_stick"]:
            image_path = os.path.join(resources_dir, f"{item}.png")
            if os.path.exists(image_path):
                img = pygame.image.load(image_path)
                self.item_icons[item] = pygame.transform.scale(img, (45, 45))

        # add trees image
        image_path = os.path.join(resources_dir, f"tree.png")
        img = pygame.image.load(image_path)
        self.item_icons['tree'] = pygame.transform.scale(img, (80, 80))

        # load random agents images
        agent_images_dir = os.path.join(resources_dir, "skins")
        agent_images_pool = []

        if os.path.exists(agent_images_dir):
            for filename in os.listdir(agent_images_dir):
                if filename.endswith(".png"):
                    path = os.path.join(agent_images_dir, filename)
                    # try to load image, if fails - print message and move on to next image
                    try:
                        img = pygame.image.load(path)
                        img = pygame.transform.scale(img, (40, 60))
                        agent_images_pool.append(img)
                    except Exception as e:
                        print(f"Failed to load {filename}: {e}")

        # set each agent with random image
        for agent in agents_actions.keys():
            if agent_images_pool:
                self.agent_icons[agent] = random.choice(agent_images_pool)
            else:
                # fallback if no images found
                surface = pygame.Surface((40, 60))
                surface.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
                self.agent_icons[agent] = surface

    def draw(self, actions_log=None):
        # draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        font = pygame.font.SysFont(None, 24)
        x = self.margin
        y = self.margin


        # Draw each agent
        for agent_name in self.agents_actions.keys():
            self.screen.blit(self.agent_icons[agent_name], (x, y))
            label = font.render(agent_name, True, (255, 255, 255))
            self.screen.blit(label, (x + 10, y - 20))

            # Draw the current action text if exists
            if actions_log and agent_name in actions_log and len(actions_log[agent_name]) > 0:
                action_text = actions_log[agent_name][0].replace("_", " ")
                action_label = font.render(f"{action_text}", True, (0, 0, 0))
                self.screen.blit(action_label, (x, y + 70))

            # Draw agent status (free/busy)
            agent_status = "Free" if self.agents_state.get(agent_name, False) else "Busy"
            status_color = (0, 255, 0) if agent_status == "Free" else (255, 0, 0)
            status_label = font.render(agent_status, True, status_color)
            self.screen.blit(status_label, (x, y + 95))

            x += 200

        # Reset x and move down to draw inventory
        x = self.margin
        y += 150

        # Draw shared inventory
        for item, count in self.inventory.items():
            img = self.item_icons.get(item.replace("count_", "").replace("_in_inventory", ""), None)
            if img:
                self.screen.blit(img, (x, y))
                count_label = font.render(str(count), True, (255, 255, 255))
                self.screen.blit(count_label, (x + 45, y + 10))
                y += 60

        # Draw individual trees
        ground_height = self.screen.get_height() / 3
        # Draw trees
        tree_icon = self.item_icons.get("tree", None)
        if tree_icon:
            tree_size = 80
            tree_spacing = 15
            start_x = self.margin * 3
            max_x = self.screen.get_width() - (self.margin*3)
            tree_y_start = self.screen.get_height() - ground_height - tree_size - 30  # Start right above grass

            tree_x = start_x
            tree_y = tree_y_start

            for i in range(self.trees):
                if tree_x + tree_size > max_x:
                    tree_x = start_x
                    tree_y += (tree_size + tree_spacing)  # Go one row up

                # Only draw if still visible
                if tree_y >= self.margin:
                    self.screen.blit(tree_icon, (tree_x, tree_y))
                    tree_x += (tree_size + tree_spacing)
                else:
                    break  # Stop drawing if we run out of vertical space

        # Draw goal
        goal_x = self.margin
        goal_y = self.screen.get_height() * 4/5

        title_label = font.render("Goal:", True, (255, 255, 255))
        self.screen.blit(title_label, (goal_x, goal_y))
        goal_y += 30  # Move down before listing items

        for key, value in self.goal.items():
            goal_text = f"{key.replace('_', ' ')}: {value}"
            goal_label = font.render(goal_text, True, (255, 255, 255))
            self.screen.blit(goal_label, (goal_x, goal_y))
            goal_y += 25

        pygame.display.flip()  # <--- Refresh screen!


class MinecraftAgent(Agent):
    def __init__(self, _name, _actions):
        super().__init__(_name, _actions)

    def execute(self, _action, agent_states, window):
        # if no action, continue
        if len(_action) == 0:
            return
        action_name = _action[0]
        agent_name = self.name
        inventory = window.inventory

        # ---- Simulate Action World Update ----
        if action_name == "get_log":
            if window.trees > 0:
                window.trees -= 1
                agent_states[agent_name] = False  # Agent now busy

        elif action_name == "return_log":
            inventory["count_log_in_inventory"] = inventory.get("count_log_in_inventory", 0) + 1
            agent_states[agent_name] = True  # Agent now free

        elif action_name == "craft_plank":
            if inventory.get("count_log_in_inventory", 0) >= 1:
                inventory["count_log_in_inventory"] -= 1
                agent_states[agent_name] = False

        elif action_name == "return_plank":
            inventory["count_planks_in_inventory"] = inventory.get("count_planks_in_inventory", 0) + 4
            agent_states[agent_name] = True

        elif action_name == "craft_stick":
            if inventory.get("count_planks_in_inventory", 0) >= 2:
                inventory["count_planks_in_inventory"] -= 2
                agent_states[agent_name] = False

        elif action_name == "return_stick":
            inventory["count_stick_in_inventory"] = inventory.get("count_stick_in_inventory", 0) + 4
            agent_states[agent_name] = True

        elif action_name == "craft_tree_tap":
            if (inventory.get("count_planks_in_inventory", 0) >= 5 and
                inventory.get("count_stick_in_inventory", 0) >= 1):
                inventory["count_planks_in_inventory"] -= 5
                inventory["count_stick_in_inventory"] -= 1
                agent_states[agent_name] = False

        elif action_name == "return_tree_tap":
            inventory["count_tree_tap_in_inventory"] = inventory.get("count_tree_tap_in_inventory", 0) + 1
            agent_states[agent_name] = True

        elif action_name == "place_tree_tap":
            if window.trees > 0 and inventory.get("count_tree_tap_in_inventory", 0) >= 1:
                inventory["count_tree_tap_in_inventory"] -= 1
                agent_states[agent_name] = False

        elif action_name == "return_sack":
            inventory["count_sack_polyisoprene_pellets_in_inventory"] = inventory.get("count_sack_polyisoprene_pellets_in_inventory", 0) + 1
            agent_states[agent_name] = True

        elif action_name == "craft_wooden_pogo":
            if (inventory.get("count_planks_in_inventory", 0) >= 2 and
                inventory.get("count_stick_in_inventory", 0) >= 4 and
                inventory.get("count_sack_polyisoprene_pellets_in_inventory", 0) >= 1):
                inventory["count_planks_in_inventory"] -= 2
                inventory["count_stick_in_inventory"] -= 4
                inventory["count_sack_polyisoprene_pellets_in_inventory"] -= 1
                agent_states[agent_name] = False

        elif action_name == "return_wooden_pogo":
            inventory["count_pogo_stick"] = inventory.get("count_pogo_stick", 0) + 1
            agent_states[agent_name] = True

        else:
            print(f"Unknown action: {action_name}")

        # ---- After World Update: Redraw the updated state ----
        window.draw()  # Immediately refresh screen after action


class MinecraftSimulator:
    def __init__(self, screen, agents_by_type, functions, init_state, goals, solution, t_value=1):
        self.window =  MinecraftWindow(screen, init_state, solution, functions, goals)                        # The visualization window
        self.agents = {}           # Correct: dict of agent_name -> MinecraftAgent instances
        for agent_name, actions in self.window.agents_actions.items():
            self.agents[agent_name] = MinecraftAgent(agent_name, actions)
        self.t = t_value                              # Time delay between steps (seconds)

    def run(self):
        print("Starting Minecraft simulation...")
        self.window.draw()  # Initial state
        running = True
        time.sleep(1)

        while running:
            running = False
            actions_log = {}

            for agent_name, agent in self.agents.items():
                if agent.actions:
                    running = True
                    action = agent.get_next_action()
                    print(f"[{agent.name}] Executing: {action}")

                    # Execute
                    agent.execute(action, self.window.agents_state, self.window)

                    # Log current action for visualization
                    actions_log[agent_name] = action

            self.window.draw(actions_log)  # Refresh final view after all agents
            time.sleep(self.t)

        print("Simulation complete.")
        time.sleep(2)
