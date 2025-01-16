import itertools
from syntax.action import Action
from MA_PDDL import MAPDDLParser


class MAtoSA:
    def __init__(self, ma_domain, ma_problem):
        # parse domain and problem
        parser = MAPDDLParser(ma_domain, ma_problem)
        # set domain and problem
        self.problem = parser.problem
        self.domain = parser.domain
        # set agents and objects from problem in domain
        self.domain.agents = self.problem.agents
        self.domain.objects = self.problem.objects


    #-----------------------------------------------
    # Generate SA-PDDL+ files
    #-----------------------------------------------
    def generate(self, domain_file_name, problem_file_name):
        """
        Generate all combinations and write the corresponding SA format file.
        """
        self.generate_no_op() # generate no operation action for each agent type
        predicates = self.generate_functions_or_predicates(self.domain.predicates) # generate all possible predicates
        combined_actions = self.generate_actions() # generate combinations of actions
        func = self.generate_functions_or_predicates(self.domain.functions) #generate functions
        procs = self.generate_processes_or_events(self.domain.processes) # generate processes
        events = self.generate_processes_or_events(self.domain.events) # generate events
        self.write_domain_to_sa_file(domain_file_name, combined_actions, predicates, func, procs, events) # write new SAPDDL+ domain file
        self.write_problem_to_sa_file(problem_file_name) # write new SAPDDL+ problem file

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
                        agent_specific.append(f"{predicate}-{'-'.join(combination)}")

        return agent_specific

    #-----------------------------------------------
    # Generate processes and events
    #-----------------------------------------------

    def generate_processes_or_events(self, processes_or_events):
        """
        Generate agent-specific processes or events and include their predicates and effects efficiently.

        :param processes_or_events: List of process or event objects.
        :return: List of dictionaries containing the specific process/event combinations with predicates and effects.
        """
        if not processes_or_events:
            return []
        all_process = [] # list of processes to return
        process_combinations = self.generate_combinations(processes_or_events) # all combinations for possible processes
        for process in processes_or_events: # iterate all process
            cur_combinations = process_combinations[process.name] # get all combinations
            for combination in cur_combinations: # iterate combinations
                process_name = str(process.name) + '-' + '-'.join(combination)
                mapped_params = {}  # mapping params to types inserted
                for i in range(len(process.parameters)):
                    mapped_params[process.parameters[i][0]] = combination[i]
                effects = self.get_effects(process.effects, mapped_params)
                predicates = self.get_predicates(process.preconditions, mapped_params)
                all_process.append({
                    'process_or_event': process_name,
                    'predicates': predicates,
                    'effects': effects
                })
        return all_process



    #-----------------------------------------------
    # Generate actions
    #-----------------------------------------------

    def generate_no_op(self):
        '''
        :return: Adds an action of no op for each agent type, in order to create combinations of actions in
        which some agents don't do anything in current time mark
        '''
        # Loop through agent types and create a no-op action for each
        for agent_type, agent_list in self.domain.agents.items():
            # Create a no-op action for the agent type
            noop_action = Action(
                name=f"NoOP",  # Name of the action
                parameters=[('?agent', agent_type)],  # Parameter for agent type
                preconditions=[],  # No preconditions
                effects=[]  # No effects
            )
            self.domain.actions.append(noop_action)

    def generate_combinations(self, actions_list):
        '''
        :param actions_list: list of action objects, from which the actions combinations needs to be constructed
        :return: a dictionary of action names as keys, and list of valid param tuples as values
        '''
        # create dictionary for all actions to be returned
        actions = {}
        # Iterate through each action
        for action in actions_list:
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
        uses helper functions go generate all combinations and joint actions.
        """
        # base case - empty domain, return empty array of actions
        if not self.domain.actions:
            return []
        # get all possible combinations
        params_for_actions = self.generate_combinations(self.domain.actions)
        # generate joined actions
        total_agents = sum(len(values) for values in self.domain.agents.values())
        joint_act = self.generate_joint_actions(params_for_actions, total_agents)
        # all actions
        all_actions = []
        # create helper domain to use for quick access of actions
        action_dict = {action.name: action for action in self.domain.actions}
        # create dictionary for memoization of effects and preconditions, where every key is (action, (objects)) and value is effects or preconditions
        effects_memo, preconditions_memo = {}, {}
        # iterate all possible combinations
        for combination in joint_act:
            # set initial values of combination
            action_name = ''
            predicates, effects = [], []
            # iterate all actions in combination
            for action in combination:
                # add action name and params to full action name
                formatted_string = f"{action[0]}-" + "-".join(action[1])
                if action_name == '':
                    action_name += formatted_string
                else:
                    action_name += f'&{formatted_string}'
                if action not in effects_memo:
                    mapped_params = {} # mapping params to types inserted
                    cur_act = action_dict[action[0]] # current action object
                    for i in range(len(cur_act.parameters)):
                        mapped_params[cur_act.parameters[i][0]] = action[1][i]
                    preconditions_memo[action] = self.get_predicates(action_dict[action[0]].preconditions, mapped_params)
                    effects_memo[action] = self.get_effects(action_dict[action[0]].effects, mapped_params)
                effects.extend(effects_memo[action])
                predicates.extend(preconditions_memo[action])
            all_actions.append({
                'combination': action_name,
                'predicates': predicates,
                'effects': effects
            })
        return all_actions

    #-----------------------------------------------
    # Helper function for predicates and effects as part of actions, processes and events
    #-----------------------------------------------
    def get_predicates(self, action_pred, mapped_params):
        '''
        :param action_pred: list of all the predicates of an action
        :param mapped_params: mapped dictionary of agent argument in params of action, to it's name of agent
        :return:
        Extract predicates (preconditions) for a given action/process/event and agent.
        Modify to use the agent's name in predicates (e.g., car1_running).
        '''
        predicates = []
        for condition in action_pred:
            predicate = ''
            if isinstance(condition[0], str) and condition[0] in ['<', '<=', '>', '>=', '=']:
                # Comparison condition
                predicate = f'{condition[0]} ({condition[1][0]}-{mapped_params[condition[1][1]]}) '
                if isinstance(condition[2], str): # if simple integer, put as is
                    predicate += condition[2]
                else: # if function, put function
                    predicate += f'({condition[2][0]}-{mapped_params[condition[2][1]]})'
            elif condition[0] == 'not': # not predicate
                predicate = f'not ({condition[1][0]}'
                for i in range(1, len(condition[1])):
                    predicate += f'-{mapped_params[condition[1][i]]}'
                predicate += ')'
            else: # Simple condition - add all required
                predicate = condition[0]
                for i in range(1, len(condition)):
                    predicate += f'-{mapped_params[condition[i]]}'
            predicates.append(predicate)
        return predicates

    def get_effects(self, act_effects, mapped_params):
        '''
        :param action_pred: list of all the effects of an action
        :param mapped_params: mapped dictionary of agent argument in params of action, to it's name of agent
        :return: Extract effects for a given action/process/event and agent.
        '''
        effects = []
        for effect in act_effects:
            if effect[0] == 'increase' or effect[0] == 'decrease' or effect[0] == 'assign':
                if isinstance(effect[2], list): # if nested, create nested expression accordingly
                    expression = self.process_expression(effect[2], mapped_params)
                    effects.append(f'{effect[0]} ({effect[1][0]}-{mapped_params[effect[1][1]]}) {expression}')
                else: # if simple values assignment
                    effects.append(f'{effect[0]} ({effect[1][0]}-{mapped_params[effect[1][1]]}) {effect[2]}')
            elif effect[0] == 'not':  # If negating the predicate
                effects.append(f'not ({effect[1][0]}-{mapped_params[effect[1][1]]})')
            else: # if simple predicate
                effects.append(f'{effect[0]}-{mapped_params[effect[1]]}')
        return effects

    def process_expression(self, expression, mapped_params):
        """
        :param expression: the tokens of the expression that needs to be processed
        :param mapped_params: mapped dictionary of agent argument in params of action, to it's name of agent
        :return:
        Process a mathematical expression or time-continuous effect, replacing agent-specific variables.
        """
        if isinstance(expression, list):  # If the expression is a nested list
            processed = []
            if len(expression) > 2:  # If it's a nested or continuous action (more than 2 items)
                for elem in expression:
                    if isinstance(elem, list):  # Nested expressions need to be processed
                        processed.append(self.process_expression(elem, mapped_params))
                    else:  # Constant or operator
                        processed.append(elem)
                return f"({' '.join(processed)})"  # Wrap processed list in parentheses
            else:  # If not nested, like an assignment or simple effect
                # Example: ['v', '?agent'] => 'v-car1'
                processed.append(f'({expression[0]}-{mapped_params[expression[1]]})')
                return ' '.join(processed)
        else:
            # If it's not a list, it's a simple string or constant, so just replace the agent's variables
            return f'{expression}'  # Add agent-specific prefix

    #-----------------------------------------------
    # Write all generated information to file
    #-----------------------------------------------

    def write_domain_to_sa_file(self, file_name, combined_actions, predicates, functions, procs, events):
        '''
        :param file_name: name of output file
        :param combined_actions: list of actions
        :param predicates: list of predicates
        :param functions: list of functions
        :param procs: list of processes
        :param events: list of events
        :return: Write the combined actions, predicates, and effects to a file in the SA format.
        '''
        with open(file_name, "w") as file:
            # Write the header (domain name, requirements, types, predicates, functions, etc.)
            file.write(f"(define (domain {self.domain.name})\n")
            file.write("  (:requirements ")
            # Join the list elements with a space and write them
            file.write(" ".join(self.domain.requirements))
            # Close the parentheses and write a newline
            file.write(")\n")

            # Write predicates
            if predicates:
                file.write("  (:predicates\n")
                for predicate in predicates:
                    file.write(f"    ({predicate})\n")
                file.write("  )\n")

            # if there are functions, write
            if self.domain.functions:
                file.write("  (:functions\n")
                for func in functions:
                    file.write(f"    ({func})\n")
                file.write("  )\n")

            # Write actions
            for action_info in combined_actions:
                file.write(f"  (:action {action_info['combination']}\n")
                # file.write("    :parameters ()\n")
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

    def write_problem_to_sa_file(self, file_name):
        '''
        :param file_name: the name of the output file
        :return: Write the MA problem in syntax of SA problem
        '''
        with open(file_name, "w") as file:
            # Write the header (domain name, requirements, types, predicates, functions, etc.)
            file.write(f"(define (problem {self.problem.name}) (:domain {self.domain.name})\n")

            # map each object and agent to itself
            mapped = {}
            for key, values in self.domain.agents.items():
                for value in values:
                    mapped[value] = value
            for key, values in self.domain.objects.items():
                for value in values:
                    mapped[value] = value

            # Write init
            if self.problem.init:
                file.write("(:init\n")
                pred = self.get_predicates(self.problem.init, mapped)
                for p in pred:
                    file.write(f"    ({p})\n")
                file.write("  )\n")

            # Write goals
            if self.problem.goals:
                file.write("(:goal\n  (and\n")
                pred = self.get_predicates(self.problem.goals, mapped)
                for p in pred:
                    file.write(f"    ({p})\n")
                file.write("  )\n)\n")

            # Close the parentheses
            file.write(")\n")


# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    domain = r"examples\Car\domain-2c.pddl"
    problem = r"examples\Car\problem-2c.pddl"
    # domain = r"examples\Blocks\domain-a1.pddl"
    # problem = r"examples\Blocks\problem-a1.pddl"
    satoma = MAtoSA(domain, problem)
    print('----------------------------')
    # print('Domain: ' + satoma.domain.__repr__())
    # dict of agent types and the number of agents to generate
    satoma.generate("outputs\\domain_3_agents.pddl", "outputs\\problem_3_agents.pddl")
