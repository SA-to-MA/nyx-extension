import re
import time
from pathlib import Path
import pygame
from MA_PDDL.MAtoSA import MAtoSA, run_nyx
from VIS.MA_VIS.Agent import Agent
from VIS.MA_VIS.BlocksSimulator.BlocksInitParser import InitState
from VIS.MA_VIS.BlocksSimulator.BlocksSimulation import BlocksWindow, BlocksSimulator
from VIS.MA_VIS.CarsSimulator.CarsSimulation import CarWindow, CarSimulator
from VIS.MA_VIS.MinecraftSimulator.MinecraftSimulation import MinecraftWindow, MinecraftSimulator
from VIS.MA_VIS.MinecraftSimulator.MinecraftInitParser import MinecraftInitState
from VIS.SA_VIS.SA_Simulator import GenericSimulator
import os
from VIS.MA_VIS.CarsSimulator.CarsInitParser import InitStateCar

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

def process_blocks_domain(domain_path, problem_path, output_dir, parse, plan_file, flags, t_value):
    """Process the 'Blocks' domain by parsing and simulating it."""
    satoma = MAtoSA(domain_path, problem_path)
    new_domain = os.path.join(output_dir, "domain.pddl")
    new_problem = os.path.join(output_dir, "problem.pddl")
    satoma.generate(new_domain, new_problem)

    agents, blocks = satoma.agents["agent"], satoma.objects["block"]
    object_dict = InitState(new_problem, agents, blocks).parse_pddl_init()

    if parse:
        plan_file = run_nyx(new_domain, new_problem, flags)

    parser = Parser(agents, {
        'no-op_agent': ['agent'],
        'stack': ['agent', 'block', 'block'],
        'unstack': ['agent', 'block', 'block'],
        'pick-up': ['agent', 'block'],
        'put-down': ['agent', 'block']
    })
    parser.parse(plan_file)
    main(parser.agents, object_dict, "Blocks", t_value)

def process_car_domain(domain_path, problem_path, output_dir, parse, plan_file, flags, t_value):
    """Process the 'Car' domain by parsing and simulating it."""
    satoma = MAtoSA(domain_path, problem_path)
    new_domain = os.path.join(output_dir, "domain.pddl")
    new_problem = os.path.join(output_dir, "problem.pddl")
    satoma.generate(new_domain, new_problem)

    agents = satoma.agents["agent"]  # Get cars (agents)
    object_dict = InitStateCar(new_problem, agents).parse_pddl_init()  # Use InitStateCar

    if parse:
        plan_file = run_nyx(new_domain, new_problem, flags)  # Run Nyx planner

    parser = Parser(agents, {
        'no-op_agent': ['agent'],
        'accelerate': ['agent'],
        'decelerate': ['agent'],
        'stop': ['agent'],
    })
    parser.parse(plan_file)

    # Pass agents (cars) and their parsed state to the simulator
    main(parser.agents, object_dict, "Car", t_value)

def process_minecraft_domain(domain_path, problem_path, output_dir, parse, plan_file, flags, t_value):
    # 1. Generate single-agent domain/problem
    satoma = MAtoSA(domain_path, problem_path)
    new_domain = os.path.join(output_dir, "domain.pddl")
    new_problem = os.path.join(output_dir, "problem.pddl")
    satoma.generate(new_domain, new_problem)

    # 2. Get agents from original domain
    agents = satoma.agents["agent"]

    # 3. Parse initial state
    inventory_dict = MinecraftInitState(new_problem, agents).parse_pddl_init()

    # 4. Run planner if needed
    if parse:
        plan_file = run_nyx(new_domain, new_problem, flags)

    # 5. Parse plan into per-agent action lists
    parser = Parser(agents, {
        'get_log': ['agent'],
        'craft_plank': ['agent'],
        'craft_stick': ['agent'],
        'get_sack': ['agent'],
        'place_tree_tap': ['agent'],
        'craft_pogo_stick': ['agent']
    })
    parser.parse(plan_file)

    # 6. Run main visual simulation
    main(parser.agents, inventory_dict, "Minecraft", t_value)

def read_flags_file(flags_path):
    """
    Reads the contents of a flags file.

    Args:
        flags_path (str): Path to the file containing flags.

    Returns:
        str: The content of the file as a single string.
    """
    try:
        with open(flags_path, "r") as file:
            return file.read().strip()  # Read and strip any leading/trailing spaces
    except FileNotFoundError:
        print(f"Error: Flags file '{flags_path}' not found.")
        return ""  # Return empty string if file doesn't exist

def extract_t_value(flags_path, default_t=1.0):
    """
    Extracts the -t flag value from the flags string.

    Args:
        flags (str): The flags string containing -t.
        default_t (float): Default value for time if -t is not found.

    Returns:
        float: Extracted time value.
    """
    flags = read_flags_file(flags_path)
    match = re.search(r"-t:(\d+(\.\d+)?)", flags)  # Match integers & floats
    if match:
        return float(match.group(1))  # Extract and return as float
    return default_t  # Return default if not found

def run(selected_domain, domain_path, problem_path, parse=False, plan_file="", flags_path=""):
    """Run the selected domain simulation."""
    # if no flags, set default flags
    if len(flags_path) == 0:
        flags = "-t:1 -pt"
    else: # if flags file is valid, read flags
        flags = read_flags_file(flags_path)
    t_value = extract_t_value(flags_path) # get t value from flags
    # if sa domain of sleeping beauty, run it
    if selected_domain == "Sleeping Beauty":
        if parse: # if no plan file, run and get plan
            plan_file = run_nyx(domain_path, problem_path, flags)
        # run domain problem and plan in simulator
        GenericSimulator(selected_domain, problem_path, plan_file).simulate()
    elif selected_domain == "Other": # if other domain, it's not supported in visualization
        return "Not supported"
    else:
        # if domain is MA, needs to convert to SA
        # get output directory if runs with conversion to SA
        output_dir = ensure_directory_exists(get_absolute_path("MA_PDDL", f"outputs/{selected_domain}"))
        if selected_domain == "Blocks":
            # if blocks, send to processing
            process_blocks_domain(domain_path, problem_path, output_dir, parse, plan_file, flags, t_value)
        elif selected_domain == "Car":
            process_car_domain(domain_path, problem_path, output_dir, parse, plan_file, flags, t_value)
        elif selected_domain == "PolyCraft":
            process_minecraft_domain(domain_path, problem_path, output_dir, parse, plan_file, flags, t_value)
        else:
            return "Not supported"


def main(agents, init_obj, domain, t_value):
    """
    Initializes and runs the visualization and simulation for the given domain.

    Args:
        agents (dict): A dictionary of agents (blocks or cars).
        init_obj (dict): The parsed initial state of objects.
        domain (str): The domain type ("Blocks" or "Car").
        t_value (int): the interval for simulation
    """
    # Initialize Pygame
    pygame.init()
    info = pygame.display.Info()
    window_height = int((3 / 4) * info.current_h)
    window_width = int((5 / 4) * window_height)
    screen = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption(f"{domain} Simulator")  # Dynamic title

    if domain == "Blocks":
        # Create Blocks visualization and simulator
        sim_window = BlocksWindow(screen, agents, init_obj)
        simulator = BlocksSimulator(sim_window, t_value)

    elif domain == "Car":
        # Create Car visualization and simulator
        sim_window = CarWindow(screen, agents, init_obj)  # CarWindow doesn't need init_obj
        simulator = CarSimulator(sim_window, t_value)

    elif domain == "PolyCraft":
        # Create Car visualization and simulator
        sim_window = MinecraftWindow(screen, agents)
        simulator = MinecraftSimulator(sim_window, t_value)

    else:
        print("Unsupported domain. Exiting...")
        pygame.quit()
        return

    # Run simulation
    simulator.run()

    # Wait before closing
    time.sleep(5)
    pygame.quit()

# if __name__ == "__main__":
#     from InitParser import InitState
#     from BlocksWindow import Agent, main
#     domain = r"../MA_PDDL/examples/Blocks/domain-a2.pddl"
#     problem = r"../MA_PDDL/examples/Blocks/problem-a2.pddl"
#     plan_file = r'../MA_PDDL/outputs/plans/plan1_problem.pddl'
#     run(domain, problem, False, plan_file)