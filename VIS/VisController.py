from pathlib import Path
from MA_PDDL.MAtoSA import MAtoSA, run_nyx
from VIS.MA_VIS.BlocksSimulator.BlocksInitParser import InitState
from VIS.MA_VIS.BlocksSimulator.BlocksWindow import Agent, main
from VIS.SA_VIS.SA_Simulator import GenericSimulator
import os
import shlex

class Parser:
    def __init__(self, _agents, _actions):
        # create list of Agents
        # actions = {'stack': [agent, block, block],'unstack':[...]}
        self.agents = {}
        self.actions = _actions
        for a in _agents:
            self.agents[a] = Agent(a, [])
        self.objects = {}

    def parse(self, _plan):
        with open(_plan, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line == '':
                    continue
                # Extract agent name and actions from the line
                self.parse_line(line)

    def parse_line(self, line):
        # Match the format: "<time>: <agent>&<action1>&<action2> <params> [<time_cost>]"
        parts = line.split()
        parts = parts[1:-1]
        actions = parts.pop(0).split('&')
        for act in actions:
            req_params = len(self.actions[act])
            params = []
            agent_name = ""
            for i in range(req_params):
                cur = parts.pop(0)
                if cur in self.agents:
                    agent_name = cur
                else:
                    params.append(cur)
            self.agents[agent_name].add_action((act, params))


def simulate_agents(parser):
    """Simulates the agents' actions step by step."""
    max_steps = max(len(agent.actions) for agent in parser.agents.values())

    for step in range(max_steps):
        print(f"Step {step + 1}:")
        for agent in parser.agents.values():
            action = agent.get_next_action()
            print(f"  {agent.name} -> {action}")

def ensure_directory_exists(directory):
    """Ensure the given directory exists."""
    os.makedirs(directory, exist_ok=True)
    return directory

def get_absolute_path(*path_parts):
    """Construct and return an absolute path from the given parts."""
    return str(Path(__file__).resolve().parent.parent.joinpath(*path_parts))

def process_blocks_domain(domain_path, problem_path, output_dir, parse, plan_file, flags):
    """Process the 'Blocks' domain by parsing and simulating it."""
    satoma = MAtoSA(domain_path, problem_path)
    new_domain = os.path.join(output_dir, "domain.pddl")
    new_problem = os.path.join(output_dir, "problem.pddl")
    satoma.generate(new_domain, new_problem)

    agents, blocks = satoma.agents["agent"], satoma.objects["block"]
    object_dict = InitState(new_problem, agents, blocks).parse_pddl_init()

    if parse:
        run_nyx(new_domain, new_problem, flags)

    parser = Parser(agents, {
        'no-op_agent': ['agent'],
        'stack': ['agent', 'block', 'block'],
        'unstack': ['agent', 'block', 'block'],
        'pick-up': ['agent', 'block'],
        'put-down': ['agent', 'block']
    })
    parser.parse(plan_file)
    main(parser.agents, object_dict)

def run(selected_domain, domain_path, problem_path, parse=False, plan_file="", flags=""):
    """Run the selected domain simulation."""
    # if no flags, set default flags
    if len(flags) == 0:
        flags = "-t:1 -pt"
    # if domain is MA, needs to convert to SA
    if selected_domain == "Blocks":
        # get output directory if runs with conversion to SA
        output_dir = ensure_directory_exists(get_absolute_path("MA_PDDL", "outputs"))
        # send to processing
        process_blocks_domain(domain_path, problem_path, output_dir, parse, plan_file, flags)
    elif selected_domain == "Other": # if other domain, it's not supported in visualization
        return "Not supported"
    else:
        if parse: # if no plan file, run and get plan
            plan_file = run_nyx(domain_path, problem_path, flags)
        # run domain problem and plan in simulator
        GenericSimulator(selected_domain, problem_path, plan_file).simulate()


# if __name__ == "__main__":
#     from InitParser import InitState
#     from BlocksWindow import Agent, main
#     domain = r"../MA_PDDL/examples/Blocks/domain-a2.pddl"
#     problem = r"../MA_PDDL/examples/Blocks/problem-a2.pddl"
#     plan_file = r'../MA_PDDL/outputs/plans/plan1_problem.pddl'
#     run(domain, problem, False, plan_file)