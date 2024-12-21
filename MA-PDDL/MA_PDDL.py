import re
import sys
import copy

from syntax.action import Action
from syntax.event import Event
from syntax.process import Process
import syntax.constants as constants
from PDDL import PDDLDomain, PDDLProblem

class MAPDDLDomain(PDDLDomain):
    def __init__(self, **kwargs):
        # call the parent class initializer
        super().__init__(**kwargs)
        # MA-specific properties
        self.agents = kwargs.get('agents', dict())
        self.objects = kwargs.get('objects', dict())

    def __repr__(self):
        return (
            f"MAPDDLDomain(name={self.name}, requirements={self.requirements}, "
            f"types={self.types}, predicates={self.predicates}, functions={self.functions}, "
            f"constants={self.constants}, processes={self.processes}, actions={self.actions}, "
            f"events={self.events}, agents={self.agents}, objects={self.objects}"
        )

class MAPDDLProblem(PDDLProblem):
    def __init__(self, **kwargs):
        # call the parent class initializer
        super().__init__(**kwargs)
        # MA-specific properties
        self.agents = kwargs.get('agents', dict())

class MAPDDLParser:

    SUPPORTED_REQUIREMENTS = [':strips', ':adl', ':negative-preconditions', ':typing', ':time', ':fluents', ':timed-initial-literals', ':durative-actions', ':duration-inequalities', ':continuous-effects', ':disjunctive-preconditions', ':semantic-attachment', ':conditional-effects']

    def __init__(self, domain_file, problem_file):
        self.domain = MAPDDLDomain()
        self.problem = MAPDDLProblem()
        self.parse_domain(domain_file)
        self.parse_problem(problem_file)

    #-----------------------------------------------
    # Tokens
    #-----------------------------------------------

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

    #-----------------------------------------------
    # Parse domain
    #-----------------------------------------------

    def parse_domain(self, domain_filename):

        try:
            tokens = self.scan_tokens(domain_filename)
        except Exception as dom_error:
            print("PDDL domain file error: missing file or malformed domain definition. \nRun \'python nyx.py -h\' for help and usage instructions.\n")
            # print(constants.HELP_TEXT)
            sys.exit(1)

        if type(tokens) is list and tokens.pop(0) == 'define':
            self.domain.name = 'unknown'
            while tokens:
                group = tokens.pop(0)
                t = group.pop(0)
                if t == 'domain':
                    self.domain.name = group[0]
                elif t == ':requirements':
                    for req in group[:]:  # Iterate over a copy of the list to modify the original group
                        if req == ':time':
                            constants.TEMPORAL_DOMAIN = True
                        if req == ':semantic-attachment':
                            constants.SEMANTIC_ATTACHMENT = True
                        if req not in self.SUPPORTED_REQUIREMENTS:  # Remove the unsupported requirement
                            group.remove(req)
                        if req == ':timed-initial-literals' or req == ':timed-initial-fluents':
                            constants.CONTAINS_TIL_TIF = True
                    self.domain.requirements = group
                elif t == ':constants':
                    self.parse_constants(group, t)
                elif t == ':predicates':
                    self.parse_predicates(group)
                elif t == ':functions':
                    self.parse_functions(group)
                elif t == ':types':
                    self.parse_types(group)
                elif t == ':action':
                    self.parse_action(group)
                elif t == ':durative-action':
                    constants.TEMPORAL_DOMAIN = True
                    self.parse_durative_action(group)
                elif t == ':event':
                    self.parse_event(group)
                elif t == ':process':
                    self.parse_process(group)
                else: self.parse_domain_extended(t, group)
        else:
            raise Exception('File ' + domain_filename + ' does not match domain pattern')

    def parse_domain_extended(self, t, group):
        print(str(t) + ' is not recognized in domain')

    #-----------------------------------------------
    # Parse hierarchy
    #-----------------------------------------------

    def parse_hierarchy(self, group, structure, name, redefine):
        list = []
        while group:
            if redefine and group[0] in structure:
                raise Exception('Redefined supertype of ' + group[0])
            elif group[0] == '-':
                if not list:
                    raise Exception('Unexpected hyphen in ' + name)
                group.pop(0)
                type = group.pop(0)
                if not type in structure:
                    structure[type] = []
                structure[type] += list
                list = []
            else:
                list.append(group.pop(0))
        if list:
            if not 'object' in structure:
                structure['object'] = []
            structure['object'] += list

    #-----------------------------------------------
    # Parse constants
    #-----------------------------------------------

    def parse_constants(self, group, name):
        self.parse_hierarchy(group, self.domain.constants, name, False)

    #-----------------------------------------------
    # Parse objects
    #-----------------------------------------------

    def parse_objects(self, group, name):
        # Separate the :private list which contains the agents
        private_list = [
            item for item in group if isinstance(item, list) and item[0] == ':private'
        ]
        # Filter out :private from the group
        filtered_group = [
            item for item in group if not (isinstance(item, list) and item[0] == ':private')
        ]
        # Send the filtered group to parse_hierarchy
        self.parse_hierarchy(filtered_group, self.problem.objects, name, False)
        # If there are private lists, pass them to another function to process
        for private_item in private_list:
            if private_item[0] == ":private":
                private_item.pop(0)
            self.parse_agents(private_item)

    #-----------------------------------------------
    # Parse agents
    #-----------------------------------------------
    def parse_agents(self, agents):
        list = []
        while agents:
            if agents[0] == '-':
                if not list:
                    raise Exception('Unexpected hyphen in private')
                agents.pop(0)
                type = agents.pop(0)
                if not type in self.problem.agents:
                    self.problem.agents[type] = []
                self.problem.agents[type] += list
                list = []
            else:
                list.append(agents.pop(0))
        if list:
            raise Exception("Undefined agent in private section")

    # -----------------------------------------------
    # Parse types
    # -----------------------------------------------

    def parse_types(self, group):
        self.parse_hierarchy(group, self.domain.types, 'types', True)

    #-----------------------------------------------
    # Parse predicates
    #-----------------------------------------------

    def parse_predicates(self, group):
        for pred in group:
            predicate_name = pred.pop(0)
            # if private predicates, parse them separately
            if predicate_name == ":private":
                if len(pred) == 0: # if private defined but no private predicates present, raise error
                    raise Exception('Private predicates section defined but is empty')
                self.parse_predicates(pred) # parse private predicates and break after that
                continue
            if predicate_name in self.domain.predicates:
                raise Exception('Predicate ' + predicate_name + ' redefined')
            arguments = {}
            untyped_variables = []
            while pred:
                t = pred.pop(0)
                if t == '-':
                    if not untyped_variables:
                        raise Exception('Unexpected hyphen in predicates')
                    type = pred.pop(0)
                    while untyped_variables:
                        arguments[untyped_variables.pop(0)] = type
                else:
                    untyped_variables.append(t)
            while untyped_variables:
                arguments[untyped_variables.pop(0)] = 'object'
            self.domain.predicates[predicate_name] = arguments

    # -----------------------------------------------
    # Parse functions
    # -----------------------------------------------

    def parse_functions(self, group):
        for func in group:
            function_name = func.pop(0)
            if function_name in self.domain.functions:
                raise Exception('Function ' + function_name + ' redefined')
            arguments = {}
            untyped_variables = []
            while func:
                t = func.pop(0)
                if t == '-':
                    if not untyped_variables:
                        raise Exception('Unexpected hyphen in functions')
                    type = func.pop(0)
                    while untyped_variables:
                        arguments[untyped_variables.pop(0)] = type
                else:
                    untyped_variables.append(t)
            while untyped_variables:
                arguments[untyped_variables.pop(0)] = 'object'
            self.domain.functions[function_name] = arguments

    #-----------------------------------------------
    # Parse action
    #-----------------------------------------------

    def parse_action(self, group):
        name = group.pop(0)
        if not type(name) is str:
            raise Exception('Action without name definition')
        for act in self.domain.actions:
            if act.name == name:
                raise Exception('Action ' + name + ' redefined')
        parameters = []
        preconditions = []
        effects = []
        extensions = None
        while group:
            t = group.pop(0)
            if t == ':parameters':
                if not type(group) is list:
                    raise Exception('Error with ' + name + ' parameters')
                parameters = []
                untyped_parameters = []
                p = group.pop(0)
                while p:
                    t = p.pop(0)
                    if t == '-':
                        if not untyped_parameters:
                            raise Exception('Unexpected hyphen in ' + name + ' parameters')
                        ptype = p.pop(0)
                        while untyped_parameters:
                            parameters.append([untyped_parameters.pop(0), ptype])
                    else:
                        untyped_parameters.append(t)
                while untyped_parameters:
                    parameters.append([untyped_parameters.pop(0), 'object'])
            elif t == ':precondition':
                # preconditions = group.pop(0)
                self.split_predicates(group.pop(0), preconditions, name, ' preconditions')
            elif t == ':effect':
                # effects = group.pop(0)
                self.split_predicates(group.pop(0), effects, name, ' effects')
            else: extensions = self.parse_action_extended(t, group)
        self.domain.actions.append(Action(name, parameters, preconditions, effects))

    def parse_action_extended(self, t, group):
        print(str(t) + ' is not recognized in action')

    # -----------------------------------------------
    # Parse durative-action
    # -----------------------------------------------

    def parse_durative_action(self, group):
        name = group.pop(0)
        if not type(name) is str:
            raise Exception('Durative-Action without name definition')
        for act in self.domain.actions:
            if act.name == name:
                raise Exception('Durative-Action ' + name + ' redefined')
        parameters_start = []
        parameters_process = []
        parameters_end = []
        preconditions_start = []
        preconditions_process = []
        preconditions_end = []
        effects_start = []
        effects_process = []
        effects_end = []
        extensions = None
        while group:
            t = group.pop(0)
            if t == ':parameters':
                if not type(group) is list:
                    raise Exception('Error with ' + name + ' parameters')
                parameters = []
                untyped_parameters = []
                p = group.pop(0)
                while p:
                    t = p.pop(0)
                    if t == '-':
                        if not untyped_parameters:
                            raise Exception('Unexpected hyphen in ' + name + ' parameters')
                        ptype = p.pop(0)
                        while untyped_parameters:
                            parameters.append([untyped_parameters.pop(0), ptype])
                    else:
                        untyped_parameters.append(t)
                while untyped_parameters:
                    parameters.append([untyped_parameters.pop(0), 'object'])
            elif t == ':duration':
                duration_condition = group.pop(0)

                # generate auxiliary timing variables + add them to domain definition
                expanded_params = []
                for param_and_type in parameters:
                        expanded_params = expanded_params + [param_and_type[0],'-',param_and_type[1]]
                aux_clock_activated_predicate = ['{}_process_clock_activated'.format(name)] + [item[0] for item in parameters]
                self.parse_predicates([['{}_process_clock_activated'.format(name)] + expanded_params])
                aux_clock_numeric = ['{}_process_clock'.format(name)] + [item[0] for item in parameters]
                self.parse_functions([['{}_process_clock'.format(name)] + expanded_params])

                aux_end_clock_reset = ['assign', aux_clock_numeric, '0.0']
                aux_start_clock_activate = aux_clock_activated_predicate
                aux_end_clock_deactivate = ['not', aux_clock_activated_predicate]

                #
                duration_condition[duration_condition.index('?duration')] =  aux_clock_numeric
                self.split_predicates(duration_condition, preconditions_end, name, ' preconditions')

                # increase durative-action process clock with each time tick
                aux_process_clock_effect = ['increase' , aux_clock_numeric, ['*', '#t', '1.0']]
                self.split_predicates(aux_start_clock_activate, preconditions_process, name, ' preconditions')
                self.split_predicates(aux_process_clock_effect, effects_process, name, ' effects')

                # deactivate and reset durative-action process clock from end snap action (+ process activated precondition)
                self.split_predicates(aux_start_clock_activate, preconditions_end, name, ' preconditions')
                self.split_predicates(aux_end_clock_deactivate, effects_end, name, ' effects')
                self.split_predicates(aux_end_clock_reset, effects_end, name, ' effects')

                # activate durative-action process from start snap action (and precondition to prevent re-starting an already-running instance).

                self.split_predicates(aux_start_clock_activate, effects_start, name, ' effects')
                self.split_predicates(aux_end_clock_deactivate, preconditions_start, name, ' preconditions')

            elif t == ':condition':
                # preconditions = group.pop(0)
                self.split_durative_predicates(group.pop(0), [preconditions_start, preconditions_process, preconditions_end], name, ' preconditions')
            elif t == ':effect':
                # effects = group.pop(0)
                self.split_durative_predicates(group.pop(0), [effects_start, effects_process, effects_end], name, ' effects')
            else:
                extensions = self.parse_action_extended(t, group)

        ###
        #   PARSE and PROCESS DURATION INFORMATION:
        #       timing process, at_end timing_process precondition, at_end timing reset, ...
        #
        #   - Investigate whether durative-actions must be ended for a plan to be valid.
        ###


        self.domain.actions.append(Action(name+"_durative_start", parameters, preconditions_start, effects_start, happening_type="snap_start"))
        self.domain.processes.append(Process(name+"_durative_process", parameters, preconditions_process, effects_process, happening_type="durative_action_process"))
        self.domain.actions.append(Action(name+"_durative_end", parameters, preconditions_end, effects_end, happening_type="snap_end"))

    def parse_durative_action_extended(self, t, group):
        print(str(t) + ' is not recognized in durative-action')

    # -----------------------------------------------
    # Parse event
    # -----------------------------------------------

    def parse_event(self, group):
        name = group.pop(0)
        if not type(name) is str:
            raise Exception('Event without name definition')
        for eve in self.domain.events:
            if eve.name == name:
                raise Exception('Event ' + name + ' redefined')
        parameters = []
        preconditions = []
        effects = []
        extensions = None
        while group:
            t = group.pop(0)
            if t == ':parameters':
                if not type(group) is list:
                    raise Exception('Error with ' + name + ' parameters')
                parameters = []
                untyped_parameters = []
                p = group.pop(0)
                while p:
                    t = p.pop(0)
                    if t == '-':
                        if not untyped_parameters:
                            raise Exception('Unexpected hyphen in ' + name + ' parameters')
                        ptype = p.pop(0)
                        while untyped_parameters:
                            parameters.append([untyped_parameters.pop(0), ptype])
                    else:
                        untyped_parameters.append(t)
                while untyped_parameters:
                    parameters.append([untyped_parameters.pop(0), 'object'])
            elif t == ':precondition':
                self.split_predicates(group.pop(0), preconditions, name, ' preconditions')
            elif t == ':effect':
                self.split_predicates(group.pop(0), effects, name, ' effects')
            else:
                extensions = self.parse_event_extended(t, group)
        self.domain.events.append(Event(name, parameters, preconditions, effects, extensions))

    def parse_event_extended(self, t, group):
        print(str(t) + ' is not recognized in event')

    # -----------------------------------------------
    # Parse process
    # -----------------------------------------------

    def parse_process(self, group):
        name = group.pop(0)
        if not type(name) is str:
            raise Exception('Process without name definition')
        for pro in self.domain.processes:
            if pro.name == name:
                raise Exception('Process ' + name + ' redefined')
        parameters = []
        preconditions = []
        effects = []
        extensions = None
        while group:
            t = group.pop(0)
            if t == ':parameters':
                if not type(group) is list:
                    raise Exception('Error with ' + name + ' parameters')
                parameters = []
                untyped_parameters = []
                p = group.pop(0)
                while p:
                    t = p.pop(0)
                    if t == '-':
                        if not untyped_parameters:
                            raise Exception('Unexpected hyphen in ' + name + ' parameters')
                        ptype = p.pop(0)
                        while untyped_parameters:
                            parameters.append([untyped_parameters.pop(0), ptype])
                    else:
                        untyped_parameters.append(t)
                while untyped_parameters:
                    parameters.append([untyped_parameters.pop(0), 'object'])
            elif t == ':precondition':
                self.split_predicates(group.pop(0), preconditions, name, ' preconditions')
            elif t == ':effect':
                self.split_predicates(group.pop(0), effects, name, ' effects')
            else:
                extensions = self.parse_process_extended(t, group)
        self.domain.processes.append(Process(name, parameters, preconditions, effects, extensions))

    def parse_process_extended(self, t, group):
        print(str(t) + ' is not recognized in process')

    #-----------------------------------------------
    # Parse problem
    #-----------------------------------------------

    def parse_problem(self, problem_filename):
        def frozenset_of_tuples(data):
            return frozenset([tuple(t) for t in data])

        try:
            tokens = self.scan_tokens(problem_filename)
        except Exception as prob_error:
            print("PDDL problem file error: missing file or malformed problem definition. \nRun \'python nyx.py -h\' for help and usage instructions.\n")
            # print(constants.HELP_TEXT)
            sys.exit(1)

        if type(tokens) is list and tokens.pop(0) == 'define':
            self.problem.name = 'unknown'
            while tokens:
                group = tokens.pop(0)
                t = group.pop(0)
                if t == 'problem':
                    self.problem.name = group[0]
                elif t == ':domain':
                    if self.domain.name != group[0]:
                        raise Exception('Different domain specified in problem file')
                elif t == ':requirements':
                    pass # Ignore requirements in problem, parse them in the domain
                elif t == ':objects':
                    self.parse_objects(group, t)
                elif t == ':init':
                    self.problem.init = copy.copy(group)
                    if (constants.CONTAINS_TIL_TIF):
                        til_index = 0
                        for init_var in group:
                            if init_var[0] == 'at' and len(init_var)==3:
                                # construct a time-based event for the TIL/TIF
                                self.parse_predicates([['TIL_{}_triggered'.format(til_index)]])
                                # self.parse_event(['TIL_{}'.format(til_index), ':parameters', [], ':precondition', ['and', ['not',['TIL_{}_triggered'.format(til_index)]], ['>=', 'state.time', init_var[1]]], ':effect', ['and', ['TIL_{}_triggered'.format(til_index)], init_var[2]]])
                                self.domain.events.insert(0, Event('TIL_{}'.format(til_index), [], [['not',['TIL_{}_triggered'.format(til_index)]],['>=', 'state.time', init_var[1]]], [['TIL_{}_triggered'.format(til_index)], init_var[2]], happening_type="timed_initial_event"))
                                til_index += 1
                                self.problem.init.remove(init_var)
                elif t == ':goal':
                    goals = []
                    self.split_predicates(group[0], goals, '', 'goals')
                    self.problem.goals = goals
                elif t == ':metric':
                    min_max_label = group.pop(0)
                    constants.METRIC_MINIMIZE = False if min_max_label == 'maximize' else True
                    self.problem.metric = group.pop(0)
                else: self.parse_problem_extended(t, group)
        else:
            raise Exception('File ' + problem_filename + ' does not match problem pattern')

    def parse_problem_extended(self, t, group):
        print(str(t) + ' is not recognized in problem')

    #-----------------------------------------------
    # Split predicates
    #-----------------------------------------------

    def split_predicates(self, group, preds, name, part):
        if not type(group) is list:
            raise Exception('Error with ' + name + part)
        if group == []:
            # takes care of empty preconditions
            return
        if group[0] == 'and':
            group.pop(0)
        else:
            group = [group]
        for predicate in group:
            if predicate[0] == 'not':
                if len(predicate) != 2:
                    raise Exception('Unexpected not in ' + name + part)
                preds.append(predicate)
            else:
                preds.append(predicate)

    # -----------------------------------------------
    # Split predicates of durative actions
    # -----------------------------------------------

    def split_durative_predicates(self, group, preds, name, part):
        if not type(group) is list:
            raise Exception('Error with ' + name + part)
        if group[0] == 'and':
            group.pop(0)
        else:
            group = [group]
        for predicate in group:
            relevant_preds = preds[1]
            if predicate[0] == 'at' and predicate[1] == 'start':
                relevant_preds = preds[0]
                predicate = predicate[2]
            elif predicate[0] == 'at' and predicate[1] == 'end':
                relevant_preds = preds[2]
                predicate = predicate[2]
            elif predicate[0] == 'over' and predicate[1] == 'all':
                relevant_preds = preds[1]
                predicate = predicate[2]
            elif predicate[0] == 'increase' or predicate[0] == 'decrease':
                relevant_preds = preds[1]
            else:
                raise Exception('malformed durative-action! no temporal annotation in happening \'{}\' for {}: {}'.format(name, part, predicate))
            if predicate[0] == 'not':
                if len(predicate) != 2:
                    raise Exception('Unexpected not in ' + name + part)
                relevant_preds.append(predicate)
            else:
                relevant_preds.append(predicate)

#-----------------------------------------------
# Main
#-----------------------------------------------
# if __name__ == '__main__':
#     domain = "C:\\Users\\Lior\\Desktop\\Nyx\\nyx-extension\\MA-PDDL\\examples\\Car_MAPDDL_Domain"
#     parser = MAPDDLParser(domain)
#     print('----------------------------')
#     print('Domain: ' + parser.domain.__repr__())
#     print('Actions: ')
#     for action in parser.domain.actions:
#         print(action)