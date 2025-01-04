import pygame
from VisController import Parser, Agent
import BlocksWindow
import time


class BlocksSimulator:
    def __init__(self, _agents, window):
        self.agents = _agents
        self.window = window

    def run(self):
        """
        Runs the simulation over a series of actions and checks events and processes at each time step,
        executing actions based on a dictionary of timestamp:[actions].
        """
        print("Starting the simulation...")
        self.window.draw()  # Draw initial state
        time.sleep(7)

        while self.agents:
            for agent in list(self.agents):  # Convert keys to a list to allow safe removal
                cur_action = agent.get_next_action()
                if cur_action == "Done":
                    self.agents.pop(agent)
                else:
                    self.execute_action(agent, cur_action)

            # Draw changes in the window
            self.window.draw()

            # Allow time to pass so changes are visible
            time.sleep(1)

        # Wait a few seconds before closing the simulation
        time.sleep(5)
        print("Simulation complete.")

    def execute_action(self, agent, action):
        """
        Executes a specific action on the agent.
        :param agent: The agent performing the action
        :param action: Action name as a string
        """
        agent.execute(action)

    def check_processes_and_events(self):
        """
        Placeholder for future processes and event handling.
        """
        pass


class BlockAgent(Agent):
    def __init__(self, _name, _actions):
        super().__init__(_name, _actions)

    def execute(self, action):
        if action == "no-op":
            self.stay()
        elif action == "pick-up":
            self.pick_up()
        elif action == "stack":
            self.stack()
        elif action == "unstack":
            self.unstack()
        elif action == "put-down":
            self.put_down()
        else:
            print(f"Unknown action: {action}")

    def stay(self):
        pass
    def pick_up(self):
        pass
    def stack(self):
        pass
    def unstack(self):
        pass
    def put_down(self):
        pass



if __name__ == '__main__':
    agents = ['a1', 'a2']
    actions = {
        'no-op_agent': ['agent'],
        'stack': ['agent', 'block', 'block'],
        'unstack': ['agent', 'block', 'block'],
        'pick-up': ['agent', 'block'],
        'put-down': ['agent', 'block'],
    }
    parser = Parser(agents, actions)
    parser.parse(r'../MA-PDDL/outputs/WithObjectsConversion/Blocks/plans/plan1_a2-problem.pddl')

    pygame.init()
    # Get the screen's height
    info = pygame.display.Info()
    window_height = int((3 / 4) * info.current_h)
    window_width = int((5 / 4) * window_height)
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Blocks Simulator")

    # Pass the Pygame window and agent objects to BlocksWindow
    blocks_window = BlocksWindow.BlocksWindow(screen, parser.agents)
    simulator = BlocksSimulator(parser.agents, blocks_window)

    # Run the simulation
    simulator.run()
