import pygame
import sys
import time

# Initialize PyGame
pygame.init()

# Set up the display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Simulation")

# Define colors
WHITE = (255, 255, 255)

# Load car image (replacing the rectangle with an image of the car)
car_image = pygame.image.load('resources/car.png')  # Use the image with a transparent background
car_image = pygame.transform.scale(car_image, (250, 250))
car_width, car_height = car_image.get_size()  # Get size of the image for positioning
car_x = 50  # Initial x position
car_y = height // 2 - car_height // 2  # Center the car vertically

velocity = 0  # Initial velocity
distance = 0  # Initial distance
acceleration = 0  # Acceleration value (updated from planner)
max_velocity = 10  # Increase max velocity for faster movement

# Time settings
clock = pygame.time.Clock()

# Function to update car state from planner output
def update_car_state(action):
    global velocity, distance, car_x, acceleration
    if action == "accelerate":
        acceleration = 2  # Increase acceleration rate for visible change
    elif action == "decelerate":
        acceleration = -2  # Decrease velocity faster
    elif action == "stop":
        velocity = 0
        acceleration = 0

    # Update velocity and cap it at max/min values
    velocity += acceleration
    if velocity > max_velocity:
        velocity = max_velocity
    elif velocity < 0:
        velocity = 0

    # Update distance and car position based on velocity
    distance += velocity
    car_x += velocity  # Move the car across the screen

# Function to read actions from the saved file with timestamps
def read_actions_from_file(file_path):
    actions = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.strip():
                # Example: '0.000: accelerate [0.0]'
                parts = line.split(':')
                time_stamp = float(parts[0].strip())
                action = parts[1].strip().split()[0]
                actions.append((time_stamp, action))
    return actions

# Main function for PyGame visualization
def run_simulation(actions):
    global velocity, distance, car_x
    current_action_index = 0
    start_time = time.time()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background
        window.fill(WHITE)

        # Draw the car image instead of a rectangle
        window.blit(car_image, (car_x, car_y))

        # Display information (velocity and distance)
        font = pygame.font.Font(None, 36)
        distance_text = font.render(f'Distance: {int(distance)}', True, (0, 0, 0))
        window.blit(distance_text, (20, 20))

        velocity_text = font.render(f'Velocity: {round(velocity, 2)}', True, (0, 0, 0))
        window.blit(velocity_text, (20, 60))

        # Get the current time since the simulation started
        current_time = time.time() - start_time

        # Execute actions based on the timestamps
        if current_action_index < len(actions):
            action_time, action = actions[current_action_index]

            # If the current time matches the next action's timestamp, execute it
            if current_time >= action_time:
                update_car_state(action)
                current_action_index += 1

        # Update the display
        pygame.display.update()

        # Cap the frame rate at 60 FPS
        clock.tick(60)

    # Quit PyGame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Assuming the saved plan file is called 'plan.txt'
    actions_file = 'C:\\Users\\PC\\PycharmProjects\\nyx\\ex\\car\\plans\\plan1_pb09.pddl'  # The file where actions are stored
    actions = read_actions_from_file(actions_file)

    # Run the simulation with the actions
    run_simulation(actions)
