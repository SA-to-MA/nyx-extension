import VisBlocks

class Parser:
    def __init__(self, _agents, _actions):
        # create list of Agents
        # actions = {'stack': [agent, block, block],'unstack':[...]}
        self.agents = {}
        self.actions = _actions
        for a in _agents:
            self.agents[a] = Agent(a, [])
        self.objects = {}

    def parse(self, _plan):
        with open(_plan, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line == '':
                    continue
                # Extract agent name and actions from the line
                self.parse_line(line)

    def parse_line(self, line):
        # Match the format: "<time>: <agent>&<action1>&<action2> <params> [<time_cost>]"
        parts = line.split()
        parts = parts[1:-2]
        actions = parts.pop(0).split('&')
        for act in actions:
            req_params = len(self.actions[act])
            params = []
            agent_name = ""
            for i in range(req_params):
                cur = parts.pop(0)
                if cur in self.agents:
                    agent_name = cur
                else:
                    params.append(cur)
            self.agents[agent_name].add_action((act, params))

class Agent:
    def __init__(self, _name, _actions):
        self.actions = _actions
        self.name = _name

    def add_action(self, _action):
        self.actions.append(_action)

    def get_next_action(self):
        return self.actions.pop(0)


