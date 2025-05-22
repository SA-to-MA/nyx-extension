from VIS.SA_VIS.ActionsParser import ActionsParser
import pygame
from VIS.SA_VIS.SleepingBeautySimulator.SleepingBeauty import SleepingBeauty
from VIS.SA_VIS.SleepingBeautySimulator.SleepingBeautySimulator import SleepingBeautySimulator
from VIS.SA_VIS.SleepingBeautySimulator.SleepingBeautyWindow import SleepingBeautyWindow


class GenericSimulator:
    def __init__(self, domain_name, problem_file, solution_file):
        self.domain = domain_name
        self.problem_file = problem_file
        self.plan_file = solution_file

    def simulate(self):
        # create actions parser with problem and solution paths
        parser = ActionsParser(self.problem_file, self.plan_file)
        # get initial state and map it
        initial_state = parser.retrieve_initial_state()
        # initialize pygame window and create sleeping beauty window
        pygame.init()
        # Create the main Pygame window
        # Get the height of the screen
        screen_info = pygame.display.Info()
        screen_height = screen_info.current_h  # Current screen height
        # Set the window dimensions to the screen's height
        window_height = (3 / 4) * screen_height
        window_width = (5 / 4) * window_height
        screen = pygame.display.set_mode((window_width, window_height))
        # Load actions of solution from a file
        actions = parser.read_solution_from_file()
        if self.domain == "Sleeping Beauty":
            # set initial state of sleeping beauty problem
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
            # set name of window to sleeping beauty
            pygame.display.set_caption("Sleeping Beauty Simulator")
            # send screen to sleeping beauty window object
            window = SleepingBeautyWindow(screen, sleeping_beauty)
            # create sleeping beauty simulator
            simulator = SleepingBeautySimulator(sleeping_beauty, window, actions)
        else:
            return "Domain not supported"
        # run simulator
        simulator.run()
        # Quit Pygame
        pygame.quit()


# if __name__ == "__main__":
#     gs = GenericSimulator("Sleeping Beauty", r"C:\Users\Lior\Desktop\Nyx\nyx-extension\ex\sleeping_beauty\pb01.pddl", r"C:\Users\Lior\Desktop\Nyx\nyx-extension\ex\sleeping_beauty\plans\plan1_pb01.pddl")
#     gs.simulate()