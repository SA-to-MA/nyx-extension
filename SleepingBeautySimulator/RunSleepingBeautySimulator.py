from SleepingBeauty import SleepingBeauty
from ActionsParser import ActionsParser
from SleepingBeautySimulator import SleepingBeautySimulator
from SleepingBeautyWindow import SleepingBeautyWindow
import pygame

# set all predicates
all_predicates = [
    "windowclosed", "windowopen", "magnetoperational", "freshair",
    "circuit", "alarmdisabled", "alarmenabled", "voltage",
    "ringing", "almostawake", "deeplyasleep", "awake"
]
# create actions parser with problem and solution paths
problem = "C:\\Users\\\Lior\\Desktop\\Nyx\\nyx-extension\\ex\\sleeping_beauty\\pb01.pddl"
sol = "C:\\Users\\\Lior\\Desktop\\Nyx\\nyx-extension\\ex\\sleeping_beauty\\plans\\plan1_pb01.pddl"
parser = ActionsParser(problem, sol)
# get initial state and map it
initial_state = parser.retrieve_initial_state(all_predicates)
# This mapping will depend on your naming convention.
mapped_initial_state = {
    "window_closed": initial_state.get("windowclosed", True),
    "magnet_operational": initial_state.get("magnetoperational", True),
    "circuit": initial_state.get("circuit", False),
    "alarm_enabled": initial_state.get("alarmenabled", False),
    "alarm_disabled": initial_state.get("alarmdisabled", True),
    "ringing": initial_state.get("ringing", False),
    "deeply_asleep": initial_state.get("deeplyasleep", True),
    "almost_awake": initial_state.get("almostawake", False),
    "awake": initial_state.get("awake", False),
    "charge": initial_state.get("charge", 0.0),
    "resistance": initial_state.get("resistance", 1.0),
    "ring_time": initial_state.get("ringtime", 0.0),
    "voltage": initial_state.get("voltage", False)
}
# Create an instance of SleepingBeauty with the initial state
sleeping_beauty = SleepingBeauty(**mapped_initial_state)
# initialize pygame window and create sleeping beauty window
pygame.init()
# Create the main Pygame window
window_width = 1000
window_height = 1000
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Sleeping Beauty Simulator")
# load images and store them in a dictionary
images = {
    "window_closed": pygame.image.load("resources/window-closed.png"),
    "window_open": pygame.image.load("resources/window-open.png"),
    "asleep": pygame.image.load("resources/asleep.png"),
    "awake": pygame.image.load("resources/awake.png"),
    "almost_awake": pygame.image.load("resources/almost-awake.png"),
    "alarm_enabled": pygame.image.load("resources/alarm-enabled.png"),
    "alarm_disabled": pygame.image.load("resources/alarm-disabled.png"),
    "alarm_ringing": pygame.image.load("resources/alarm-ringing.png"),
}
positions = {
    "window": (300, 100),         # Position for the window
    "alarm": (750, 550),          # Position for the alarm clock
    "figure": (200, 400),         # Position for the main figure (Sleeping Beauty)
}
# send screen to sleeping beauty window object
window = SleepingBeautyWindow(screen, sleeping_beauty, images, positions)
# Load actions of solution from a file
actions = parser.read_solution_from_file()
# create simulator object
simulator = SleepingBeautySimulator(sleeping_beauty, window, actions)
simulator.run()
# Quit Pygame
pygame.quit()