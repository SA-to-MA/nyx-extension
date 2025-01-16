from collections import defaultdict
import re

class InitState:
    def __init__(self, problem, agents, blocks):
        self.problem_file = problem
        self.agents = agents
        self.blocks = blocks

    def parse_pddl_init(self):
        """
        Parse the :init predicates from a PDDL problem file into a dictionary
        specific to agents and blocks.

        Args:
            problem_file (str): Path to the PDDL problem file.
            agents (list): List of agents.
            blocks (list): List of blocks.

        Returns:
            dict: A dictionary with separate predicates for agents and blocks.
        """
        objects = defaultdict(dict)  # Nested dictionary for agents and blocks
        inside_init = False
        stack = 0  # To track nested parentheses

        with open(self.problem_file, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace

                # Check if we are entering the :init section
                if not inside_init and "(:init" in line:
                    inside_init = True
                    # Count the opening parenthesis
                    stack += line.count("(") - line.count(")")
                    # Remove the :init keyword and continue processing
                    line = line.replace("(:init", "").strip()
                elif "(:goal" in line:
                    inside_init = False

                # If we are inside the :init section
                if inside_init:
                    # Count parentheses to detect the end of :init
                    stack += line.count("(") - line.count(")")

                    # Extract predicates from the current line
                    matches = re.findall(r"\((.*?)\)", line)
                    for match in matches:
                        parts = match.split()
                        predicate = parts[0]
                        args = parts[1:]

                        # Handle predicates for blocks
                        if predicate == "clear" and args[0] in self.blocks:
                            block = args[0]
                            objects[block]["clear"] = True

                        elif predicate == "ontable" and args[0] in self.blocks:
                            block = args[0]
                            objects[block]["on_table"] = True

                        elif predicate == "on" and args[0] in self.blocks and args[1] in self.blocks:
                            top_block, bottom_block = args
                            objects[top_block]["on"] = bottom_block

                        elif predicate == "handempty" and args[0] in self.agents:
                            agent = args[0]
                            objects[agent]["holding"] = None
                            objects[agent]["is_empty"] = True

                        elif predicate == "holding" and args[0] in self.agents and args[1] in self.blocks:
                            agent, block = args
                            objects[agent]["holding"] = block
                            objects[agent]["is_empty"] = False
                            objects[block]["in_hand"] = True

                    # If stack is zero, it means the :init section is complete
                    if stack == 0:
                        break

        # Finalize the structure for agents and blocks
        for agent in self.agents:
            objects[agent].setdefault("holding", None)
            objects[agent].setdefault("is_empty", True)

        for block in self.blocks:
            objects[block].setdefault("on_table", False)
            objects[block].setdefault("clear", False)
            objects[block].setdefault("in_hand", False)
            objects[block].setdefault("on", None)

        return dict(objects)


# Example usage
# file_path = "../MA_PDDL/examples/Blocks/problem-a1.pddl"  # Replace with your file path
# try:
#     parser = InitState(file_path,['a1', 'a2'], ['a', 'b', 'c'])
#     object_dict = parser.parse_pddl_init()
#     print(object_dict)
# except FileNotFoundError:
#     print(f"File not found: {file_path}")
# except ValueError as e:
#     print(e)
