import pygame
import time
import os
import random
from VIS.MA_VIS.Agent import Agent

class MinecraftWindow:
    def __init__(self, screen, agent_data):
        self.screen = screen
        self.agents = agent_data
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

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear to black background
        font = pygame.font.SysFont(None, 24)
        x = self.margin
        y = self.margin

        for agent in self.agents:
            inv = agent.inventory

            self.screen.blit(self.agent_icons[agent.name], (x, y))
            label = font.render(agent.name, True, (255, 255, 255))
            self.screen.blit(label, (x, y - 20))

            item_y = y + 50
            for item, count in inv.items():
                if item == "free":
                    continue
                img = self.item_icons.get(item.replace("count_", "").replace("_in_inventory", ""), None)
                if img:
                    self.screen.blit(img, (x, item_y))
                    count_label = font.render(str(count), True, (255, 255, 255))
                    self.screen.blit(count_label, (x + 45, item_y + 10))
                    item_y += 50

            x += 150

        pygame.display.flip()


class MinecraftAgent(Agent):
    def __init__(self, _name, _actions, inventory=None):
        super().__init__(_name, _actions)
        self.inventory = inventory or {}

    def execute(self, _action, objects, screen):
        action_name = _action[0]

        if action_name == "get_log":
            self.inventory["count_log_in_inventory"] = self.inventory.get("count_log_in_inventory", 0) + 1

        elif action_name == "craft_plank":
            if self.inventory.get("count_log_in_inventory", 0) >= 1:
                self.inventory["count_log_in_inventory"] -= 1
                self.inventory["count_planks_in_inventory"] = self.inventory.get("count_planks_in_inventory", 0) + 4

        elif action_name == "craft_stick":
            if self.inventory.get("count_planks_in_inventory", 0) >= 2:
                self.inventory["count_planks_in_inventory"] -= 2
                self.inventory["count_stick_in_inventory"] = self.inventory.get("count_stick_in_inventory", 0) + 4

        elif action_name == "craft_tree_tap":
            self.inventory["count_tree_tap_in_inventory"] += 1

        elif action_name == "place_tree_tap":
            if self.inventory.get("count_tree_tap_in_inventory", 0) >= 1:
                self.inventory["count_tree_tap_in_inventory"] -= 1

        elif action_name in {"return_log", "return_plank", "return_stick", "return_tree_tap", "return_sack","return_wooden_pogo"}:
            item = "count_" + action_name.replace("return_", "") + "_in_inventory"
            self.inventory[item] += 1

        elif action_name in {"craft_wooden_pogo", "craft_pogo_stick"}:

            if self.inventory.get("count_stick_in_inventory", 0) >= 2 and self.inventory.get("count_sack_polyisoprene_pellets_in_inventory", 0) >= 1:
                self.inventory["count_stick_in_inventory"] -= 2
                self.inventory["count_sack_polyisoprene_pellets_in_inventory"] -= 1
                self.inventory["count_pogo_stick"] += 1


class MinecraftSimulator:
    def __init__(self, window, t_value=1):
        self.window = window                      # The visualization window
        self.agents = window.agents                 # Dict of MinecraftAgent instances
        self.t = t_value                          # Time delay between steps (seconds)
        self.shared_state = {}                    # You can pass global env or trees here

    def run(self):
        print("Starting Minecraft simulation...")
        self.window.draw()  # Initial state
        running = True
        time.sleep(1)

        while running:
            running = False

            for agent_name, agent in self.agents.items():
                if agent.actions:
                    running = True
                    action = agent.get_next_action()
                    print(f"[{agent.name}] Executing: {action}")
                    agent.execute(action, self.shared_state, self.window.screen)

            self.window.draw()
            time.sleep(self.t)

        print("Simulation complete.")
