import pygame
import time
import os
from VIS.Agent import Agent

class SailingWindow:
    def __init__(self, screen, agents_by_type, init_state, solution):
        self.screen = screen
        self.boats = {}
        self.people = {}
        self.solution = solution
        self.load_images()
        self.initializeObjects(agents_by_type, init_state, solution)

    def load_images(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        res_dir = os.path.join(base_path, "resources")
        self.boat_image = pygame.transform.scale(
            pygame.image.load(os.path.join(res_dir, "boat.png")), (80, 80))
        self.person_image = pygame.transform.scale(
            pygame.image.load(os.path.join(res_dir, "man.png")), (50, 50))
        self.background_image = pygame.transform.scale(
        pygame.image.load(os.path.join(res_dir, "background.png")),
        self.screen.get_size())

    def initializeObjects(self, agents_by_type, init_state, solution):
        # Initialize boats
        for name in agents_by_type["boat"]:
            x = init_state[name]["x"]
            y = init_state[name]["y"]
            self.boats[name] = SailingAgent(name, solution[name], x, y)

        # Use the first available boat as reference for positioning people
        first_boat = next(iter(agents_by_type["boat"]))
        boat_x = init_state[first_boat]["x"]
        boat_y = init_state[first_boat]["y"]

        # Initialize people
        for i, (name, props) in enumerate(init_state.items()):
            if name not in agents_by_type["boat"]:
                d = props["d"]
                self.people[name] = Person(name, d, boat_x, boat_y, i)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        font = pygame.font.SysFont(None, 20)

        # Draw people
        for person in self.people.values():
            px, py = person.get_pos()
            self.screen.blit(self.person_image, (px, py))
            label = font.render(person.name, True, (0, 0, 0))
            self.screen.blit(label, (px, py - 15))

        # Draw boats
        for boat in self.boats.values():
            bx, by = boat.get_pos()
            self.screen.blit(self.boat_image, (bx, by))
            label = font.render(boat.name, True, (255, 255, 255))
            self.screen.blit(label, (bx + 5, by + 60))

        pygame.display.flip()


class SailingAgent(Agent):
    def __init__(self, name, actions, x, y):
        super().__init__(name, actions)
        self.x = x * 10 + 400  # adjust for screen scale
        self.y = -y * 10 + 300

    def get_pos(self):
        return self.x, self.y

    def execute(self, action, agent_states, window):
        if not action:
            return
        name, args = action[0], action[1]

        GRID_SCALE = 10

        # ואז:
        if name == "go-north-east":
            self.x += 1.5 * GRID_SCALE
            self.y -= 1.5 * GRID_SCALE
        elif name == "go-north-west":
            self.x -= 1.5 * GRID_SCALE
            self.y -= 1.5 * GRID_SCALE
        elif name == "go-east":
            self.x += 3 * GRID_SCALE
        elif name == "go-west":
            self.x -= 3 * GRID_SCALE
        elif name == "go-south-west":
            self.x += 2 * GRID_SCALE
            self.y += 2 * GRID_SCALE
        elif name == "go-south-east":
            self.x -= 2 * GRID_SCALE
            self.y += 2 * GRID_SCALE
        elif name == "go-south":
            self.y += 2 * GRID_SCALE


class Person:
    def __init__(self, name, d, boat_x, boat_y, index=0):
        self.name = name
        self.d = d
        self.saved = False

        logical_x = index * 2
        logical_y = d

        GRID_SCALE = 10

        self.x = (boat_x - logical_x) * GRID_SCALE + 400
        self.y = (boat_y + logical_y) * -GRID_SCALE + 300

        if self.y < 30:
            self.y = 30

    def get_pos(self):
        return self.x, self.y


class SailingSimulator:
    def __init__(self, screen, agents_by_type, init_state, solution, t_value):
        self.window = SailingWindow(screen, agents_by_type, init_state, solution)
        self.t = t_value

    def run(self):
        print("Starting sailing simulation...")
        self.window.draw()
        running = True
        time.sleep(1)
        while running:
            running = False
            for agent in self.window.boats.values():
                if agent.actions:
                    running = True
                    action = agent.actions.pop(0)
                    agent.execute(action, "", "")
                    self.window.draw()
            time.sleep(self.t)
        print("Sailing simulation complete.")
