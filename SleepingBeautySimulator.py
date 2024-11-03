from SleepingBeauty import SleepingBeauty
from ActionsParser import ActionsParser
import math

class SleepingBeautySimulator:
    def __init__(self, sleeping_beauty, actions, time_step=1, max_time=math.inf):
        self.sleeping_beauty = sleeping_beauty
        self.actions = actions
        self.time_step = time_step
        self.max_time = max_time
        self.total_time = 0

    def run(self):
        """
        Runs the simulation over a series of actions and checks events and processes at each time step.
        """
        print("Starting the simulation...")
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

if __name__ == "__main__":
    # set all predicates
    all_predicates = [
        "windowclosed", "windowopen", "magnetoperational", "freshair",
        "circuit", "alarmdisabled", "alarmenabled", "voltage",
        "ringing", "almostawake", "deeplyasleep", "awake"
    ]
    # create actions parser with problem and solution paths
    problem = "ex/sleeping_beauty/pb01.pddl"
    sol = "ex/sleeping_beauty/plans/plan1_pb01.pddl"
    parser = ActionsParser(problem, sol)
    # get initial state and map it
    initial_state = parser.retrieve_initial_state(all_predicates)
    # This mapping will depend on your naming convention.
    mapped_initial_state = {
        "window_closed": initial_state.get("windowclosed", True),
        "magnet_operational": initial_state.get("magnetoperational", True),
        "circuit": initial_state.get("circuit", False),
        "alarm_enabled": initial_state.get("alarmenabled", False),
        "alarm_disabled": initial_state.get("alarmdisabled", True),
        "ringing": initial_state.get("ringing", False),
        "deeply_asleep": initial_state.get("deeplyasleep", True),
        "almost_awake": initial_state.get("almostawake", False),
        "awake": initial_state.get("awake", False),
        "charge": initial_state.get("charge", 0.0),
        "resistance": initial_state.get("resistance", 1.0),
        "ring_time": initial_state.get("ringtime", 0.0),
        "voltage": initial_state.get("voltage", False)
    }
    # Create an instance of SleepingBeauty with the initial state
    sleeping_beauty = SleepingBeauty(**mapped_initial_state)
    # Load actions of solution from a file
    actions = parser.read_solution_from_file()
    # create simulator object
    simulator = SleepingBeautySimulator(sleeping_beauty, actions)
    simulator.run()