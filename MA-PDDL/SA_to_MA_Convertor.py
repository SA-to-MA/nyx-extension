import itertools
from MA_PDDL import MAPDDLParser, MAPDDLDomain

class MAtoSA_Domain:
    def __init__(self, ma_file):
        parser = MAPDDLParser(ma_file)
        self.domain = parser.domain

    def generate(self, agents):
        """
        :param agents: dictionary of agents to be generated in file, where key is agent type and value is list of names of instances of that type
        :return:
        """
        # set agents in domain
        self.domain.agents = agents
        # iterate all actions and create dictionary of {agent type: [possible actions]}
        actions_by_agent = {}
        for action in self.domain.actions:
            # get parameters
            params = action.parameters
            # iterate parameters and add action to each agent type
            for p in params:
                if p[1] in actions_by_agent.keys():
                    actions_by_agent[p[1]].append(action.name)
                else:
                    actions_by_agent[p[1]] = [action.name]
        print(self.generate_actions(actions_by_agent))
        print(self.generate_processes_and_events(actions_by_agent))

    def generate_processes_and_events(self, actions_by_process):
        """
        :param actions_by_process: a dict where each agent type has a list of possible events/processes it can perform
        :return: a list of all possible agent-process combinations
        """
        agent_proc_pairs = []
        # Generate combinations of agent-process pairs
        for agent_type, agent_list in self.domain.agents.items():
            for agent in agent_list:
                # Get processes specific to the agent's type
                available_proc = actions_by_process(agent_type, [])

                # Generate all combinations of processes for this agent
                for proc in available_proc:
                    agent_proc_pairs.append(f'{agent}_{proc}')
        return agent_proc_pairs

    def generate_actions(self, actions_by_agent):
        """
        Generate all possible combinations of actions for each agent type.

        :param actions_by_agent: dictionary of agents, where key is the agent type and value is a list of possible actions.
        :return: list of formatted action pairs for multiple agents
        """
        action_lists = []

        # Generate list of actions for each agent type
        for agent_type, agent_list in self.domain.agents.items():
            actions_for_agents = []

            # For each agent of a given type, generate possible actions
            for agent in agent_list:
                available_actions = actions_by_agent.get(agent_type, [])
                actions_for_agents.append([f'{agent}_{action}' for action in available_actions])

            # Add the action list for the agent type to the action_lists
            action_lists.append(actions_for_agents)

        # Use itertools.product to generate all combinations of actions for all agents
        all_combinations = list(itertools.product(*action_lists))

        # Format the combinations into a list of strings
        formatted_combinations = ['-'.join(combination) for combination in all_combinations]

        return formatted_combinations


#-----------------------------------------------
# Main
#-----------------------------------------------
if __name__ == '__main__':
    import numpy
    print(numpy.__version__)
    domain = "C:\\Users\\Lior\\Desktop\\Nyx\\nyx-extension\\MA-PDDL\\exMA\\Car_MAPDDL_Domain"
    satoma = MAtoSA_Domain(domain)
    print('----------------------------')
    print('Domain: ' + satoma.domain.__repr__())
    print('Actions: ')
    for action in satoma.domain.actions:
        print(action)
    agents = {'agent': ["car1", "car2"]}
    satoma.generate(agents)



