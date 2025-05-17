import re

class SolutionParser:
    def __init__(self, agents_by_type, domain, plan):
        self.domain = domain
        self.plan = plan
        self.agents_by_type = agents_by_type
        self.all_agents = [agent for agents in self.agents_by_type.values() for agent in agents]
        self.agents_actions = {}
        self.actions = {}


    def parse_actions(self):
        with open(self.domain, 'r') as f:
            domain_text = f.read()

        # Clean up comments and whitespace
        domain_text = re.sub(r";.*", "", domain_text)  # remove comments
        domain_text = re.sub(r"\s+", " ", domain_text)  # normalize whitespace

        # Regex for :action blocks only
        pattern = r"\(:action\s+([^\s]+)\s+:parameters\s*\(([^)]*)\)"
        for match in re.finditer(pattern, domain_text):
            action_name, param_str = match.groups()
            action_name = action_name.lower() # convert to lowercase if not already
            param_tokens = param_str.strip().split()

            # Extract parameter types
            param_types = []
            i = 0
            while i < len(param_tokens):
                if param_tokens[i].startswith("?") and i + 2 < len(param_tokens) and param_tokens[i + 1] == "-":
                    param_types.append(param_tokens[i + 2])
                    i += 3
                else:
                    i += 1  # skip malformed or incomplete tokens

            self.actions[action_name] = param_types

        return self.actions

    def parse(self):
        # create actions dictionary from domain
        self.parse_actions()
        with open(self.plan, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line == '':
                    continue
                # Extract agent name and actions from the line
                self.parse_line(line)

    def parse_line(self, line):
        parts = line.split()
        parts = parts[1:-1]
        actions = parts.pop(0).split('&')
        cur_agents = []
        for act in actions:
            req_params = len(self.actions[act])
            params = []
            agent_name = ""
            for i in range(req_params):
                cur = parts.pop(0)
                if cur in self.all_agents:
                    agent_name = cur
                else:
                    params.append(cur)
            if agent_name not in self.agents_actions:
                self.agents_actions[agent_name] = []
            self.agents_actions[agent_name].append((act, params))
            cur_agents.append(agent_name)
        # if agent does nothing, append empty tuple
        for agent in self.all_agents:
            if agent not in cur_agents:
                if agent not in self.agents_actions:
                    self.agents_actions[agent] = []
                self.agents_actions[agent].append(())
