import itertools
from MA_PDDL import MAPDDLParser


class MAtoSA_Domain:
    def __init__(self, ma_file):
        parser = MAPDDLParser(ma_file)
        self.domain = parser.domain

    #-----------------------------------------------
    # Set agents
    #-----------------------------------------------
    def set_agents(self, agents):
        for agent_type in agents.keys():
            for agent_name in agents[agent_type]:
                self.domain.add_agent(agent_type, agent_name)
    #-----------------------------------------------
    # Set objects
    #-----------------------------------------------
    def set_objects(self, objects):
        for obj_type in objects.keys():
            for obj_name in objects[obj_type]:
                self.domain.add_object(obj_type, obj_name)


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
        Generate all combinations of agent-specific definitions for the agents based on their type (functions or predicates).
        Creates predicates in the format: holding_a1_b1 instead of (holding a1 b1).
        """
        agent_specific = []

        for predicate, params in assign_dict.items():
            if len(params) == 0:
                # No parameters, add predicate as is
                agent_specific.append(predicate)
            else:
                # Collect lists of possible values for each parameter
                param_lists = []

                for param, ptype in params.items():
                    if ptype in self.domain.agents:
                        # If it's an agent type, generate all relevant agents
                        relevant_agents = [f"{agent}" for agent in self.domain.agents[ptype]]
                        param_lists.append(relevant_agents)
                    elif ptype in self.domain.objects:
                        # If it's an object type, generate all relevant objects
                        relevant_objects = [f"{obj}" for obj in self.domain.objects[ptype]]
                        param_lists.append(relevant_objects)

                # Use itertools.product to generate all combinations of parameters
                for combination in itertools.product(*param_lists):
                    if not any(agent == obj for agent, obj in zip(combination[::2], combination[1::2])):
                        agent_specific.append(f"{predicate}_{'_'.join(combination)}")

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

    def generate_combinations_for_actions(self):
        '''
        :return: a dictionary of action names as keys, and list of valid param tuples as values
        '''
        # create dictionary for all actions to be returned
        actions = {}
        # Iterate through each action
        for action in self.domain.actions:
            params = action.parameters
            if len(params) == 0:
                actions[action.name] = []
            else:
                comb_list = [()]
                # create all possible combinations
                for param in params:
                    if param[1] in self.domain.agents:
                        # Get the list of agents for this parameter type
                        param_values = self.domain.agents[param[1]]
                    elif param[1] in self.domain.objects:
                        # Get the list of objects for this parameter type
                        param_values = self.domain.objects[param[1]]
                    else:
                        raise Exception(f"Unexpected type {param[1]} in action {action.name}")
                    comb_list = [
                        existing_comb + (new_value,)
                        for existing_comb in comb_list
                        for new_value in param_values
                    ]
                    filtered_combinations = []
                    for comb in comb_list:
                        # If there are no duplicate objects, keep the combination
                        if len(comb) == len(set(comb)):
                            filtered_combinations.append(comb)
                    actions[action.name] = filtered_combinations
        return actions

    def generate_joint_actions(self, action_combinations, total_agents):
        """
        Generate all possible joint actions based on the given action combinations
        while ensuring no intersection of parameters across actions.

        :param action_combinations: A dictionary of actions and their parameter combinations.
        :param total_agents: Total number of agents in the system.
        :return: A list of valid joint action combinations.
        """
        # Collect all possible actions for each agent
        all_possible_actions = [
            (action_name, params) for action_name, combinations in action_combinations.items()
            for params in combinations
        ]

        # Generate all possible joint action combinations for the number of agents
        joint_combinations = itertools.combinations(all_possible_actions, total_agents)

        valid_joint_actions = []

        for joint_action in joint_combinations:
            # Collect all agents and objects used in the joint action
            used_agents = set()
            used_objects = set()
            is_valid = True

            for action_name, params in joint_action:
                agent = params[0]
                objects = params[1:]

                # Check if the agent or objects are already used
                if agent in used_agents or any(obj in used_objects for obj in objects):
                    is_valid = False
                    break

                # Add the agent and objects to the used sets
                used_agents.add(agent)
                used_objects.update(objects)

            if is_valid:
                valid_joint_actions.append(joint_action)

        return valid_joint_actions

    def generate_actions(self):
        """
        Generate all valid combinations of actions based on agents and objects, with no repetition of agents or objects in the same combination.
        """
        # get all possible combinations
        params_for_actions = self.generate_combinations_for_actions()
        # generate joined actions
        total_agents = sum(len(values) for values in self.domain.agents.values())
        joint_act = self.generate_joint_actions(params_for_actions, total_agents)
        # all actions
        all_actions = []
        # create helper domain to use for quick access of actions
        action_dict = {action.name: action for action in self.domain.actions}
        # iterate all possible combinations
        for combination in joint_act:
            # set initial values of combination
            action_name = ''
            predicates, effects = [], []
            # iterate all actions in combination
            for action in combination:
                # add action name and params to full action name
                formatted_string = f"{action[0]}_" + "_".join(action[1])
                if action_name == '':
                    action_name += formatted_string
                else:
                    action_name += f'&{formatted_string}'
                predicates.extend(self.get_predicates(action_dict[action[0]], action[1]))

    #-----------------------------------------------
    # Helper function for predicates and effects as part of actions, processes and events
    #-----------------------------------------------
    def get_predicates(self, action, params):
        """
        Extract predicates (preconditions) for a given action/process/event and agent.
        Modify to use the agent's name in predicates (e.g., car1_running).
        """
        # iterate params of action and map each argument to a param from input
        mapped_params = {}
        for i in range(len(action.parameters)):
            mapped_params[action.parameters[i][0]] = params[i]
        predicates = []
        agent= ""
        for condition in action.preconditions:
            predicate = ''
            if isinstance(condition[0], str) and condition[0] in ['<', '<=', '>', '>=', '=']:
                # Comparison condition
                predicate = f'{condition[0]} ({condition[1][0]}_{mapped_params[condition[1][1]]}) '
                if isinstance(condition[2], str): # if simple integer, put as is
                    predicate += condition[2]
                else: # if function, put function
                    predicate += f'({condition[2][0]}_{mapped_params[condition[2][1]]})'
                predicates.append(predicate)
            elif condition[0] == 'not': # not predicate
                predicate = f'not ({condition[1][0]}'
                for i in range(1, len(condition[1])):
                    predicate += f'_{mapped_params[condition[1][i]]}'
                predicate += ')'
            else: # Simple condition - add all required
                predicate = condition[0]
                for i in range(1, len(condition)):
                    predicate += f'_{mapped_params[condition[i]]}'
            predicates.append(predicate)
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
    # domain = r"examples\Blocks\domain-a1.pddl"
    # satoma = MAtoSA_Domain(domain)
    # print('----------------------------')
    # # print('Domain: ' + satoma.domain.__repr__())
    # # dict of agent types and the number of agents to generate
    # agents = {'agent': ['agent1', 'agent2']}
    # objects = {'block': ['block1', 'block2', 'block3']}
    # satoma.set_agents(agents)
    # satoma.set_objects(objects)
    # satoma.generate("2_domain.pddl")
    domain = r"examples\Car\Car_MAPDDL_Domain"
    satoma = MAtoSA_Domain(domain)
    print('----------------------------')
    # print('Domain: ' + satoma.domain.__repr__())
    # dict of agent types and the number of agents to generate
    agents = {'car': ['car1', 'car2']}
    satoma.set_agents(agents)
    satoma.generate("2_domain.pddl")
