import itertools
from MA_PDDL import MAPDDLParser, MAPDDLDomain


class MAtoSA_Domain:
    def __init__(self, ma_file):
        parser = MAPDDLParser(ma_file)
        self.domain = parser.domain

    def set_agents(self, agents):
        self.domain.agents = agents

    def generate(self):
        """
        Generate all combinations and write the corresponding SA format file.
        """
        combined_actions = self.generate_actions()
        self.write_to_sa_file(combined_actions)

    def generate_actions(self):
        """
        Generate all combinations of actions for the agents and include their predicates and effects.
        """
        # Build the actions_by_agent dictionary
        actions_by_agent = {}
        for action in self.domain.actions:
            for param in action.parameters:
                actions_by_agent.setdefault(param[1], []).append(action)

        # Prepare agent-specific action combinations
        agent_actions = [
            [f"{agent}_{action.name}" for action in actions_by_agent.get(agent_type, [])]
            for agent_type, agents in self.domain.agents.items() for agent in agents
        ]

        # Generate combinations of actions for all agents
        all_combinations = itertools.product(*agent_actions)

        # Process each combination and gather predicates/effects
        all_combined_info = []
        for combination in all_combinations:
            # Collect predicates and effects for each action in the combination
            predicates = []
            effects = []
            for agent_action in combination:
                agent, action_name = agent_action.split('_')
                action = next(act for act in self.domain.actions if act.name == action_name)
                # Process predicates (preconditions)
                predicates.extend(self.get_predicates(action, agent))
                # Process effects
                effects.extend(self.get_effects(action, agent))

            # Collect all info for this combination
            formatted_combination = '-'.join(combination)
            all_combined_info.append({
                'combination': formatted_combination,
                'predicates': predicates,
                'effects': effects
            })

        return all_combined_info

    def get_predicates(self, action, agent):
        """
        Extract predicates (preconditions) for a given action and agent.
        Modify to use the agent's name in predicates (e.g., car1_running).
        """
        predicates = []
        for condition in action.preconditions:
            if isinstance(condition[0], str) and condition[0] in ['<', '<=', '>', '>=', '=']:
                # Comparison condition
                predicates.append(f'({condition[0]} ({agent}_{condition[1][0]}) {agent}_{condition[2][0]})')
            elif condition[0] == 'not': # not predicate
                predicates.append(f'(not ({agent}_{condition[1][0]}))')
            else:# Simple condition
                predicates.append(f'({agent}_{condition[0]})')
        return predicates

    def get_effects(self, action, agent):
        """
        Extract effects for a given action and agent.
        """
        effects = []
        for effect in action.effects:
            if effect[0] == 'increase' or effect[0] == 'decrease' or effect[0] == 'assign':
                effects.append(f'({effect[0]} ({agent}_{effect[1][0]}) {effect[2]})')
            elif effect[0] == 'not':  # If negating the predicate
                effects.append(f'(not ({agent}_{effect[1][0]}))')
            else:
                effects.append(f'({agent}_{effect[0]})')
        return effects

    def write_to_sa_file(self, combined_actions):
        """
        Write the combined actions, predicates, and effects to a file in the SA format.
        """
        with open("output_file.pddl", "w") as file:
            # Write the header (domain name, requirements, types, predicates, functions, etc.)
            file.write(f"(define (domain {self.domain.name})\n")
            file.write("  (:requirements :typing :fluents :time :negative-preconditions :multi-agent)\n")
            file.write("  (:types agent)\n")

            # Write predicates and functions
            file.write("  (:predicates\n")
            for predicate, params in self.domain.predicates.items():
                param_str = " ".join(f"?{param}" for param in params)
                file.write(f"    ({predicate} {param_str})\n")
            file.write("  )\n")

            file.write("  (:functions\n")
            for func, params in self.domain.functions.items():
                param_str = " ".join(f"?{param}" for param in params)
                file.write(f"    ({func} {param_str})\n")
            file.write("  )\n")

            # Write actions
            for action_info in combined_actions:
                file.write(f"  (:action {action_info['combination']}\n")
                file.write("    :precondition (and\n")
                for pred in action_info['predicates']:
                    file.write(f"      {pred}\n")
                file.write("    )\n")
                file.write("    :effect (and\n")
                for eff in action_info['effects']:
                    file.write(f"      {eff}\n")
                file.write("    )\n")
                file.write("  )\n")

            file.write(")\n")


# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    domain = "C:\\Users\\Lior\\Desktop\\Nyx\\nyx-extension\\MA-PDDL\\exMA\\Car_MAPDDL_Domain"
    satoma = MAtoSA_Domain(domain)
    print('----------------------------')
    print('Domain: ' + satoma.domain.__repr__())
    print('Actions: ')
    for action in satoma.domain.actions:
        print(action)

    agents = {'agent': ["car1", "car2", "car3"]}
    satoma.set_agents(agents)
    satoma.generate()
