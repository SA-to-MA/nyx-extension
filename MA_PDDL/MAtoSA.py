import itertools
import subprocess
from itertools import product
import re
import os
import glob
import shlex
from MA_PDDL.DeduplicateFunc import transform_pddl


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

    def generate_action_combinations(self, parsed_actions, agents_dict):
        """
        Generate all possible combinations of actions based on the number of agents of each type.

        :param parsed_actions: Dictionary of actions with {action_name: {'params': ..., 'pre': ..., 'effects': ...}}.
        :return: List of all possible action combinations.
        """
        # create dict of agents count of agent type
        agent_type_counts = {}
        for agent_type, agents in agents_dict: # Yarin added
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
        groups = {} # Yarin added
        i = 0
        value = []
        while i < len(data):
            if data[i] == "-":
                current_category = data[i + 1]
                if current_category not in groups:
                    groups[current_category] = []
                groups[current_category] += value
                value = []
                i += 1
            else:
                value.append(data[i])
            i += 1

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
                if len(action['pre']) > 0:
                    if action['pre'][0] == "and":
                        action['pre'].pop(0)
                        unified_pre.extend(action['pre'])
                    else:
                        unified_pre.append(action['pre'])
                if len(action['effects']) > 0:
                    if action['effects'][0] == "and":
                        action['effects'].pop(0)
                        unified_effects.extend(action['effects'])
                    else:
                        unified_effects.append(action['effects'])
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
        possible_combinations = []
        for agent_type, agents in self.agents.items():
            for i in range(1, len(agents) + 1):
                possible_combinations += self.generate_action_combinations(
                    parsed_act, {agent_type: agents[:i]}.items()
                )
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
        current_objects = []
        while i < len(input_list):
            if isinstance(input_list[i], list) and input_list[i][0] == ':private': # if agents private list, process and add to agents
                private_list = input_list[i][1:]
                agents_list = " ".join(private_list)
                filtered = re.findall(r"([\w\s]+)-\s*([\w]+)", agents_list)
                for item_value, item_type in filtered:
                    for value in item_value.strip().split():
                        if item_type not in self.agents:
                            self.agents[item_type] = []
                        self.agents[item_type].append(value)
            else:
                if input_list[i] == "-":
                    type = input_list[i+1]
                    if type not in self.objects:
                        self.objects[type] = []
                    self.objects[type] += current_objects
                    current_objects = []
                    i+=1
                else:
                    current_objects.append(input_list[i])
            i+=1



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

class SolveController:
    def __init__(self, domain_file, problem_file, domain_name, flags):
        self.domain = os.path.abspath(domain_file)
        self.problem = os.path.abspath(problem_file)
        self.domain_name = domain_name
        self.flags = self.process_flags(flags)
        self.plan = self.solve()

    def process_flags(self, flags):
        """Checks if flags is a file, reads its content if so, otherwise returns the default flags."""
        # if no flags, return default
        if len(flags) == 0:
            return "-t:1 -pt"
        elif os.path.isfile(flags):  # Check if flags is a path to a file
            try:
                with open(flags, 'r') as file:
                    return file.read().strip()  # Read and clean up whitespace
            except Exception as e:
                print(f"Error reading flags file: {e}")
                return "-t:1 -pt"  # Return default if file read fails
        return flags  # Return flags as is if not a file

    def solve(self):
        """
        solves the problem using nyx and saves the solution path
        """

        if self.domain_name == "Sleeping Beauty":
            self.plan = run_nyx(self.domain, self.problem, self.flags)
        else:
            satoma = MAtoSA(self.domain, self.problem)
            # Get absolute path for outputs directory
            output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "MA_PDDL", f"outputs/{self.domain_name}"))
            os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

            # Define the new output files with correct absolute paths
            new_domain = os.path.join(output_dir, "domain.pddl")
            new_problem = os.path.join(output_dir, "problem.pddl")

            # generate the combined pddl files
            satoma.generate(new_domain, new_problem)
            # remove duplicates of functions
            transform_pddl(new_domain, new_domain)
            # solve
            self.plan = run_nyx(new_domain, new_problem, self.flags)
        return self.plan

    def getPlanFile(self):
        """
        returns the path to the plan. if no path, will be none
        """
        return self.plan

    def getParsedPlan(self):
        """
        Return a parsed solution for display.
        Supports visualization for specific domains.
        """
        try:
            with open(self.plan, "r") as file:
                plan_text = file.read()

            # Early check: verify that the plan has time stamps
            if not re.search(r'^\s*\d+(\.\d+)?:', plan_text, re.MULTILINE):
                return "Solution not found"

            # ----------------- BLOCKS DOMAIN -----------------
            if self.domain_name == "Blocks":
                action_mapping = {
                    'no-op_agent': ['agent'],
                    'stack': ['agent', 'block', 'block'],
                    'unstack': ['agent', 'block', 'block'],
                    'pick-up': ['agent', 'block'],
                    'put-down': ['agent', 'block']
                }
                parsed_lines = []
                for line in plan_text.strip().split("\n"):
                    if not line.strip():
                        continue
                    parts = re.split(r'\s+', line.strip())
                    if len(parts) < 3:
                        continue  # Skip invalid lines
                    time = parts[0].strip(':')
                    actions_combined = parts[1]
                    arguments = parts[2:-1]  # Exclude cost/metadata
                    actions = actions_combined.split("&")
                    parsed_action_descriptions = []
                    arg_index = 0
                    for action in actions:
                        if action in action_mapping:
                            roles = action_mapping[action]
                            assigned_args = [f"{roles[i]} {arguments[arg_index + i]}" for i in range(len(roles))]
                            parsed_action_descriptions.append(f"{action} - " + ", ".join(assigned_args))
                            arg_index += len(roles)
                    parsed_lines.append(f"{time}: " + ", ".join(parsed_action_descriptions))
                return "\n".join(parsed_lines)

            # ----------------- CAR DOMAIN -----------------
            elif self.domain_name == "Car":
                from MA_PDDL import MAtoSA  # Ensure import inside method to avoid circular import
                satoma = MAtoSA(self.domain, self.problem)
                problem_tokens = satoma.scan_tokens(self.problem)
                for token in problem_tokens:
                    if token[0] == ':objects':
                        satoma.process_objects_and_agents(token[1:])
                        break

                car_agents = []
                for agent_type, names in satoma.agents.items():
                    if agent_type.lower() in ["car", "vehicle"]:
                        car_agents.extend(names)
                if not car_agents:
                    car_agents = ["car1", "car2"]  # Fallback

                parsed_lines = []
                for line in plan_text.strip().split("\n"):
                    if not line.strip():
                        continue
                    parts = re.split(r'\s+', line.strip())
                    if len(parts) < 2:
                        continue  # Skip invalid lines
                    time = parts[0].strip(':')
                    actions = parts[1].split("&")
                    action_texts = [f"{action} - {car}" for action, car in zip(actions, car_agents)]
                    parsed_lines.append(f"{time}: " + ", ".join(action_texts))
                return "\n".join(parsed_lines)

            # ----------------- DEFAULT -----------------
            else:
                return plan_text

        except Exception as e:
            print(f"[Error] Failed to parse plan: {e}")
            return "Solution not found"


def run_nyx(domain, problem, flags):
    """Run the Nyx planner and generate a plan."""
    flags_list = shlex.split(flags)
    command = [
        "python",
        os.path.join(os.path.dirname(__file__), "..", "nyx.py"),
        os.path.abspath(domain),
        os.path.abspath(problem),
    ] + flags_list
    print(f"Executing command: {' '.join(command)}")  # Debugging print
    result = subprocess.run(command, text=True, capture_output=True, encoding='utf-8')
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    # Get the directory where the problem file is located
    problem_dir = os.path.dirname(os.path.abspath(problem))
    # Dynamically define the expected output directory
    output_dir = os.path.join(problem_dir, "plans")
    # Ensure the output directory exists before execution
    os.makedirs(output_dir, exist_ok=True)
    # Find the most recent plan file in the dynamically determined output directory
    plan_files = glob.glob(os.path.join(output_dir, "*.pddl"))  # Find all PDDL plan files
    if not plan_files:
        raise FileNotFoundError(f"No plan files found in {output_dir} after running Nyx.")
    # Get the latest plan file based on modification time
    latest_plan = max(plan_files, key=os.path.getmtime)
    return latest_plan  # Return the correct dynamically found plan file


# EXAMPLE OF USAGE
# if __name__ == "__main__":
#     solve = SolveController("examples/Car/domain.pddl", "examples/Car/problem.pddl", "Car", "examples/Car/config.pddl")
    # solve.solve()
