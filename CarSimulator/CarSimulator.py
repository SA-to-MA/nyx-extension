import time
import math


class CarSimulator:
    def __init__(self, car, window, actions, time_step=1, max_time=math.inf):
        """
        :param car: Car object to simulate
        :param window: Window object to draw the simulation
        :param actions: List of actions and their timestamps (e.g., [(0, 'start'), (5, 'accelerate')])
        :param time_step: Simulation time step in seconds
        :param max_time: Maximum simulation time
        """
        self.car = car
        self.actions = actions
        self.time_step = time_step
        self.max_time = max_time
        self.total_time = 0
        self.window = window

    def run(self):
        """
        Runs the simulation over a series of actions and checks events and processes at each time step.
        """
        print("Starting the simulation...")
        self.window.draw()  # Draw initial state
        action_index = 0
        action_count = len(self.actions)

        while self.total_time < self.max_time and not self.car.goal_reached:
            # Check if it's time to execute the next action
            if action_index < action_count:
                action_time, action = self.actions[action_index]
                if self.total_time >= action_time:
                    self.execute_action(action)
                    action_index += 1

            if not self.car.goal_reached:
                # Process continuous actions and trigger events
                self.check_processes_and_events()
                self.total_time += self.time_step

            # Draw changes in the window
            self.window.draw()
            # allow time to pass so changes are visible
            time.sleep(1)

        # Wait a few seconds before closing the simulation
        time.sleep(5)
        print(f"Simulation complete. Car {'reached the goal' if self.car.goal_reached else 'did not reach the goal'} after {self.total_time} time units.")

    def execute_action(self, action):
        """
        Executes a specific action on the car.
        :param action: Action name as a string
        """
        if action == "start":
            self.car.start()
        elif action == "accelerate":
            self.car.accelerate()
        elif action == "decelerate":
            self.car.decelerate()
        elif action == "stop":
            self.car.stop()

    def check_processes_and_events(self):
        """
        Checks and triggers processes and events for the car.
        """
        # Processes
        self.car.moving(self.time_step)
        self.car.wind_resistance(self.time_step)
        # Events
        self.car.engine_explode()
