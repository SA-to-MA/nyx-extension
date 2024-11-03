from SleepingBeauty import SleepingBeauty

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