from collections import defaultdict
import re

class MinecraftInitState:
    def __init__(self, problem_file, agents):
        self.problem_file = problem_file
        self.agents = agents

    def extract_block(self, content, tag):
        """Extracts a full balanced block like (:init ...) or (:goal ...)"""
        start = content.find(f"({tag}")
        if start == -1:
            raise ValueError(f"({tag} not found")

        index = start + len(f"({tag}")
        depth = 1
        while index < len(content):
            if content[index] == "(":
                depth += 1
            elif content[index] == ")":
                depth -= 1
                if depth == 0:
                    return content[start + len(f"({tag}"):index].strip()
            index += 1

        raise ValueError(f"Unmatched parentheses for ({tag})")

    def parse_pddl_init(self):
        inventory = defaultdict(int)
        env = {}
        agent_status = defaultdict(lambda: {"free": False})
        goals = {}

        with open(self.problem_file, 'r') as file:
            content = file.read().replace('\n', ' ')

        init_content = self.extract_block(content, ":init")
        goal_content = self.extract_block(content, ":goal")

        # Split init_content into tokens based on ')(' boundaries
        tokens = init_content.replace(')(', ')|(').split('|')
        # Parse goal block
        goal_content = goal_content.replace('(and', '').strip()
        goal_tokens = goal_content.replace(')(', ')|(').split('|')

        for raw in tokens:
            raw = raw.strip().strip('()')  # Remove outer parens and whitespace
            if not raw:
                continue

            parts = raw.split()

            # Handle (= x y)
            if parts[0] == '=' and len(parts) >= 3:
                func_name = parts[1].strip('()')
                try:
                    value = int(parts[2].strip(')'))
                    if func_name.startswith("count_"):
                        inventory[func_name] += value
                    else:
                        env[func_name] = value
                except ValueError:
                    continue


            # Handle (agent_free a1)
            elif parts[0] == "agent_free" and len(parts) == 2:
                agent = parts[1]
                if agent in self.agents:
                    agent_status[agent]["free"] = True

            # Optional: Handle direct value predicates like (trees_in_map 3)
            elif len(parts) == 2:
                key = parts[0]
                try:
                    value = int(parts[1])
                    env[key] = value
                except ValueError:
                    continue

        for raw in goal_tokens:
            raw = raw.strip().strip('()')
            if not raw:
                continue

            parts = raw.split()
            if parts[0] == '=' and len(parts) >= 3:
                func_name = parts[1].strip('()')
                try:
                    value = int(parts[2].strip(')'))
                    goals[func_name] = value
                except ValueError:
                    continue

        return inventory, env, agent_status, goals

