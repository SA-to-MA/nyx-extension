import re
import sys

class InitParser:
    def __init__(self, problem):
        '''
        Takes in path to domain file and problem file,
        '''
        self.problem = problem
        self.init_state = {} # { agent/object : [list of predicates] }
        self.objects = {} # { object_type : [list of objects] }
        self.agents = {} # { agent_type : [list of agents] }
        self.functions = {} # { function : value }
        self.goals = {} # { list of goals (functions/predicates and values) }

    ### PROBLEM FILE PARSER
    def parse_problem(self):
        try:
            tokens = self.scan_tokens(self.problem)
        except Exception as prob_error:
            print(
                "PDDL problem file error: missing file or malformed problem definition. \nCheck out \'README.md\' for help and usage instructions.\n")
            sys.exit(1)

        if type(tokens) is list and tokens.pop(0) == 'define':
            while tokens:
                group = tokens.pop(0)
                t = group.pop(0)
                if t == ':init':
                    self.parse_init(group)
                elif t == ':objects':
                    self.parse_objects(group)
                elif t == ':goal':
                    self.parse_goal(group)
        else:
            raise Exception('File ' + self.problem + ' does not match problem pattern')

    ### INIT SECTION PARSER
    def parse_init(self, group):
        """
        Parses the :init section of the problem file.
        Builds self.init_state as a dict: { object: {predicate/function: value} }
        """
        for entry in group:
            if isinstance(entry, list):
                if len(entry) == 3 and entry[0] == '=' and isinstance(entry[1], list):
                    # Example: (= (charge robot1) 80)
                    func_expr = entry[1]  # ['charge', 'robot1']
                    value = entry[2]
                    if len(func_expr) == 2:
                        func_name = func_expr[0]
                        obj_name = func_expr[1]
                        if obj_name not in self.init_state:
                            self.init_state[obj_name] = {}
                        self.init_state[obj_name][func_name] = float(value)
                    else:
                        func_name = func_expr[0]
                        self.functions[func_name] = float(value)
                else:
                    # Standard predicate, e.g., (at robot1 room1)
                    pred_name = entry[0]
                    args = entry[1:]

                    if not args:
                        continue  # Skip malformed

                    obj_name = args[0]
                    if obj_name not in self.init_state:
                        self.init_state[obj_name] = {}

                    if len(args) == 1:
                        # Boolean predicate
                        self.init_state[obj_name][pred_name] = True
                    elif len(args) == 2:
                        # Key-value
                        self.init_state[obj_name][pred_name] = args[1]
                    else:
                        # Multiple values: store as tuple
                        self.init_state[obj_name][pred_name] = tuple(args[1:])
            else:
                print(f"Warning: Skipped unexpected init entry: {entry}")

    ### TOKENIZER
    def scan_tokens(self, filename):
        with open(filename,'r') as f:
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

    ### OBJECTS SECTION PARSER
    def parse_objects(self, input_list):
        i = 0
        current_objects = []
        while i < len(input_list):
            if isinstance(input_list[i], list) and input_list[i][
                0] == ':private':  # if agents private list, process and add to agents
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
                    type = input_list[i + 1]
                    if type not in self.objects:
                        self.objects[type] = []
                    self.objects[type] += current_objects
                    current_objects = []
                    i += 1
                else:
                    current_objects.append(input_list[i])
            i += 1


    ### GOAL SECTION PARSER
    def parse_goal(self, group):
        """
        Parses the :goal section of the problem file.
        Builds self.goals as a dict: { object: {predicate/function: value} or function : value }
        """
        for entry in group:
            if isinstance(entry, list):
                if entry[0] == "and":
                    entry = entry[1]
                if len(entry) == 3 and entry[0] in ['=', "<", ">", "<=", ">="] and isinstance(entry[1], list):
                    # Example: (= (charge robot1) 80)
                    func_expr = entry[1]  # ['charge', 'robot1']
                    value = entry[2]
                    if len(func_expr) == 2:
                        func_name = func_expr[0]
                        obj_name = func_expr[1]
                        if obj_name not in self.goals:
                            self.goals[obj_name] = {}
                        self.goals[obj_name][func_name] = float(value)
                    else:
                        func_name = func_expr[0]
                        self.goals[func_name] = float(value)
                else:
                    # Standard predicate, e.g., (at robot1 room1)
                    pred_name = entry[0]
                    args = entry[1:]

                    if not args:
                        continue  # Skip malformed

                    obj_name = args[0]
                    if obj_name not in self.goals:
                        self.goals[obj_name] = {}

                    if len(args) == 1:
                        # Boolean predicate
                        self.goals[obj_name][pred_name] = True
                    elif len(args) == 2:
                        # Key-value
                        self.goals[obj_name][pred_name] = args[1]
                    else:
                        # Multiple values: store as tuple
                        self.goals[obj_name][pred_name] = tuple(args[1:])
            else:
                print(f"Warning: Skipped unexpected goals entry: {entry}")