import re
import sys

from syntax.action import Action


####### THIS IS GENERIC INIT PARSER FOR YOUR USAGE
####### SOME OF THE CODE IS TAKEN FROM ORIGINAL NYX CODE IN FILE PDDL.py
class InitParser:
    def __init__(self, problem):
        '''
        Takes in path to domain file and problem file,
        '''
        self.problem = problem
        self.init_state = {}

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
                    func_name = func_expr[0]
                    obj_name = func_expr[1]
                    if obj_name not in self.init_state:
                        self.init_state[obj_name] = {}
                    self.init_state[obj_name][func_name] = float(value)
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
                        # Boolean predicate: for example (running car1)
                        self.init_state[obj_name][pred_name] = True
                    elif len(args) == 2:
                        # Key-value style: (= (a car1) 0)
                        self.init_state[obj_name][pred_name] = args[1]
                    else:
                        # Multiple values: store as tuple
                        self.init_state[obj_name][pred_name] = tuple(args[1:])
            else:
                print(f"Warning: Skipped unexpected init entry: {entry}")

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

    def parse_problem(self):
        try:
            tokens = self.scan_tokens(self.problem)
        except Exception as prob_error:
            print(
                "PDDL problem file error: missing file or malformed problem definition. \nRun \'python nyx.py -h\' for help and usage instructions.\n")
            # print(constants.HELP_TEXT)
            sys.exit(1)

        if type(tokens) is list and tokens.pop(0) == 'define':
            while tokens:
                group = tokens.pop(0)
                t = group.pop(0)
                if t == ':init':
                    self.parse_init(group)
        else:
            raise Exception('File ' + self.problem + ' does not match problem pattern')



# if __name__ == "__main__":
#     # parser = InitParser("C:\\Users\\v-laftabi\Desktop\\Nyx\\nyx-extension\MA_PDDL\examples\Blocks\problem-a1.pddl")
#     parser = InitParser("C:\\Users\\v-laftabi\Desktop\\Nyx\\nyx-extension\MA_PDDL\examples\Car\problem.pddl")
#     parser.parse_problem()
#     print(parser.init_state)