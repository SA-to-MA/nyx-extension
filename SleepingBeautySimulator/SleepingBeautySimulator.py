import math
import time


class SleepingBeautySimulator:
    def __init__(self, sleeping_beauty, window, actions, time_step=1, max_time=math.inf):
        '''
        :param sleeping_beauty: Sleeping beauty object of current simulation
        :param window: Sleeping beauty window object to draw the simulation
        :param actions: list of actions and their timestamps
        :param time_step: current time step
        :param max_time: max time can operate
        '''
        self.sleeping_beauty = sleeping_beauty
        self.actions = actions
        self.time_step = time_step
        self.max_time = max_time
        self.total_time = 0
        self.window = window

    def run(self):
        """
        Runs the simulation over a series of actions and checks events and processes at each time step,
        executing actions based on a dictionary of timestamp:[actions].
        """
        print("Starting the simulation...")
        # Draw the initial state of the window
        self.window.draw()
        time.sleep(3)

        while self.total_time < self.max_time and not self.sleeping_beauty.awake:
            # Check if there are actions for the current timestamp
            if self.total_time in self.actions:
                for action in self.actions[self.total_time]:
                    self.execute_action(action)

            if not self.sleeping_beauty.awake:
                # Process continuous actions and trigger events based on conditions
                self.check_processes_and_events()

                # Increment time
                self.total_time += self.time_step

            # Draw changes in the window
            self.window.draw()

            # Allow time to pass so changes are visible
            time.sleep(1)

        # Wait a few seconds before closing the simulation
        time.sleep(5)
        print(
            f"Simulation complete. Sleeping Beauty is {'awake' if self.sleeping_beauty.awake else 'still asleep'} after {self.total_time} time units.")

    def execute_action(self, action):
        if action == "openwindow":
            self.sleeping_beauty.open_window()
        elif action == "closewindow":
            self.sleeping_beauty.close_window()
        elif action == "kiss":
            self.sleeping_beauty.kiss()

    def check_processes_and_events(self):
        """Checks all events and processes, and triggers them if their conditions are met."""
        # circuit, charge and voltage
        self.sleeping_beauty.make_circuit()
        self.sleeping_beauty.rouse_princess()
        self.sleeping_beauty.charge_capacitor(self.time_step)
        self.sleeping_beauty.voltage_available()
        # alarm enable or disable or ring
        self.sleeping_beauty.trigger_alarm()
        self.sleeping_beauty.ring(self.time_step)
        # breaking circuit or alarm if necessary
        self.sleeping_beauty.break_circuit()
        self.sleeping_beauty.disable_alarm()