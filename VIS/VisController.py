from MA_PDDL import MAtoSA
import subprocess
from VIS.InitParser import InitState
from VIS.MA_VIS.BlocksSimulator.BlocksWindow import Agent, main
from VIS.SA_VIS import SA_Simulator
import os

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

def run(selected_domain, domain_path, problem_path, parse=False, plan_file=""):
    # Construct absolute path to the outputs directory
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "MA_PDDL", "outputs"))
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

    if selected_domain == "Blocks":
        # parse domain and problem, and create multiagent files
        satoma = MAtoSA.MAtoSA(domain_path, problem_path)

        # Define new domain and problem output paths
        new_domain = os.path.join(output_dir, "domain-a1.pddl")
        new_problem = os.path.join(output_dir, "problem-a1.pddl")

        satoma.generate(new_domain, new_problem)
        # get all agents and blocks
        agents = satoma.agents['agent']
        blocks = satoma.objects['block']
        # parse init state
        parser = InitState(new_problem, agents, blocks)
        object_dict = parser.parse_pddl_init()
        # create parser for plan
        actions = {'no-op_agent': ['agent'], 'stack': ['agent','block', 'block'], 'unstack': ['agent','block', 'block'], 'pick-up': ['agent','block'], 'put-down': ['agent','block']}
        parser = Parser(agents, actions)

        # Construct plan file path
        plan_output_dir = os.path.join(output_dir, "plans")
        os.makedirs(plan_output_dir, exist_ok=True)  # Ensure the plans directory exists
        plan_file = os.path.join(plan_output_dir, "plan1_problem.pddl")

        # Get plan from Nyx
        if parse:
            command = [
                'python',
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "nyx.py")),
                new_domain,
                new_problem,
                '-t:1'
            ]
            print(f"Executing command: {' '.join(command)}")  # Debugging print
            subprocess.run(command, text=True, capture_output=True)

        parser.parse(plan_file)
        main(parser.agents, object_dict)
    elif selected_domain == "Other":
        return
    else:
        # Construct plan file path
        plan_output_dir = os.path.join(output_dir, "plans")
        os.makedirs(plan_output_dir, exist_ok=True)

        plan_file = os.path.join(plan_output_dir, "plan1_problem.pddl")

        # Get plan from Nyx if needed
        if parse:
            command = [
                'python',
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "nyx.py")),
                domain_path,
                problem_path,
                '-t:1'
            ]
            subprocess.run(command, text=True, capture_output=True)

        sa_sim = SA_Simulator.GenericSimulator(selected_domain, problem_path, plan_file)
        sa_sim.simulate()


# if __name__ == "__main__":
#     from InitParser import InitState
#     from BlocksWindow import Agent, main
#     domain = r"../MA_PDDL/examples/Blocks/domain-a2.pddl"
#     problem = r"../MA_PDDL/examples/Blocks/problem-a2.pddl"
#     plan_file = r'../MA_PDDL/outputs/plans/plan1_problem.pddl'
#     run(domain, problem, False, plan_file)