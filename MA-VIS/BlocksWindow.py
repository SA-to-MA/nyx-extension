import random
import pygame
import time
from VisController import Agent

class BlocksWindow:
    def __init__(self, screen, agents, blocks):
        self.screen = screen
        self.agents = agents
        self.blocks = blocks
        self.block_size = 50
        self.agent_size = 40
        self.margin = 10

        # Load the table background image
        self.background_image = pygame.image.load('images/table.png')  # Replace with your image file
        self.background_image = pygame.transform.scale(self.background_image, screen.get_size())  # Scale to screen size

        # Load the hand image for agents
        self.hand_image = pygame.image.load('images/hand.png')  # Load the hand image
        self.hand_image = pygame.transform.scale(self.hand_image,(150, 110))

    def draw(self):
        # Clear the screen
        self.screen.blit(self.background_image, (0, 0))

        # Draw agents as hands
        for agent in self.agents:
            # Render the hand image for each agent
            self.screen.blit(self.hand_image, (agent.x, agent.y))

            # Display the agent name above the hand
            font = pygame.font.SysFont(None, 20)
            label = font.render(agent.name, True, (255, 255, 255))
            self.screen.blit(label, (agent.x + 10, agent.y - 20))  # Name above the hand

        # Draw blocks
        for block in self.blocks.values():
            pygame.draw.rect(
                self.screen,
                block.color,  # Blue color for blocks
                (block.x, block.y, self.block_size, self.block_size),
            )
            font = pygame.font.SysFont(None, 24)
            label = font.render(block.name, True, (255, 255, 255))
            self.screen.blit(label, (block.x + 10, block.y + 10))


        # Update display
        pygame.display.flip()


class Block:
    def __init__(self, name, x, y, clear, on_table, in_hand=False):
        self.name = name
        self.x = x
        self.y = y
        self.clear = clear
        self.on_table = on_table
        self.in_hand = in_hand
        self.color = self.random_color()
    def random_color(self):
        """Generate a random RGB color."""
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class BlockAgent(Agent):
    def __init__(self, _name, _actions, x, y):
        super().__init__(_name, _actions)
        self.x = x
        self.y = y
        self.holding = None

    def execute(self, action, blocks):
        if action[0] == "pick-up":
            block_name = action[1][0]  # Extract the first element from the list
            block = blocks[block_name]
            if block.clear and block.on_table:
                self.holding = block
                block.in_hand = True
                block.on_table = False
                #block.clear = False
                block.x = self.x
                block.y = self.y + 70 # Hold above the agent
        elif action[0] == "put-down":
            if self.holding:
                block = self.holding
                block.in_hand = False
                block.on_table = True
                block.clear = True
                block.x = self.x
                block.y = 400  # Drop on table baseline
                self.holding = None
        elif action[0] == "stack":
            block_name = action[1][0]  # Extract the first element from the list
            target_block_name = action[1][1]
            block = blocks[block_name]
            target_block = blocks[target_block_name]
            if target_block.clear:
                target_block.clear = False
                block.in_hand = False
                block.on_table = False
                block.clear = True
                block.x = target_block.x
                block.y = target_block.y - 50  # Stack above target block
                self.holding = None
        elif action[0] == "unstack":
            block_name = action[1][0] # a
            under_block_name = action[1][1] # b
            block = blocks[block_name]
            under_block = blocks[under_block_name]
            if block.clear and not block.in_hand:
                self.holding = block
                block.in_hand = True
                block.on_table = False
                block.clear = False
                block.x = self.x
                block.y = self.y + 70 # Unstack to agent's position
                under_block.clear = True

class BlocksSimulator:
    def __init__(self, agents, blocks, window):
        self.agents = agents
        self.blocks = blocks
        self.window = window

    def run(self):
        print("Starting simulation...")
        self.window.draw()  # Initial state
        running = True
        time.sleep(1)
        while running:
            running = False  # Assume no actions are left
            for agent_name, agent in self.agents.items():
                if agent.actions:  # Check if the agent still has actions
                    running = True
                    action = agent.actions.pop(0)  # Get the next action
                    agent.execute(action, blocks)  # Execute the action
                    self.window.draw()  # Update visualization
            time.sleep(1)  # Pause for visualization

        print("Simulation complete.")


# Initialize Pygame
pygame.init()
info = pygame.display.Info()
window_height = int((3 / 4) * info.current_h)
window_width = int((5 / 4) * window_height)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Blocks Simulator")

# Initialize agents and blocks
agents = {
    "a1": BlockAgent("A1", [('no-op_agent', []), ('pick-up', ['c']), ('no-op_agent', []), ('stack', ['c', 'b']), ('no-op_agent', [])], 100, 100),
    "a2": BlockAgent("A2", [('no-op_agent', []), ('pick-up', ['b']), ('stack', ['b', 'a']), ('no-op_agent', []), ('no-op_agent', [])],  250, 100),
    "a3": BlockAgent("A3", [('unstack', ['a', 'b']), ('put-down', ['a']), ('pick-up', ['d']), ('no-op_agent', []), ('stack', ['d', 'c'])], 400, 100)
}
blocks = {
    'a': Block('a', x=300, y=350, clear=True, on_table=False),  # Block a is on Block b
    'b': Block('b', x=300, y=400, clear=False, on_table=True),  # Block b is on the table
    'c': Block('c', x=400, y=400, clear=True, on_table=True),  # Block c is on the table
    'd': Block('d', x=500, y=400, clear=True, on_table=True),  # Block d is on the table
}




# Create visualization window
blocks_window = BlocksWindow(screen, agents.values(), blocks)

# Create simulator
simulator = BlocksSimulator(agents, blocks, blocks_window)

# Run simulation
simulator.run()

# Wait before closing
time.sleep(5)
pygame.quit()