import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the display with a wider window
width, height = 1600, 600  # Increased width to 1600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Simulation with Velocity Graph")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Load car image
car_image = pygame.image.load('ex/car/resources/i20_Modelpc.png')
car_image = pygame.transform.scale(car_image, (120, 50))
car_width, car_height = car_image.get_size()

# Car starting position
car_x = 50
car_y = height // 2 - car_height // 2  # Center the car vertically

velocity = 0
acceleration = 0
distance = 0

# Time settings
clock = pygame.time.Clock()

# Read actions from file
def read_actions_from_file(file_path):
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
    global velocity, acceleration
    if action == "accelerate":
        acceleration = 0.5  # Lower acceleration for slower movement
    elif action == "decelerate":
        acceleration = -0.5  # Lower deceleration
    elif action == "stop":
        velocity = 0
        acceleration = 0
        return True  # Signal that the stop action has been reached
    return False

# Function to draw the velocity graph on the side of the Pygame window
def draw_velocity_graph(window, time_data, velocity_data):
    graph_width = 300  # Increased graph width to better fit the wider window
    graph_height = 300
    margin = 50
    max_velocity = max(max(velocity_data, default=0), 1)  # Avoid division by zero

    # Calculate position for the graph
    graph_x = width - graph_width - margin
    graph_y = margin

    # Draw graph background
    pygame.draw.rect(window, WHITE, (graph_x, graph_y, graph_width, graph_height))
    pygame.draw.rect(window, BLACK, (graph_x, graph_y, graph_width, graph_height), 4)

    # Plot the velocity points
    for i in range(1, len(velocity_data)):
        x1 = graph_x + (i - 1) * (graph_width / len(velocity_data))
        y1 = graph_y + graph_height - (velocity_data[i - 1] / max_velocity) * (graph_height - 20)
        x2 = graph_x + i * (graph_width / len(velocity_data))
        y2 = graph_y + graph_height - (velocity_data[i] / max_velocity) * (graph_height - 20)
        pygame.draw.line(window, BLUE, (x1, y1), (x2, y2), 2)

    # Draw axes
    pygame.draw.line(window, BLACK, (graph_x, graph_y + graph_height),
                     (graph_x + graph_width, graph_y + graph_height), 2)  # X-axis
    pygame.draw.line(window, BLACK, (graph_x, graph_y),
                     (graph_x, graph_y + graph_height), 2)  # Y-axis

    # Draw labels
    font = pygame.font.Font(None, 24)
    velocity_label = font.render('Velocity', True, BLACK)
    window.blit(velocity_label, (graph_x + 5, graph_y + graph_height - 30))

# Function to draw the road
def draw_road(window):
    # Draw road
    road_width = width - 400  # Leave space for the graph
    road_height = 150  # Adjusted height for the road
    road_y = height // 2 - road_height // 2  # Center the road vertically

    # Draw the road
    pygame.draw.rect(window, GRAY, (0, road_y, road_width, road_height))  # Road

    # Draw center line
    for i in range(0, road_width, 40):
        pygame.draw.line(window, YELLOW, (i, road_y + road_height // 2),
                         (i + 20, road_y + road_height // 2), 5)  # Dotted center line

# Main function for visualization
def run_simulation(actions):
    global velocity, car_x, acceleration
    current_action_index = 0
    start_time = time.time()

    # For storing velocity over time
    time_data = []
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
        time_data.append(current_time)  # Capture current time
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

        # Display information
        font = pygame.font.Font(None, 36)
        distance_text = font.render(f'Distance: {int(car_x)}', True, (0, 0, 0))
        velocity_text = font.render(f'Velocity: {round(velocity, 2)}', True, (0, 0, 0))
        window.blit(distance_text, (20, 20))
        window.blit(velocity_text, (20, 60))

        # Draw the velocity graph
        draw_velocity_graph(window, time_data, velocity_data)

        # Update display
        pygame.display.update()
        clock.tick(60)

    time.sleep(10)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    actions_file = 'ex/car/plans/plan1_pb02.pddl'
    actions = read_actions_from_file(actions_file)
    run_simulation(actions)
