from collections import defaultdict
import re

class MinecraftInitState:
    def __init__(self, problem_file, agents):
        self.problem_file = problem_file
        self.agents = agents

    def parse_pddl_init(self):
        inventory = defaultdict(dict)
        env = {}
        inside_init = False
        stack = 0

        with open(self.problem_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not inside_init and "(:init" in line:
                    inside_init = True
                    stack += line.count("(") - line.count(")")
                    line = line.replace("(:init", "").strip()
                elif "(:goal" in line:
                    inside_init = False

                if inside_init:
                    stack += line.count("(") - line.count(")")
                    matches = re.findall(r"\(=\s+\((.*?)\)\s+(\d+)\)", line)
                    for func_name, value in matches:
                        func_parts = func_name.strip().split()
                        func = func_parts[0]
                        value = int(value)
                        if "inventory" in func or "count_" in func:
                            # Try to extract the agent (usually second token)
                            if len(func_parts) > 1 and func_parts[1] in self.agents:
                                agent = func_parts[1]
                                inventory[agent][func] += value
                            else:
                                inventory["global"][func] += value
                        else:
                            env[func] = value

                    pred_matches = re.findall(r"\((\w+)(.*?)\)", line)
                    for pred, args in pred_matches:
                        args = args.strip().split()
                        if pred == "agent_free" and args[0] in self.agents:
                            inventory[args[0]]["free"] = True

                    if stack == 0:
                        break

        return dict(inventory)
