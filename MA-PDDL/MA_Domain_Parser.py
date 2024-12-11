import itertools
from PDDL_Parser import PDDL_Parser

class MA_Domain:
    def __init__(self, sa_file, numberOfAgents):
        parser = PDDL_Parser(sa_file)
        self.SA_domain = parser.domain
        self.numOfAgents = numberOfAgents
        self.MA_domain = self.generate()

    def generate(self):
        pass

    def generate_ordered_pairs(self, agents, actions):
        """
        Generate all possible ordered pairs of agents and actions in the format:
        agent1_action-agent2_action-...
        """
        pairs = []

        # Generate all combinations of agents and actions (cross product)
        for agent_action_pair in itertools.product(actions, repeat=len(agents)):
            # Create a formatted string for this particular combination
            pair_string = '-'.join([f'{agents[i]}_{agent_action_pair[i]}' for i in range(len(agents))])
            pairs.append(pair_string)

        return pairs


