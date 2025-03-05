import os
import pygame
import time
from VIS.MA_VIS.Agent import Agent
from VIS.MA_VIS.CarsSimulator.Car import Car


class CarAgent(Agent):
    def __init__(self, _name, _actions, car):
        super().__init__(_name, _actions)
        self.car = car

    def execute(self, action, objects, screen):
        """Executes an action on the Car object."""
        if action[0] == "accelerate":
            self.car.accelerate()
        elif action[0] == "decelerate":
            self.car.decelerate()
        elif action[0] == "stop":
            self.car.stop()
        # check processes
        self.car.moving()
        self.car.wind_resistance()
        self.car.engine_explode()
        self.car.stop()

class CarWindow:
    def __init__(self, screen, agents, car_pred):
        """
        Initialize the Car Simulation Window.

        Args:
            screen (pygame.Surface): The display screen for rendering.
            agents (dict): Dictionary of car agent objects.
        """
        self.screen = screen
        self.cars = self.initialize_cars(agents, car_pred)  # Now storing actual Car objects

        # Define car sizes
        self.car_width = 150
        self.car_height = 60

        # Get the absolute path of the current script
        base_path = os.path.dirname(os.path.abspath(__file__))
        resources_dir = os.path.join(base_path, "resources")

        # Load background road image
        self.background_image = pygame.image.load(os.path.join(resources_dir, "road.jpg"))
        self.background_image = pygame.transform.scale(self.background_image, screen.get_size())

        # Load car image
        self.car_image = pygame.image.load(os.path.join(resources_dir, "car.png"))
        self.car_image = pygame.transform.scale(self.car_image, (self.car_width, self.car_height))

        # initialize initial state
        # Set initial positions for cars
        self.positions = self.initialize_positions()

    def initialize_cars(self, agents, parsed_data):
        """
        Converts parsed PDDL initial state dictionary into Car objects.

        Args:
            parsed_data (dict): Parsed initial conditions from PDDL.

        Returns:
            dict: A dictionary of Car objects indexed by car name.
        """
        cars = {}

        for car_name, car_data in parsed_data.items():
            # Extract values with defaults
            running = car_data.get("running", False)
            engine_blown = car_data.get("engine_blown", False)
            transmission_fine = car_data.get("transmission_fine", False)
            d = car_data.get("d", 0.0)
            v = car_data.get("v", 0.0)
            a = car_data.get("a", 0.0)
            up_limit = car_data.get("up_limit", 10.0)
            down_limit = car_data.get("down_limit", -1.0)
            running_time = car_data.get("running_time", 0.0)

            # Create Car object
            cur_car = Car(
                running, engine_blown, transmission_fine, d, v, a, up_limit, down_limit, running_time
            )
            # create car agent for it
            cars[car_name] = CarAgent(car_name, agents[car_name].actions, cur_car)
        return cars

    def initialize_positions(self):
        """
        Initialize starting positions for each car.
        """
        screen_width, screen_height = self.screen.get_size()
        start_x = int(screen_width * 0.05)  # 5% from the left
        start_y = int(screen_height * 0.6)  # 60% from the top

        positions = {}
        for i, car_name in enumerate(self.cars.keys()):
            positions[car_name] = [start_x, start_y + i * 80]  # Stack cars vertically
        return positions

    def update_positions(self):
        """
        Updates car positions based on their distance traveled, but slows down the movement.
        """
        speed_factor = 10

        for car_name, car_agent in self.cars.items():
            car = car_agent.car  # Access the actual Car object

            if car.running:
                # Move the car **more slowly** based on its distance (`d`)
                self.positions[car_name][0] = int(50 + (car.d * 2) / speed_factor)

    def draw(self):
        """
        Draws all elements in the simulation.
        """
        # Clear screen and draw background
        self.screen.blit(self.background_image, (0, 0))

        for car_name, car_agent in self.cars.items():
            car = car_agent.car  # Extract actual Car object
            x, y = self.positions[car_name]

            # Draw car image
            self.screen.blit(self.car_image, (x, y))

            # Display car status
            font = pygame.font.SysFont(None, 24)
            label = font.render(f"{car_name} (v={car.v:.1f}, a={car.a:.1f})", True, (255, 255, 255))
            self.screen.blit(label, (x + 10, y - 20))

            # Display engine explosion if applicable
            if car.engine_blown:
                explosion_font = pygame.font.SysFont(None, 30)
                explosion_label = explosion_font.render("💥 Engine Blown!", True, (255, 0, 0))
                self.screen.blit(explosion_label, (x + 10, y - 50))

        pygame.display.flip()


class CarSimulator:
    def __init__(self, window, t_value=1):
        """
        Handles the simulation loop for multiple cars.
        """
        self.window = window
        self.t = t_value

    def run(self):
        """
        Runs the simulation, executing car processes and updating visuals in parallel.
        """
        print("Starting car simulation...")
        self.window.draw()
        running = True
        time.sleep(1)

        while running:
            running = False  # Assume no actions remain

            # **Step 1: Pop the next action for each car (simultaneously)**
            car_actions = {}  # Stores the current action for each car
            for car_name, car_agent in self.window.cars.items():
                # if car reached goals, continue
                if car_agent.car.goal_reached:
                    continue
                if car_agent.actions:  # Only pop if there are remaining actions
                    car_actions[car_name] = car_agent.actions.pop(0)

            # **Step 2: Execute all actions in parallel for t time steps**
            for _ in range(int(self.t)):
                for car_name, car_agent in self.window.cars.items():
                    car = car_agent.car  # Extract Car object

                    if car.running:
                        running = True  # Keep simulation running if at least one car is active

                        # Execute the previously popped action
                        if car_name in car_actions:
                            car_agent.execute(car_actions[car_name], {}, self.window.screen)

                self.window.update_positions()  # Move cars visually
                self.window.draw()  # Redraw screen
                time.sleep(1)  # Pause before next time step

        print("Simulation complete.")




