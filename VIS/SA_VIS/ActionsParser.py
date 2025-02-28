class ActionsParser:
    # initialize paths for constructor
    def __init__(self, problem_path, sol_path):
        self.problem = problem_path
        self.sol = sol_path

    # Read actions from solution file and return dictionary, each entry is timestamp and actions
    def read_solution_from_file(self):
        '''
        :return: dictionary that contain timestamps as keys, and actions in the timestamp as values
        '''
        actions = {}
        with open(self.sol, 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.split(':')
                    timestamp = float(parts[0].strip())
                    action = parts[1].strip().split()[0]
                    if timestamp in actions:
                        actions[timestamp].append(action)
                    else:
                        actions[timestamp] = [action]
        return actions

    # make initial state and return it
    def retrieve_initial_state(self, all_predicates=[]):
        """
        Parses the PDDL problem file to retrieve the initial state,
        with unlisted predicates initialized as False.

        :param all_predicates: List of all possible predicates in the domain.
        :return: Dictionary representing the initial state.
        """
        initial_state = {predicate: False for predicate in all_predicates}  # Set all predicates to False by default

        with open(self.problem, 'r') as file:
            lines = file.readlines()
            init_section = False
            for line in lines:
                line = line.strip()

                # Start reading the :init section
                if line.startswith("(:init"):
                    init_section = True
                    line = line[6:].strip()
                elif line.startswith("(:goal") or line.startswith("(:metric"):
                    init_section = False

                # Process the initial state values if in :init section
                if init_section:
                    # Parse numeric values
                    if line.startswith("(="):
                        parts = line.strip("()").split()
                        variable = parts[1].strip("()")
                        value = float(parts[2])
                        initial_state[variable] = value

                    # Set listed predicates to True
                    else:
                        predicate = line.strip("()")
                        initial_state[predicate] = True
        return initial_state