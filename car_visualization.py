import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the display with a wider window
width, height = 1400, 400  # Increased width to 1600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Simulation with Velocity Graph")

# Define constants for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Load car image and set size
car_image = pygame.image.load('ex/car/resources/i20_Modelpc.png')
car_image = pygame.transform.scale(car_image, (120, 50))
car_width, car_height = car_image.get_size()

# Car starting position and parameters
car_x = 50
car_y = height // 2 - car_height // 2
velocity = 0
acceleration = 0
distance = 0

# Time settings
clock = pygame.time.Clock()

# Read actions from file
def read_actions_from_file(file_path):
    '''
    :param file_path: path of file that stores the execution plan
    :return: list of tuples that contain actions to perform and their timestamp
    '''
    actions = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                parts = line.split(':')
                timestamp = float(parts[0].strip())
                action = parts[1].strip().split()[0]
                actions.append((timestamp, action))
    return actions

# Update car state based on action
def update_car_state(action):
    '''
    :param action: string which represents the action to be taken
    :return: boolean which represents goal has been reached. true means goal reached, while false means it hasn't reached its goal yet
    '''
    global velocity, acceleration
    if action == "accelerate":
        acceleration = 0.5  # lower acceleration for slower movement
    elif action == "decelerate":
        acceleration = -0.5  # lower deceleration
    elif action == "stop":
        velocity = 0
        acceleration = 0
        return True  # signal that the stop action has been reached, therefore car needs to be stopped
    return False

# Function to draw the velocity graph on the side of the Pygame window
# Function to draw the velocity graph with labels and ticks
def draw_velocity_graph(window, velocity_data):
    '''
    Draws a velocity graph on the side of the main Pygame window.
    :param window: The Pygame window to draw on
    :param velocity_data: List of velocity values over time
    '''
    graph_width = 300  # Graph dimensions
    graph_height = 300
    margin = 50
    max_velocity = max(max(velocity_data, default=0), 1)  # Avoid division by zero

    # Calculate position for the graph
    graph_x = width - graph_width - margin
    graph_y = margin

    # Draw graph background and borders
    pygame.draw.rect(window, WHITE, (graph_x, graph_y, graph_width, graph_height))
    pygame.draw.rect(window, BLACK, (graph_x, graph_y, graph_width, graph_height), 5)

    # Plot the velocity points
    for i in range(1, len(velocity_data)):
        x1 = graph_x + (i - 1) * (graph_width / len(velocity_data))
        y1 = graph_y + graph_height - (velocity_data[i - 1] / max_velocity) * (graph_height - 20)
        x2 = graph_x + i * (graph_width / len(velocity_data))
        y2 = graph_y + graph_height - (velocity_data[i] / max_velocity) * (graph_height - 20)
        pygame.draw.line(window, BLUE, (x1, y1), (x2, y2), 2)

    # Draw static axes
    pygame.draw.line(window, BLACK, (graph_x, graph_y + graph_height),
                     (graph_x + graph_width, graph_y + graph_height), 2)  # X-axis
    pygame.draw.line(window, BLACK, (graph_x, graph_y),
                     (graph_x, graph_y + graph_height), 2)  # Y-axis

    # Draw labels for axes
    font = pygame.font.Font(None, 20)
    velocity_label = font.render('Velocity', True, BLACK)
    window.blit(velocity_label, (graph_x + 5, graph_y + 5))
    time_label = font.render('Time', True, BLACK)
    window.blit(time_label, (graph_x + graph_width // 2 - time_label.get_width() // 2, graph_y + graph_height + 10))

    # Draw Y-axis ticks and labels for velocity
    tick_count = 5  # Number of tick marks
    for i in range(tick_count + 1):
        tick_value = max_velocity * i / tick_count
        y = graph_y + graph_height - (tick_value / max_velocity) * (graph_height - 20)
        pygame.draw.line(window, BLACK, (graph_x - 5, y), (graph_x + 5, y), 2)
        tick_label = font.render(f"{int(tick_value)}", True, BLACK)
        window.blit(tick_label, (graph_x - 30, y - tick_label.get_height() // 2))

    # Draw X-axis ticks and labels for time
    for i in range(0, len(velocity_data), max(1, len(velocity_data) // tick_count)):
        x = graph_x + i * (graph_width / len(velocity_data))
        pygame.draw.line(window, BLACK, (x, graph_y + graph_height - 5), (x, graph_y + graph_height + 5), 2)
        tick_label = font.render(f"{i}", True, BLACK)
        window.blit(tick_label, (x - tick_label.get_width() // 2, graph_y + graph_height + 15))

# Function to draw the road on which the car drives
def draw_road(window):
    '''
    :param window: window for the road to be drawn in
    :return: draws the road in the window
    '''
    # Draw road
    road_width = width - 400  # Leave space for the graph
    road_height = 100  # Adjusted height for the road
    road_y = height // 2 - road_height // 2  # Center the road vertically

    # Draw the road
    pygame.draw.rect(window, GRAY, (0, road_y, road_width, road_height))  # Road

    # Draw center line
    for i in range(0, road_width, 40):
        pygame.draw.line(window, YELLOW, (i, road_y + road_height // 2),
                         (i + 20, road_y + road_height // 2), 5)  # Dotted center line

# Function to display information
def display_information(window, car_x, velocity, start_time):
    '''
    :param window: PyGame window to draw in
    :param car_x: location of car on axis
    :param velocity: velocity of the car
    :param start_time: time pygame window started running
    :return:
    '''
    # Define fonts
    title_font = pygame.font.Font(None, 40)  # Font for title
    info_font = pygame.font.Font(None, 30)   # Font for distance, velocity, and time

    # Get window width for centering text
    window_width = window.get_width()

    # Title
    title_text = title_font.render('Car Information', True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(window_width // 2, 35))
    window.blit(title_text, title_rect.topleft)

    # Distance
    distance_text = info_font.render(f'Distance: {int(car_x)}', True, (0, 0, 0))
    distance_rect = distance_text.get_rect(center=(window_width // 2, 70))
    window.blit(distance_text, distance_rect.topleft)

    # Velocity
    velocity_text = info_font.render(f'Velocity: {round(velocity, 2)}', True, (0, 0, 0))
    velocity_rect = velocity_text.get_rect(center=(window_width // 2, 100))
    window.blit(velocity_text, velocity_rect.topleft)

    # Time
    current_time = time.time()  # Get the current time
    elapsed_time = current_time - start_time  # Calculate elapsed time in seconds
    time_text = info_font.render(f'Time: {round(elapsed_time, 2)}s', True, (0, 0, 0))
    time_rect = time_text.get_rect(center=(window_width // 2, 130))
    window.blit(time_text, time_rect.topleft)

# Main function for visualization
def run_simulation(actions):
    '''
    :param actions: list of tuples containing actions and timestamp
    :return: runs the simulation and draws all in window of pygame
    '''
    global velocity, car_x, acceleration
    current_action_index = 0
    start_time = time.time()

    # For storing velocity over time
    velocity_data = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background
        window.fill(WHITE)

        # Draw the road
        draw_road(window)

        # Update time and get next action if due
        current_time = time.time() - start_time
        velocity_data.append(velocity)  # Capture current velocity

        if current_action_index < len(actions):
            action_time, action = actions[current_action_index]
            if current_time >= action_time:
                # If the stop action is encountered, end the simulation
                if update_car_state(action):
                    running = False
                current_action_index += 1

        # Update velocity and position only if running
        velocity += acceleration
        if velocity < 0:
            velocity = 0

        # Scale the car's position update to slow down movement
        car_x += velocity * 0.01  # Adjust this scaling factor to control speed

        # Draw car
        window.blit(car_image, (car_x, car_y))

        # Display car information
        display_information(window, car_x, velocity, start_time)

        # Draw the velocity graph
        draw_velocity_graph(window, velocity_data)

        # Update display
        pygame.display.update()
        clock.tick(60)

    time.sleep(10)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    ### TO BE CHANGED: needs to write code that will able performing simulation on given problem using command line
    actions_file = 'ex/car/plans/plan1_pb02.pddl'
    actions = read_actions_from_file(actions_file)
    run_simulation(actions)
