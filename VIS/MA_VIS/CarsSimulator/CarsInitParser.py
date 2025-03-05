from collections import defaultdict
import re

class InitStateCar:
    def __init__(self, problem, cars):
        """
        Initialize the PDDL parser for the Car domain.

        Args:
            problem (str): Path to the PDDL problem file.
            cars (list): List of car agents.
        """
        self.problem_file = problem
        self.cars = cars  # List of car agents

    def parse_pddl_init(self):
        """
        Parses the :init section of a PDDL problem file into a structured dictionary
        specific to the Car domain.

        Returns:
            dict: A dictionary containing parsed predicates and fluents for cars.
        """
        objects = defaultdict(dict)  # Dictionary to store cars and their attributes
        inside_init = False
        stack = 0  # Track nested parentheses

        with open(self.problem_file, 'r') as file:
            for line in file:
                line = line.strip()  # Remove whitespace

                # Detect the start of the :init section
                if not inside_init and "(:init" in line:
                    inside_init = True
                    stack += line.count("(") - line.count(")")
                    line = line.replace("(:init", "").strip()
                elif "(:goal" in line:  # Stop parsing at :goal
                    inside_init = False

                if inside_init:
                    stack += line.count("(") - line.count(")")

                    # Extract predicates and fluents
                    matches = re.findall(r"\((.*?)\)", line)

                    for match in matches:
                        parts = match.split()
                        if not parts:
                            continue

                        # Handle negation: (not (predicate object))
                        if parts[0] == "not" and len(parts) > 1:
                            negated_match = re.match(r"\((\w+)\s+(\w+)\)", parts[1])
                            if negated_match:
                                predicate, car = negated_match.groups()
                                if car in self.cars:
                                    objects[car][predicate] = False  # Store as False

                        # Handle standard predicates (e.g., (running car1))
                        elif len(parts) == 2 and parts[1] in self.cars:
                            predicate, car = parts
                            objects[car][predicate] = True  # Store as True

                        # Handle numeric fluents (e.g., (= (d car1) 0))
                        elif len(parts) == 4 and parts[0] == "=" and parts[1].startswith("("):
                            fluent_match = re.match(r"\((\w+)\s+(\w+)\)", parts[1])
                            if fluent_match:
                                fluent_name, car = fluent_match.groups()
                                if car in self.cars:
                                    objects[car][fluent_name] = float(parts[2])  # Store as float

                    if stack == 0:
                        break  # End of :init section

        # Ensure all expected keys exist with default values
        for car in self.cars:
            objects[car].setdefault("running", False)
            objects[car].setdefault("transmission_fine", False)
            objects[car].setdefault("engine_blown", False)
            objects[car].setdefault("goal_reached", False)
            objects[car].setdefault("running_time", 0.0)
            objects[car].setdefault("d", 0.0)
            objects[car].setdefault("v", 0.0)
            objects[car].setdefault("a", 0.0)
            objects[car].setdefault("up_limit", 10.0)
            objects[car].setdefault("down_limit", -1.0)

        return dict(objects)


# Example Usage
# file_path = "path/to/car_problem.pddl"
# parser = InitStateCar(file_path, ['car1', 'car2'])
# car_init_state = parser.parse_pddl_init()
# print(car_init_state)
