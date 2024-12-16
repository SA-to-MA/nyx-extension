import itertools
from MA_PDDL import MAPDDLParser, MAPDDLDomain


class MAtoSA_Domain:
    def __init__(self, ma_file):
        parser = MAPDDLParser(ma_file)
        self.domain = parser.domain

    #-----------------------------------------------
    # Set agents
    #-----------------------------------------------
    def set_agents(self, agents):
        self.domain.agents = agents

    #-----------------------------------------------
    # Generate SA-PDDL+ file
    #-----------------------------------------------
    def generate(self, file_name):
        """
        Generate all combinations and write the corresponding SA format file.
        """
        combined_actions = self.generate_actions()
        predicates = self.generate_functions_or_predicates(self.domain.predicates)
        func = self.generate_functions_or_predicates(self.domain.functions)
        procs = self.generate_processes_or_events(self.domain.processes)
        events = self.generate_processes_or_events(self.domain.events)
        self.write_to_sa_file(file_name, combined_actions, predicates, func, procs, events)

    #-----------------------------------------------
    # Generate functions and predicates
    #-----------------------------------------------

    def generate_functions_or_predicates(self, assign_dict):
        """
        Generate all combinations of agent specific definitions for the agents based on their type (functions or predicates)
        """
        agent_specific = []

        for predicate, params in assign_dict.items():
            for param, agent_type in params.items():
                if agent_type in self.domain.agents:
                    for agent in self.domain.agents[agent_type]:
                        # Generate predicate specific to the agent
                        agent_specific.append(f"{agent}_{predicate}")
        return agent_specific

    #-----------------------------------------------
    # Generate processes and events
    #-----------------------------------------------

    def generate_processes_or_events(self, processes_or_events):
        """
        Generate agent-specific processes or events and include their predicates and effects.

        :param processes_or_events: List of process or event objects.
        :return: List of dictionaries containing the specific process/event combinations with predicates and effects.
        """
        agent_specific_info = []

        # Iterate over each agent type and their respective agents
        for agent_type, agents in self.domain.agents.items():
            for agent in agents:
                for process_or_event in processes_or_events:
                    # Check if the process/event matches the agent type
                    if any(param[1] == agent_type for param in process_or_event.parameters):
                        # Generate the agent-specific name for the process/event
                        agent_specific_name = f"{agent}_{process_or_event.name}"

                        # Process preconditions (predicates) using the existing get_predicates function
                        predicates = self.get_predicates(process_or_event, agent)

                        # Process effects using the existing get_effects function
                        effects = self.get_effects(process_or_event, agent)

                        # Collect information for this specific agent-process/event pair
                        agent_specific_info.append({
                            'agent': agent,
                            'process_or_event': agent_specific_name,
                            'predicates': predicates,
                            'effects': effects,
                        })

        return agent_specific_info

    #-----------------------------------------------
    # Generate actions
    #-----------------------------------------------

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

    #-----------------------------------------------
    # Helper function for predicates and effects as part of actions, processes and events
    #-----------------------------------------------
    def get_predicates(self, action, agent):
        """
        Extract predicates (preconditions) for a given action/process/event and agent.
        Modify to use the agent's name in predicates (e.g., car1_running).
        """
        predicates = []
        for condition in action.preconditions:
            if isinstance(condition[0], str) and condition[0] in ['<', '<=', '>', '>=', '=']:
                # Comparison condition
                predicates.append(f'{condition[0]} ({agent}_{condition[1][0]}) {agent}_{condition[2][0]}')
            elif condition[0] == 'not': # not predicate
                predicates.append(f'not ({agent}_{condition[1][0]})')
            else: # Simple condition
                predicates.append(f'{agent}_{condition[0]}')
        return predicates

    def get_effects(self, action, agent):
        """
        Extract effects for a given action/process/event and agent.
        """
        effects = []
        for effect in action.effects:
            if effect[0] == 'increase' or effect[0] == 'decrease' or effect[0] == 'assign':
                if isinstance(effect[2], list): # if nested, create nested expression accordingly
                    expression = self.process_expression(effect[2], agent)
                    effects.append(f'{effect[0]} ({agent}_{effect[1][0]}) {expression}')
                else: # if simple values assignment
                    effects.append(f'{effect[0]} ({agent}_{effect[1][0]}) {effect[2]}')
            elif effect[0] == 'not':  # If negating the predicate
                effects.append(f'not ({agent}_{effect[1][0]})')
            else: # if simple predicate
                effects.append(f'{agent}_{effect[0]}')
        return effects

    def process_expression(self, expression, agent):
        """
        Process a mathematical expression or time-continuous effect, replacing agent-specific variables.
        """
        if isinstance(expression, list):  # If the expression is a nested list
            processed = []
            if len(expression) > 2:  # If it's a nested or continuous action (more than 2 items)
                for elem in expression:
                    if isinstance(elem, list):  # Nested expressions need to be processed
                        processed.append(self.process_expression(elem, agent))
                    else:  # Constant or operator
                        processed.append(elem)
                return f"({' '.join(processed)})"  # Wrap processed list in parentheses
            else:  # If not nested, like an assignment or simple effect
                # Example: ['v', '?agent'] => 'car1_v'
                processed.append(f'{agent}_{expression[0]}')
                return ' '.join(processed)
        else:
            # If it's not a list, it's a simple string or constant, so just replace the agent's variables
            return f'{agent}_{expression}'  # Add agent-specific prefix

    #-----------------------------------------------
    # Write all generated information to file
    #-----------------------------------------------

    def write_to_sa_file(self, file_name, combined_actions, predicates, functions, procs, events):
        """
        Write the combined actions, predicates, and effects to a file in the SA format.
        """
        with open(file_name, "w") as file:
            # Write the header (domain name, requirements, types, predicates, functions, etc.)
            file.write(f"(define (domain {self.domain.name})\n")
            file.write("  (:requirements :typing :fluents :time :negative-preconditions)\n")

            # Write predicates and functions
            file.write("  (:predicates\n")
            for predicate in predicates:
                file.write(f"    ({predicate})\n")
            file.write("  )\n")

            file.write("  (:functions\n")
            for func in functions:
                file.write(f"    ({func})\n")
            file.write("  )\n")

            # Write actions
            for action_info in combined_actions:
                file.write(f"  (:action {action_info['combination']}\n")
                file.write("    :precondition (and\n")
                for pred in action_info['predicates']:
                    file.write(f"      ({pred})\n")
                file.write("    )\n")
                file.write("    :effect (and\n")
                for eff in action_info['effects']:
                    file.write(f"      ({eff})\n")
                file.write("    )\n")
                file.write("  )\n")

            # Write processes
            for process_or_event_info in procs:
                file.write(f"  (:process {process_or_event_info['process_or_event']}\n")
                file.write("    :precondition (and\n")
                for pred in process_or_event_info['predicates']:
                    file.write(f"      ({pred})\n")
                file.write("    )\n")
                file.write("    :effect (and\n")
                for eff in process_or_event_info['effects']:
                    file.write(f"      ({eff})\n")
                file.write("    )\n")
                file.write("  )\n")

            # Write events
            for process_or_event_info in events:
                file.write(f"  (:event {process_or_event_info['process_or_event']}\n")
                file.write("    :precondition (and\n")
                for pred in process_or_event_info['predicates']:
                    file.write(f"      ({pred})\n")
                file.write("    )\n")
                file.write("    :effect (and\n")
                for eff in process_or_event_info['effects']:
                    file.write(f"      ({eff})\n")
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
    # print('Domain: ' + satoma.domain.__repr__())

    agents = {'agent': ["sb1", "sb2"]}
    satoma.set_agents(agents)
    satoma.generate("sleeping_beauty_2agents.pddl")
