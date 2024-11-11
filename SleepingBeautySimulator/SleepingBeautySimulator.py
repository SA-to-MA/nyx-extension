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
        Runs the simulation over a series of actions and checks events and processes at each time step.
        """
        print("Starting the simulation...")
        # draw window in initial state
        self.window.draw()
        time.sleep(2)
        action_index = 0
        action_count = len(self.actions)
        while self.total_time < self.max_time and not self.sleeping_beauty.awake:
            # Check if it's time to execute the next action
            if action_index < action_count:
                action_time, current_action = self.actions[action_index]
                if self.total_time >= action_time:
                    self.execute_action(current_action)
                    action_index += 1

            if not self.sleeping_beauty.awake:
                # Process continuous actions
                self.check_processes()
                # Trigger events based on conditions
                self.check_events()
                # Increment time
                self.total_time += self.time_step

            # draw changes in window
            self.window.draw()
            # allow time to pass so changes are visible
            time.sleep(2)

        print(f"Simulation complete. Sleeping Beauty is {'awake' if self.sleeping_beauty.awake else 'still asleep'} after {self.total_time} time units.")

    def execute_action(self, action):
        if action == "openwindow":
            self.sleeping_beauty.open_window()
        elif action == "closewindow":
            self.sleeping_beauty.close_window()
        elif action == "kiss":
            self.sleeping_beauty.kiss()

    def check_processes(self):
        self.sleeping_beauty.charge_capacitor(self.time_step)
        self.sleeping_beauty.ring(self.time_step)

    def check_events(self):
        """Checks all events and triggers them if their conditions are met."""
        self.sleeping_beauty.make_circuit()
        self.sleeping_beauty.break_circuit()
        self.sleeping_beauty.trigger_alarm()
        self.sleeping_beauty.disable_alarm()
        self.sleeping_beauty.rouse_princess()
        self.sleeping_beauty.voltage_available()