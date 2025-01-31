import pygame
class SleepingBeautyWindow:
    def __init__(self, window, sleeping_beauty):
        ''' Window is pygame object of screen
        Sleeping beauty is object containing booleans of current state
        Images is dictionary containing image name and image path
        Positions is dictionary containing image name and position in window '''
        self.sleeping_beauty = sleeping_beauty
        # set window
        self.window = window
        # Get current window size
        window_width, window_height = self.window.get_size()

        # Calculate scaling factor based on 1000x1000 base
        scale_x = window_width / 1000
        scale_y = window_height / 1000

        # Scale positions proportionally
        self.positions = {
            "window": (int(300 * scale_x), int(10 * scale_y)),
            "alarm": (int(740 * scale_x), int(280 * scale_y)),
            "figure": (int(170 * scale_x), int(310 * scale_y)),
            "kiss": (int(50 * scale_x), int(380 * scale_y)),
            "magnet": (int(700 * scale_x), int(750 * scale_y)),
            "circuit": (int(785 * scale_x), int(680 * scale_y)),
            "dresser": (int(700 * scale_x), int(400 * scale_y)),
            "chest": (int(590 * scale_x), int(675 * scale_y)),
        }
        # load raw images and store them in a dictionary
        images = {
            "window_closed": pygame.image.load("resources/window-closed.png"),
            "window_open": pygame.image.load("resources/window-open.png"),
            "asleep": pygame.image.load("resources/asleep.png"),
            "awake": pygame.image.load("resources/awake.png"),
            "almost_awake": pygame.image.load("resources/almost-awake.png"),
            "alarm_enabled": pygame.image.load("resources/alarm-enabled.png"),
            "alarm_disabled": pygame.image.load("resources/alarm-disabled.png"),
            "alarm_ringing": pygame.image.load("resources/alarm-ringing.png"),
            "kiss": pygame.image.load("resources/kiss.png"),
            "magnet": pygame.image.load("resources/magnet.png"),
            "open_circuit" : pygame.image.load("resources/open-circut.png"),
            "close_circuit": pygame.image.load("resources/closed-circut.png"),
            "dresser": pygame.image.load("resources/dresser.png"),
            "bedroom": pygame.image.load("resources/bedroom-cropped.jpg"),
            "chest": pygame.image.load("resources/chest.png"),
        }

        # Scale images proportionally
        self.images = {
            name: pygame.transform.scale(image,
                                         (int(image.get_width() * scale_x),
                                          int(image.get_height() * scale_y)))
            for name, image in images.items()
        }
        self.font = pygame.font.Font(None, 30)

    def draw_window(self):
        # draw window
        if self.sleeping_beauty.window_closed:
            self.window.blit(self.images["window_closed"], self.positions["window"])
        else:
            self.window.blit(self.images["window_open"], self.positions["window"])

    def draw_sleeping_beauty(self):
        if self.sleeping_beauty.deeply_asleep:
            self.window.blit(self.images["asleep"], self.positions["figure"])
        elif self.sleeping_beauty.almost_awake:
            self.window.blit(self.images["almost_awake"], self.positions["figure"])
        else:
            self.window.blit(self.images["awake"], self.positions["figure"])

    def draw_kiss(self):
        if self.sleeping_beauty.kissed:
            self.window.blit(self.images["kiss"], self.positions["kiss"])

    def draw_magnet_and_circuit(self):
        ''' Draw the magnet and circuit based on their states. '''
        # Draw magnet
        if self.sleeping_beauty.magnet_operational:
            self.window.blit(self.images["magnet"], self.positions["magnet"])

        # Draw circuit based on the state
        if self.sleeping_beauty.circuit:
            self.window.blit(self.images["close_circuit"], self.positions["circuit"])
            charging_time_text = f"Charging: {self.sleeping_beauty.charge}s"
            charging_time_surface = self.font.render(charging_time_text, True, (255, 0, 0))  # Red color
            # Position the charging time text near the circuit
            circuit_x, circuit_y = self.positions["circuit"]
            charging_time_position = (circuit_x, circuit_y - 25)  # Adjust vertical offset as needed
            self.window.blit(charging_time_surface, charging_time_position)
        else:
            self.window.blit(self.images["open_circuit"], self.positions["circuit"])

    def draw_alarm(self):
        if self.sleeping_beauty.alarm_enabled:
            if self.sleeping_beauty.ringing:
                self.window.blit(self.images["alarm_ringing"], self.positions["alarm"])
                # Render and draw ring time above the alarm clock
                ring_time_text = "Ring Time:" + str(self.sleeping_beauty.ring_time)
                ring_time_surface = self.font.render(ring_time_text, True, (255, 0, 0))  # Red color
                # Calculate the position above the alarm
                ring_time_position = (self.positions["alarm"][0], self.positions["alarm"][1] - 30)
                self.window.blit(ring_time_surface, ring_time_position)
            else:
                self.window.blit(self.images["alarm_enabled"], self.positions["alarm"])
        elif self.sleeping_beauty.alarm_disabled:
            self.window.blit(self.images["alarm_disabled"], self.positions["alarm"])

    def draw_constants(self):
        # draw bedroom
        background_image = pygame.transform.scale(self.images["bedroom"], self.window.get_size())  # Adjust size as needed
        self.window.blit(background_image, (0, 0))
        # draw chest
        self.window.blit(self.images["chest"], self.positions["chest"])
        # Draw dresser
        self.window.blit(self.images["dresser"], self.positions["dresser"])

    def draw(self):
        # reset pygame window
        self.window.fill((255, 255, 255))
        # draw constants
        self.draw_constants()
        # draw window open or closed
        self.draw_window()
        # draw sleeping beauty
        self.draw_sleeping_beauty()
        # draw kiss
        self.draw_kiss()
        # draw magnet and circuit
        self.draw_magnet_and_circuit()
        # draw alarm
        self.draw_alarm()
        # Update the display
        pygame.display.flip()

