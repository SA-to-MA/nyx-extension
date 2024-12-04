from Car import Car
from ActionsParser import ActionsParser
from CarSimulator import CarSimulator
from CarWindow import CarWindow
import pygame

# Set paths to the problem and solution files
problem = "C:\\Users\\Lior\\Desktop\\Nyx\\nyx-extension\\ex\\car\\pb02.pddl"
solution = "C:\\Users\\Lior\\Desktop\\Nyx\\nyx-extension\\ex\\car\\plans\\plan1_pb02.pddl"
parser = ActionsParser(problem, solution)

# Retrieve the initial state and map it to the Car class attributes
initial_state = parser.retrieve_initial_state()
mapped_initial_state = {
    "running": initial_state.get("running", True),
    "engine": initial_state.get("engineBlown", False),
    "trans": initial_state.get("transmission_fine", True),
    "d": initial_state.get("d", 0.0),
    "v": initial_state.get("v", 0.0),
    "a": initial_state.get("a", 0.0),
    "up": initial_state.get("up_limit", 1.0),
    "down": initial_state.get("down_limit", -1.0),
}

# Create an instance of the Car class
car = Car(**mapped_initial_state)

# Initialize Pygame and create the main window
pygame.init()
window_width = 1000
window_height = 800
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Car Simulator")

# Pass the Pygame window and Car object to the CarWindow
car_window = CarWindow(screen, car)

# Load actions of the solution from the file
actions = parser.read_solution_from_file()

# Create a CarSimulator instance
simulator = CarSimulator(car, car_window, actions)

# Run the simulation
simulator.run()

# Quit Pygame after the simulation ends
pygame.quit()
