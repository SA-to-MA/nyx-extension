import re
import time
from pathlib import Path
import pygame
from MA_PDDL.MAtoSA import run_nyx
from VIS.InitParser import InitParser
from VIS.MA_VIS.BlocksSimulator.BlocksSimulation import BlocksSimulator
from VIS.MA_VIS.CarsSimulator.CarsSimulation import CarSimulator
from VIS.MA_VIS.MinecraftSimulator.MinecraftSimulation import MinecraftSimulator
from VIS.MA_VIS.SailingSimulator.SailingSimulator import SailingSimulator
import os
from VIS.SolutionParser import SolutionParser

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
        flags_path (str): The flags file path containing -t.
        default_t (float): Default value for time if -t is not found.

    Returns:
        float: Extracted time value.
    """
    flags = read_flags_file(flags_path)
    match = re.search(r"-t:(\d+(\.\d+)?)", flags)  # Match integers & floats
    if match:
        return float(match.group(1))  # Extract and return as float
    return default_t  # Return default if not found


def run(selected_domain, domain_path, problem_path, solve=False, plan_file="", flags_path="", exc="parallel"):
    """Run the selected domain simulation."""
    # if no flags, set default flags
    if len(flags_path) == 0:
        flags = "-t:1 -pt"
    else: # if flags file is valid, read flags
        flags = read_flags_file(flags_path)
    if solve: # if no plan file, run and get plan
        plan_file = run_nyx(domain_path, problem_path, flags)
    t_value = extract_t_value(flags_path)  # get t value from flags
    # parse init of problem
    init_parser = InitParser(problem_path)
    init_parser.parse_problem()
    # if sequential, take agents
    if exc == "sequential":
        init_parser.agents['agent'] = init_parser.objects.pop('agent')
    # parse solution
    sol_parser = SolutionParser(init_parser.agents, domain_path, plan_file)
    sol_parser.parse()
    main(selected_domain, init_parser.agents, init_parser.objects, init_parser.functions, init_parser.init_state, init_parser.goals, sol_parser.agents_actions, t_value)


def main(selected_domain, agents_by_type, objects_by_type, functions, init_state, goals, solution, t_value):
    """
    Initializes and runs the visualization and simulation for the given domain.

    Args:
        agents_by_type (dict): A dictionary of types of agents, and the agents' names. e.g. {'agent': ['a1']}
        objects_by_type (dict): A dictionary of types of objects, and the objects' names. e.g. {'block': ['a', 'c', 'b']}
        init_state (dict): A dictionary of agents/objects and their initial state. e.g. {'a1': {'handempty': True}, 'a2': {'handempty': True}, 'c': {'clear': True, 'on': 'b'}, 'a': {'clear': True, 'ontable': True}, 'b': {'ontable': True}}
        solution (dict): A dict containing agent names and their actions. e.g. { 'a1': [('pick-up', 'b'), (), ('stack', 'b', 'a')]}
        t_value(float): integer representing pace of simulation.
    """
    # Initialize Pygame
    pygame.init()
    info = pygame.display.Info()
    window_height = int((3 / 4) * info.current_h)
    window_width = int((5 / 4) * window_height)
    screen = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption(f"{selected_domain} Simulator")  # Dynamic title

    domain = selected_domain.lower()
    if domain == "blocks":
        simulator = BlocksSimulator(screen, agents_by_type, init_state, solution, t_value)
    elif domain == "car":
        simulator = CarSimulator(screen, init_state, solution, t_value)
    elif domain == "polycraft":
        simulator = MinecraftSimulator(screen, agents_by_type, functions, init_state, goals, solution, t_value)
    elif domain == "sailing":
        simulator = SailingSimulator(screen, agents_by_type, init_state, solution, t_value)
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
#     domain = r"../MA_PDDL/examples/Sailing/original_domain.pddl"
#     problem = r"../MA_PDDL/examples/Sailing/problem_2.pddl"
#     plan_file = r'../MA_PDDL/outputs/Sailing/plans/plan1_problem.pddl'
#     flags = r"../MA_PDDL/outputs/Sailing/config.txt"
#     run("Sailing", domain, problem, False, plan_file, flags)