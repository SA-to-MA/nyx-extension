import math


class SleepingBeauty:
    def __init__(self, window_closed=True,magnet_operational=True,circuit=False,alarm_enabled=False,alarm_disabled=True,ringing=False,deeply_asleep=True,almost_awake=False,awake=False,charge=0.0,resistance=1.0,ring_time=0.0,voltage=False):
        # Initial conditions based on provided initial state
        self.window_closed = window_closed
        self.magnet_operational = magnet_operational
        self.circuit = circuit
        self.alarm_enabled = alarm_enabled
        self.alarm_disabled = alarm_disabled
        self.ringing = ringing
        self.deeply_asleep = deeply_asleep
        self.almost_awake = almost_awake
        self.awake = awake
        self.charge = charge
        self.resistance = resistance
        self.ring_time = ring_time
        self.voltage = voltage
        self.total_time = 0

    '''Actions'''
    def open_window(self):
        if self.window_closed and self.magnet_operational:
            self.window_closed = False
            self.magnet_operational = False
            print("Action: Window opened, fresh air enters.")

    def close_window(self):
        if not self.window_closed and not self.magnet_operational:
            self.window_closed = True
            self.magnet_operational = True
            print("Action: Window closed.")

    def kiss(self):
        if self.almost_awake:
            self.awake = True
            self.almost_awake = False
            print("Action: Kiss. Sleeping Beauty is now fully awake.")

    '''Events'''
    def make_circuit(self):
        if not self.magnet_operational and not self.circuit:
            self.circuit = True
            print("Event: Circuit completed.")

    def break_circuit(self):
        if self.magnet_operational and self.circuit:
            self.circuit = False
            self.charge = 0
            print("Event: Circuit broken, charge reset.")

    def trigger_alarm(self):
        if self.circuit and self.alarm_disabled and self.voltage:
            self.alarm_enabled = True
            self.alarm_disabled = False
            self.ringing = True
            print("Event: Alarm triggered, ringing begins.")

    def voltage_available(self):
        if self.charge >= 5 and not self.voltage:
            self.voltage = True
            print("Event: Voltage available.")

    def rouse_princess(self):
        if self.ringing and self.ring_time >= 0.001 and self.deeply_asleep:
            self.deeply_asleep = False
            self.almost_awake = True
            print("Event: Rouse Princess. Sleeping Beauty is almost awake.")

    def disable_alarm(self):
        if not self.circuit and self.alarm_enabled and self.ringing:
            self.alarm_enabled = False
            self.ringing = False
            self.alarm_disabled = True
            self.ring_time = 0
            print("Event: Alarm disabled.")

    '''Process'''
    def ring(self, time_step=1):
        if self.ringing:
            self.ring_time += time_step
            print(f"Process: Ringing... Ring time: {self.ring_time:.3f}")
            self.rouse_princess()

    def charge_capacitor(self, time_step=1):
        if self.circuit and not self.voltage:
            self.charge += time_step * (1 / self.resistance)
            print(f"Process: Charging... Charge level: {self.charge:.2f}")
            self.voltage_available()

    def simulate(self, actions, time_step=1, max_time=math.inf):
        """
        Runs the simulation over a series of actions and checks events and processes at each time step.

        :param actions: List of actions to perform along with their timestamps.
        :param time_step: Small increment for time, to allow processes to evolve.
        :param max_time: The maximum simulation time.
        """
        print("Starting the simulation...")
        action_index = 0
        action_count = len(actions)

        while self.total_time < max_time and self.awake == False:
            # Check if it's time to execute the next action
            if action_index < action_count:
                action_time, current_action = actions[action_index]
                if self.total_time >= action_time:
                    if current_action == "openwindow":
                        self.open_window()
                    elif current_action == "closewindow":
                        self.close_window()
                    elif current_action == "kiss":
                        self.kiss()
                    action_index += 1

            if self.awake == False:
                # Process continuous actions
                self.check_processes(time_step)
                # Trigger events based on conditions
                self.check_events()
                # Increment time
                self.total_time += time_step

        print(
            f"Simulation complete. Sleeping Beauty is {'awake' if self.awake else 'still asleep'} after {self.total_time} time units.")

    def check_processes(self, time_step):
        # Process continuous actions
        self.charge_capacitor(time_step)
        self.ring(time_step)
    def check_events(self):
        """Checks all events and triggers them if their conditions are met."""
        self.make_circuit()
        self.break_circuit()
        self.trigger_alarm()
        self.disable_alarm()
        self.rouse_princess()
        self.voltage_available()


# Read actions from file
def read_actions_from_file(file_path):
    '''
    :param file_path: path of file that stores the execution plan
    :return: list of tuples that contain actions to perform and their timestamp
    '''
    actions = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                parts = line.split(':')
                timestamp = float(parts[0].strip())
                action = parts[1].strip().split()[0]
                actions.append((timestamp, action))
    return actions


def retrieve_initial_state(file_path, all_predicates):
    """
    Parses the PDDL problem file to retrieve the initial state,
    with unlisted predicates initialized as False.

    :param file_path: Path to the PDDL problem file.
    :param all_predicates: List of all possible predicates in the domain.
    :return: Dictionary representing the initial state.
    """
    initial_state = {predicate: False for predicate in all_predicates}  # Set all predicates to False by default

    with open(file_path, 'r') as file:
        lines = file.readlines()
        init_section = False
        for line in lines:
            line = line.strip()

            # Start reading the :init section
            if line.startswith("(:init"):
                init_section = True
                continue
            elif line.startswith("(:goal") or line.startswith("(:metric"):
                init_section = False

            # Process the initial state values if in :init section
            if init_section:
                # Parse numeric values
                if line.startswith("(="):
                    parts = line.strip("()").split()
                    variable = parts[1]
                    value = float(parts[2])
                    initial_state[variable] = value

                # Set listed predicates to True
                else:
                    predicate = line.strip("()")
                    initial_state[predicate] = True

    return initial_state

if __name__ == "__main__":
    # set all predicates
    all_predicates = [
        "windowclosed", "windowopen", "magnetoperational", "freshair",
        "circuit", "alarmdisabled", "alarmenabled", "voltage",
        "ringing", "almostawake", "deeplyasleep", "awake"
    ]
    initial_state = retrieve_initial_state("ex/sleeping_beauty/pb01.pddl", all_predicates)
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
    # Load actions from a file and run the simulation
    actions = read_actions_from_file("ex/sleeping_beauty/plans/plan1_pb01.pddl")
    sleeping_beauty.simulate(actions)
