import random

import pygame
import time

class Agent:
    def __init__(self, _name, _actions):
        self.actions = _actions
        self.name = _name

    def add_action(self, _action):
        self.actions.append(_action)

    def get_next_action(self):
        if self.actions:
            return self.actions.pop(0)
        return "Done"

    def execute(self, _action, blocks, screen):
        pass

class BlocksWindow:
    def __init__(self, screen, agents, blocks):
        self.screen = screen
        # initialize empty dictionaries
        self.agents = {}
        self.blocks = {}
        # initialize blocks and agents
        self.initializeVisObjects(agents, blocks)
        # set blocks size
        self.block_size = 50
        self.agent_size = 40
        self.margin = 10
        # Load the table background image
        self.background_image = pygame.image.load('../MA_VIS/images/table.png')  # Replace with your image file
        self.background_image = pygame.transform.scale(self.background_image, screen.get_size())  # Scale to screen size

        # Load the hand image for agents
        self.hand_image = pygame.image.load('../MA_VIS/images/hand.png')  # Load the hand image
        self.hand_image = pygame.transform.scale(self.hand_image,(150, 110))

    def initializeVisObjects(self, agents, init_obj, dis=150):
        screen_width, screen_height = self.screen.get_size()
        # Define base positions relative to screen size
        block_x = int(screen_width * 0.3)
        block_y = int(screen_height * 0.7)
        positions = {}
        # calculate positions of objects recursively
        def calculateBlockPosition(obj):
            properties = init_obj[obj]
            if properties.get('on_table', False):
                # Object is on the table
                positions[obj] = {'x': block_x, 'y': block_y}
                return positions[obj]
            elif 'on' in properties and properties['on']:
                # Object is on another object
                parent_obj = properties['on']
                parent_position = calculateBlockPosition(parent_obj)  # Recursively get parent's position
                positions[obj] = {'x': parent_position['x'], 'y': parent_position['y'] - 50}
                return positions[obj]
        for obj in init_obj.keys():
            if obj not in agents:
                if init_obj[obj].get('on_table', False):
                    block_x += 50  # Increment base_x for each new table object
                calculateBlockPosition(obj)
        # set blocks properties in blocks dictionary
        for block, pos in positions.items():
            self.blocks[block] = Block(block, pos['x'], pos['y'], init_obj[block]['clear'], init_obj[block]['on_table'], init_obj[block]['in_hand'])
        agent_x = int(screen_width * 0.05)
        agent_y = int(screen_height * 0.1)
        for agent_name, agent_obj in agents.items():
            # check if agent holding object, if so - put it
            if init_obj[agent_name]['is_empty'] == True:
                holding = None
            else:
                block_name = init_obj[agent_name]['holding']
                holding = self.blocks[block_name]
            # create vis agent
            new_agent = BlockAgent(agent_name, agent_obj.actions, agent_x, agent_y, holding)
            self.agents[agent_name] = new_agent
            # increase x index by dis
            agent_x+=dis

    def draw(self):
        # Clear the screen
        self.screen.blit(self.background_image, (0, 0))

        # Draw agents as hands
        for agent in self.agents.values():
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

### VISUALIZATION OBJECTS AND AGENTS ###
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
    def __init__(self, _name, _actions, x, y, holding):
        super().__init__(_name, _actions)
        self.x = x
        self.y = y
        self.holding = holding

    def execute(self, action, blocks, screen):
        # Get screen dimensions
        screen_width, screen_height = screen.get_size()

        # Define relative heights and offsets
        agent_offset_y = int(screen_height * 0.1)  # Height above agent when holding
        table_y = int(screen_height * 0.7)  # Baseline for placing blocks on table
        stack_offset_y = int(screen_height * 0.06)  # Height difference when stacking

        if action[0] == "pick-up":
            block_name = action[1][0]  # Extract the first element from the list
            block = blocks[block_name]
            if block.clear and block.on_table:
                self.holding = block
                block.in_hand = True
                block.on_table = False
                block.x = self.x  # Align with agent
                block.y = self.y + agent_offset_y  # Hold above agent

        elif action[0] == "put-down":
            if self.holding:
                block = self.holding
                block.in_hand = False
                block.on_table = True
                block.clear = True
                block.x = self.x  # Place at agent's position
                block.y = table_y  # Drop to table level
                self.holding = None

        elif action[0] == "stack":
            block_name = action[1][0]  # Block to stack
            target_block_name = action[1][1]  # Block on which to stack
            block = blocks[block_name]
            target_block = blocks[target_block_name]
            if target_block.clear:
                target_block.clear = False
                block.in_hand = False
                block.on_table = False
                block.clear = True
                block.x = target_block.x  # Align x with target
                block.y = target_block.y - stack_offset_y  # Stack relative to target
                self.holding = None

        elif action[0] == "unstack":
            block_name = action[1][0]  # Block being picked up
            under_block_name = action[1][1]  # Block below
            block = blocks[block_name]
            under_block = blocks[under_block_name]
            if block.clear and not block.in_hand:
                self.holding = block
                block.in_hand = True
                block.on_table = False
                block.clear = False
                block.x = self.x  # Align with agent
                block.y = self.y + agent_offset_y  # Lift above agent
                under_block.clear = True


class BlocksSimulator:
    def __init__(self, window):
        self.window = window

    def run(self):
        print("Starting simulation...")
        self.window.draw()  # Initial state
        running = True
        time.sleep(1)
        while running:
            running = False  # Assume no actions are left
            for agent_name, agent in self.window.agents.items():
                if agent.actions:  # Check if the agent still has actions
                    running = True
                    action = agent.actions.pop(0)  # Get the next action
                    agent.execute(action, self.window.blocks, self.window.screen)  # Execute the action
                    self.window.draw()  # Update visualization
            time.sleep(1)  # Pause for visualization
        print("Simulation complete.")

def main(agents, init_obj):
    # Initialize Pygame
    pygame.init()
    info = pygame.display.Info()
    window_height = int((3 / 4) * info.current_h)
    window_width = int((5 / 4) * window_height)
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Blocks Simulator")
    # Create visualization window
    blocks_window = BlocksWindow(screen, agents, init_obj)
    # Create simulator
    simulator = BlocksSimulator(blocks_window)
    # Run simulation
    simulator.run()
    # Wait before closing
    time.sleep(5)
    pygame.quit()

