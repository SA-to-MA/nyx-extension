import pygame
import time
import os
import random
from VIS.MA_VIS.Agent import Agent

class MinecraftWindow:
    def __init__(self, screen,init_obj, agent_data):
        self.screen = screen
        self.agents_actions = agent_data

        self.inventory = init_obj[0]
        self.trees = init_obj[1]['trees_in_map'] # int
        self.agents_state = init_obj[2] # free or not
        self.goal = init_obj[3] # goal state

        self.agent_icons = {}
        self.item_icons = {}
        self.block_size = 50
        self.margin = 20

        base_path = os.path.dirname(os.path.abspath(__file__))
        resources_dir = os.path.join(base_path, "resources")

        for item in ["log", "plank", "stick", "sack", "tree_tap", "pogo_stick"]:
            image_path = os.path.join(resources_dir, f"{item}.png")
            if os.path.exists(image_path):
                img = pygame.image.load(image_path)
                self.item_icons[item] = pygame.transform.scale(img, (40, 40))

        for agent in agent_data.keys():
            self.agent_icons[agent] = pygame.Surface((40, 40))
            self.agent_icons[agent].fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))

    def draw(self, actions_log=None):
        self.screen.fill((0, 0, 0))  # Clear screen
        font = pygame.font.SysFont(None, 24)
        x = self.margin
        y = self.margin

        # Draw each agent
        for agent_name in self.agents_actions.keys():
            self.screen.blit(self.agent_icons[agent_name], (x, y))
            label = font.render(agent_name, True, (255, 255, 255))
            self.screen.blit(label, (x, y - 20))

            # Draw the current action text if exists
            if actions_log and agent_name in actions_log:
                action_label = font.render(f"Action: {actions_log[agent_name][0]}", True, (255, 215, 0))
                self.screen.blit(action_label, (x, y + 50))

            # Draw agent status (free/busy)
            agent_status = "Free" if self.agents_state.get(agent_name, False) else "Busy"
            status_color = (0, 255, 0) if agent_status == "Free" else (255, 0, 0)
            status_label = font.render(agent_status, True, status_color)
            self.screen.blit(status_label, (x, y + 80))

            x += 150

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

        # Draw trees counter
        trees_label = font.render(f"Trees left: {self.trees}", True, (0, 200, 0))
        self.screen.blit(trees_label, (self.margin, y + 30))

        # Draw goal (optional)
        goal_label = font.render(f"Goal: {self.goal}", True, (255, 215, 0))
        self.screen.blit(goal_label, (self.margin, y + 70))

        pygame.display.flip()  # <--- Refresh screen!


class MinecraftAgent(Agent):
    def __init__(self, _name, _actions):
        super().__init__(_name, _actions)

    def execute(self, _action, agent_states, window):
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
        time.sleep(0.3)  # Small pause to visualize the change


class MinecraftSimulator:
    def __init__(self, window, t_value=1):
        self.window = window                         # The visualization window
        self.agents = {}           # Correct: dict of agent_name -> MinecraftAgent instances
        for agent_name, agent in window.agents_actions.items():
            self.agents[agent_name] = MinecraftAgent(agent_name, agent.actions)
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

                    # Redraw immediately showing this action
                    self.window.draw(actions_log)
                    time.sleep(0.5)  # small pause after each agent acts

            self.window.draw()  # Refresh final view after all agents
            time.sleep(self.t)

        print("Simulation complete.")
