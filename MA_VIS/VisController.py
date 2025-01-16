from MA_PDDL import MAtoSA
import InitParser
import subprocess
import BlocksWindow

class Parser:
    def __init__(self, _agents, _actions):
        # create list of Agents
        # actions = {'stack': [agent, block, block],'unstack':[...]}
        self.agents = {}
        self.actions = _actions
        for a in _agents:
            self.agents[a] = BlocksWindow.Agent(a, [])
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

def run(domain_path, problem_path, parse=False, plan_file=""):
    # parse domain and problem, and create multiagent files
    satoma = MAtoSA.MAtoSA(domain_path, problem_path)
    new_domain = "../MA_PDDL/outputs_old/Blocks/domain.pddl"
    new_problem = "../MA_PDDL/outputs_old/Blocks/problem.pddl"
    satoma.generate(new_domain, new_problem)
    # get all agents and blocks
    agents = satoma.agents['agent']
    blocks = satoma.objects['block']
    # parse init state
    parser = InitParser.InitState(new_problem, agents, blocks)
    object_dict = parser.parse_pddl_init()
    # create parser for plan
    actions = {'no-op_agent': ['agent'], 'stack': ['agent','block', 'block'], 'unstack': ['agent','block', 'block'], 'pick-up': ['agent','block'], 'put-down': ['agent','block']}
    parser = Parser(agents, actions)
    # get plan from nyx
    if parse:
        command = [
            'python',
            '../nyx.py',
            new_domain,
            new_problem,
            '-t:1'
        ]
        command = " ".join(command)
        subprocess.run(command, text=True, capture_output=True)
        plan_file = r'../MA_PDDL/outputs_old/Blocks/plans/plan1_problem.pddl'
    parser.parse(plan_file)
    BlocksWindow.main(parser.agents, object_dict)


# if __name__ == "__main__":
#     domain = r"../MA_PDDL/examples/Blocks/domain-a3.pddl"
#     problem = r"../MA_PDDL/examples/Blocks/problem-a3.pddl"
#     plan_file = r'../MA_PDDL/outputs_old/Blocks/plans/plan1_problem.pddl'
#     run(domain, problem, False, plan_file)