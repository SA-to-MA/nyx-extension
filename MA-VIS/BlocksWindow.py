import pygame


class BlocksWindow:
    def __init__(self, window, car):
        """
        :param window: Pygame screen object for rendering the simulation.
        :param car: Car object containing the state to visualize.
        """
        self.car = car
        self.window = window
        self.font = pygame.font.Font(None, 30)

        # Load and resize images into a dictionary
        self.images = {
            "car": pygame.transform.scale(pygame.image.load("resources/car.png"), (250, 107)),
            "goal_reached": pygame.transform.scale(pygame.image.load("resources/goal.png"), (120, 120)),
            "background": pygame.transform.scale(pygame.image.load("resources/road.jpg"), self.window.get_size()),
            "wind_resistance": pygame.transform.scale(pygame.image.load("resources/wind.png"), (70, 70)),
            "engine_blow": pygame.transform.scale(pygame.image.load("resources/engine_blow.png"), (150, 150)),
        }

        # Store positions for various elements
        window_width, window_height = self.window.get_size()
        self.positions = {
            "car": [window_width * 0.01, window_height * 0.6],  # 5% from the left, 85% from the top
            "goal": [window_width * 0.4, window_height * 0.4],
            "wind_resistance": (window_width * 0.8, window_height * 0.6),  # 10% from left, 75% from top
            "engine_blow": (window_width * 0.15, window_height * 0.85),  # 15% from left, 85% from top
        }

    def draw_background(self):
        """
        Draws the road or background image.
        """
        background = pygame.transform.scale(self.images["background"], self.window.get_size())
        self.window.blit(background, (0, 0))


    def draw_car(self):
        """
        Updates the car's position based on its distance from starting point, and draws it.
        """
        if self.car.running:
            self.positions["car"][0] = 50 + self.car.d * 10
        car_x, car_y = self.positions["car"]
        self.window.blit(self.images["car"], (car_x, car_y))

    def draw_goal(self):
        """
        Displays a "goal reached" image if the car has reached its goal.
        """
        if self.car.goal_reached:
            self.window.blit(self.images["goal_reached"], self.positions["goal"])

    def draw_wind_resistance(self):
        """
        Displays a wind resistance effect if velocity is high.
        """
        if self.car.v >= 50:
            self.window.blit(self.images["wind_resistance"], self.positions["wind_resistance"])

    def draw_engine_blow(self):
        """
        Displays an engine blow effect if the engine has exploded.
        """
        if self.car.engine_blown:
            self.window.blit(self.images["engine_blow"], self.positions["engine_blow"])

    def draw_statistics(self):
        """
        Draws the car's statistics (time, velocity, distance, acceleration)
        centered horizontally at the bottom, within a white box with a title.
        """
        # Title text
        title_text = "Statistics:"
        title_surface = self.font.render(title_text, True, (0, 0, 0))  # Black text
        title_width, title_height = title_surface.get_size()

        # Statistics text
        stats_text = (
            f"Time: {self.car.running_time:.2f}s | "
            f"Distance: {self.car.d:.2f}m | "
            f"Velocity: {self.car.v:.2f}m/s | "
            f"Acceleration: {self.car.a:.2f}m/s²"
        )
        stats_surface = self.font.render(stats_text, True, (0, 0, 0))  # Black text
        stats_width, stats_height = stats_surface.get_size()

        # Box dimensions
        padding = 10  # Padding inside the box
        box_width = max(title_width, stats_width) + 2 * padding
        box_height = title_height + stats_height + 3 * padding  # Extra padding for spacing between title and stats
        x_pos = (self.window.get_width() - box_width) // 2
        y_pos = self.window.get_height() - box_height - 50  # Adjusted height for placement

        # Draw the white box with a border
        pygame.draw.rect(self.window, (255, 255, 255), (x_pos, y_pos, box_width, box_height))  # White box
        pygame.draw.rect(self.window, (0, 0, 0), (x_pos, y_pos, box_width, box_height), 2)  # Black border

        # Draw the title
        title_x = x_pos + (box_width - title_width) // 2
        title_y = y_pos + padding
        self.window.blit(title_surface, (title_x, title_y))

        # Draw the statistics text below the title
        stats_x = x_pos + (box_width - stats_width) // 2
        stats_y = title_y + title_height + padding
        self.window.blit(stats_surface, (stats_x, stats_y))

    def draw(self):
        """
        Draws all elements in the simulation.
        """
        # Reset pygame window
        self.window.fill((255, 255, 255))  # White background
        # Draw background
        self.draw_background()
        # Draw the moving car
        self.draw_car()
        # Draw wind resistance
        self.draw_wind_resistance()
        # Draw engine blow
        self.draw_engine_blow()
        # Draw goal if reached
        self.draw_goal()
        # draw statistics of car
        self.draw_statistics()
        # Update the display
        pygame.display.flip()
