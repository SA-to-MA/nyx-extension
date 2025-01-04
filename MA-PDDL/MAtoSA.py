import itertools
from itertools import product
import re


class MAtoSA:
    def __init__(self, ma_domain, ma_problem):
        self.ma_domain_file = ma_domain
        self.ma_problem_file = ma_problem
        self.agents = {}
        self.actions = {}
        self.objects = {}

    def scan_tokens(self, file):
        with open(file,'r') as f:
            # Remove single line comments
            str = re.sub(r';.*$', '', f.read(), flags=re.MULTILINE).lower()
        # Tokenize
        stack = []
        list = []
        for t in re.findall(r'[()]|[^\s()]+', str):
            if t == '(':
                stack.append(list)
                list = []
            elif t == ')':
                if stack:
                    l = list
                    list = stack.pop()
                    list.append(l)
                else:
                    raise Exception('Missing open parentheses')
            else:
                list.append(t)
        if stack:
            raise Exception('Missing close parentheses')
        if len(list) != 1:
            raise Exception('Malformed expression')
        return list[0]

    def parse_actions(self, tokens):
        # actions dictionary of actions by agent type
        actions = {}
        # iterate all tokens
        for lst in tokens:
            # if action, parse action
            if lst[0] == ':action':
                name = lst[1]
                params, pre, effects = [], [], []
                for i in range(2, len(lst), 2):
                    if lst[i] == ':parameters':
                        params = lst[i+1]
                    elif lst[i] == ":precondition":
                        pre = lst[i+1]
                    elif lst[i] == ":effect":
                        effects = lst[i+1]
                # add parsed action to dictionary
                actions[name] = {'params': params, 'pre': pre, 'effects': effects}
        # return all parsed actions
        return actions

    def generate_action_combinations(self, parsed_actions):
        """
        Generate all possible combinations of actions based on the number of agents of each type.

        :param parsed_actions: Dictionary of actions with {action_name: {'params': ..., 'pre': ..., 'effects': ...}}.
        :return: List of all possible action combinations.
        """
        # create dict of agents count of agent type
        agent_type_counts = {}
        for agent_type, agents in self.agents.items():
            agent_type_counts[agent_type] = len(agents)
        # Step 1: Group actions by agent type
        actions_by_agent_type = {}
        valid_agent_types = set(agent_type_counts.keys())  # Use known agent types as a reference
        for action, details in parsed_actions.items():
            # Extract the type of the agent
            agent_type = None
            for i in range(len(details['params']) - 1):
                if details['params'][i] == '-' and i > 0:
                    param_type = details['params'][i + 1]
                    if param_type in valid_agent_types:  # Check if the param type is a valid agent type
                        agent_type = param_type
                        break
            if agent_type:
                if agent_type not in actions_by_agent_type:
                    actions_by_agent_type[agent_type] = []
                actions_by_agent_type[agent_type].append(action)

        # Step 2: Generate combinations for each agent type
        action_combinations_by_agent_type = {}
        for agent_type, actions in actions_by_agent_type.items():
            count = agent_type_counts.get(agent_type, 0)
            # Create all combinations with repetition for the given number of agents
            action_combinations_by_agent_type[agent_type] = list(product(actions, repeat=count))

        # Step 3: Combine across agent types
        all_combinations = list(product(*action_combinations_by_agent_type.values()))
        # eliminate redundancies
        unique_combinations = list(set(tuple(sorted(comb[0])) for comb in all_combinations))
        all_combinations = unique_combinations

        # Step 4: Assign unique parameter names for each action and update preconditions/effects
        def update_references(expression, param_mapping):
            """
            Recursively update parameter references in the given expression based on param_mapping.
            :param expression: The nested list or string to update.
            :param param_mapping: A dictionary mapping old parameters to new ones.
            :return: Updated expression with parameters replaced.
            """
            if isinstance(expression, list):
                return [update_references(item, param_mapping) for item in expression]
            elif isinstance(expression, str) and expression in param_mapping:
                # Replace if the string matches a parameter in the mapping
                return param_mapping[expression]
            return expression

        final_combinations = []
        for combo in all_combinations:
            flat_combo = []
            action_index = 1  # Track the action index for unique parameter naming
            for action in combo:
                # Get the original action details
                action_details = parsed_actions[action]
                # Assign unique parameter names and create a mapping
                unique_params = [
                    f"{param}{action_index}" if param.startswith('?') else param
                    for param in action_details['params']
                ]
                param_mapping = {
                    original: unique
                    for original, unique in zip(action_details['params'], unique_params)
                }

                # Update preconditions, effects, and other relevant structures
                updated_pre = update_references(action_details['pre'], param_mapping)
                updated_effects = update_references(action_details['effects'], param_mapping)

                # Construct the unique action structure
                unique_action = {
                    'name': action,
                    'params': unique_params,
                    'pre': updated_pre,
                    'effects': updated_effects
                }
                flat_combo.append(unique_action)
                action_index += 1
            final_combinations.append(flat_combo)

        return final_combinations

    def generate_constraints(self, data):
        # Group objects by type
        groups = {}
        for i in range(0, len(data), 3):  # Process every triplet
            obj = data[i]
            obj_type = data[i + 2]
            if obj_type not in groups:
                groups[obj_type] = []
            groups[obj_type].append(obj)

        # Generate preconditions
        preconditions = []
        for obj_type, objects in groups.items():
            for i in range(len(objects)):
                for j in range(i + 1, len(objects)):
                    dif_cond = [f'dif_{obj_type}', objects[i], objects[j]]
                    preconditions.append(dif_cond)

        return preconditions


    def unify_combinations(self, combinations):
        """
        Unify parameters, preconditions, and effects for each combination of actions.
        :param combinations: List of combinations, where each combination is a list of action dicts.
        :return: List of unified actions.
        """
        unified_actions = []
        for combination in combinations:
            unified_params = []
            unified_pre = []
            unified_effects = []
            for action in combination:
                # Merge parameters, preconditions and effects
                unified_params.extend(action['params'])
                unified_pre.extend(action['pre'][1:])
                unified_effects.extend(action['effects'][1:])
            # get constraints
            unified_pre.extend(self.generate_constraints(unified_params))
            # Create the unified action
            unified_action = {
                'name': '&'.join([action['name'] for action in combination]),
                'params': unified_params,
                'pre': unified_pre,
                'effects': unified_effects
            }
            unified_actions.append(unified_action)
        return unified_actions

    def generate_actions(self, tokens):
        parsed_act = self.parse_actions(tokens)
        for agent in self.agents.keys():
            parsed_act[f"no-op_{agent}"] = {'params': ['?a', '-', agent], 'pre': [], 'effects': []}
        possible_combinations = self.generate_action_combinations(parsed_act)
        self.actions = self.unify_combinations(possible_combinations)

    def process_expression(self, expression):
        """
        :param expression: a nested expression to be processed
        :return: a string of processed expression
        """
        uni_exp = ""
        for exp in expression:
            if isinstance(exp, list):
                proc_exp = self.process_expression(exp)
                uni_exp += "(" + proc_exp + ")"
            else:
                uni_exp += f"{exp} "
        return uni_exp

    def process_objects_and_agents(self, input_list):

        # Iterate through the input list to classify the items
        i = 0
        while i < len(input_list):
            if isinstance(input_list[i], list) and input_list[i][0] == ':private':
                private_list = input_list[i]
                for k in range(1, len(private_list), 3):
                    item_value = private_list[k]
                    item_type = private_list[k + 2]
                    if item_type not in self.agents:
                        self.agents[item_type] = []
                    self.agents[item_type].append(item_value)
                i+=1
            else:
                item_value = input_list[i]
                item_type = input_list[i + 2]
                if item_type not in self.objects:
                    self.objects[item_type] = []
                self.objects[item_type].append(item_value)
            i+=3



    #-----------------------------------------------
    # Generate SA-PDDL+ files
    #-----------------------------------------------
    def generate(self, output_domain, output_problem):
        """
        Generate all combinations and write the corresponding SA format file.
        """
        # get agents from problem file (should be defined under :private in objects)
        # and write new problem
        self.write_problem(output_problem)
        domain_tokens = self.scan_tokens(self.ma_domain_file) # get tokens of domain
        self.generate_actions(domain_tokens) # replace token with real names
        self.write_domain(output_domain, domain_tokens)

    def write_domain(self, output, domain_tokens):
        '''
        :param file_name: the name of the output file
        :return: Write the MA problem in syntax of SA problem
        '''
        with open(output, "w") as file:
            # write definition of domain
            if domain_tokens[0] == "define":
                domain_tokens.pop(0)
                domain_name = " ".join(domain_tokens.pop(0))
                file.write(f"(define ({domain_name})\n")
            # iterate tokens and write them
            for token in domain_tokens:
                # if predicates section, check for private predicates and make them public
                if token[0] == ':predicates':
                    if isinstance(token[len(token)-1], list) and token[len(token)-1][0] == ":private":
                        private = token.pop(len(token)-1)
                        private.pop(0)
                        token.extend(private)
                    for agent_type in self.agents.keys():
                        token.append([f"dif_{agent_type} ?ob1 - {agent_type} ?ob2 - {agent_type}"])
                    for obj_type in self.objects.keys():
                        token.append([f"dif_{obj_type} ?ob1 - {obj_type} ?ob2 - {obj_type}"])
                # if not action, write to file
                if token[0] != ':action':
                    exp = self.process_expression(token)
                    file.write(f"({exp})\n")
            # iterate all actions
            for action in self.actions:
                # write action name
                file.write(f"(:action {action['name']}\n")
                # write parameters
                unified_params = " ".join(action['params'])
                file.write(f":parameters ({unified_params})\n")
                # write preconditions
                file.write(":precondition (and\n")
                for pred in action['pre']:
                    exp = self.process_expression(pred)
                    file.write(f"({exp})\n")
                file.write(')\n')
                # write effects
                file.write(":effect (and\n")
                for eff in action['effects']:
                    exp = self.process_expression(eff)
                    file.write(f"({exp})\n")
                file.write(')\n')
                file.write(')\n')
            file.write(")\n")

    def write_problem(self, output_filename):
        problem = self.scan_tokens(self.ma_problem_file)
        with open(output_filename, "w") as file:
            if problem[0] == "define":
                file.write(f'(define ')
                problem.pop(0)
            else:
                raise Exception("Problem not defined correctly")
            for token in problem:
                if token[0] == ':objects':
                    token.pop(0)
                    self.process_objects_and_agents(token)
                    # write objects
                    file.write(f"(:objects ")
                    for agent_type, agent_value in self.agents.items():
                        for agent in agent_value:
                            file.write(f"{agent} - {agent_type}\n")
                    for obj_type, obj_value in self.objects.items():
                        for obj in obj_value:
                            file.write(f"{obj} - {obj_type}\n")
                    file.write(f")\n")
                else:
                    if token[0] == ":init":
                        permutations = {}
                        # add dif predicate
                        for agent_type, agent_value in self.agents.items():
                            permutations[agent_type] = list(itertools.permutations(agent_value, 2))
                        for obj_type, obj_value in self.objects.items():
                            permutations[obj_type] = list(itertools.permutations(obj_value, 2))
                        for type, list_of_perms in permutations.items():
                            for perm in list_of_perms:
                                token.append([f"dif_{type} {perm[0]} {perm[1]}"])
                    exp = self.process_expression(token)
                    file.write(f"({exp})\n")
            file.write(')')


# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    domain = r"examples\Car\domain-2c.pddl"
    problem = r"examples\Car\problem-2c.pddl"
    # domain = r"examples\Car\domain-2c.pddl"
    # problem = r"examples\Car\problem-2c.pddl"
    satoma = MAtoSA(domain, problem)
    print('----------------------------')
    # print('Domain: ' + satoma.domain.__repr__())
    # dict of agent types and the number of agents to generate
    satoma.generate("outputs\\WithObjectsConversion\\Car\\domain.pddl", "outputs\\WithObjectsConversion\\Car\\problem.pddl")
