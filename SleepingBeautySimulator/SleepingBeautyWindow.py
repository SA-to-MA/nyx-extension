import pygame
class SleepingBeautyWindow:
    def __init__(self, window, sleeping_beauty, images, positions):
        ''' Window is pygame object of screen
        Sleeping beauty is object containing booleans of current state
        Images is dictionary containing image name and image path
        Positions is dictionary containing image name and position in window '''
        self.sleeping_beauty = sleeping_beauty
        self.images = images
        self.positions = positions
        self.window = window

    def draw(self):
        # reset window
        self.window.fill((255, 255, 255))
        # draw window
        if self.sleeping_beauty.window_closed:
            self.window.blit(self.images["window_closed"], self.positions["window"])
        else:
            self.window.blit(self.images["window_open"], self.positions["window"])
        # draw sleeping beauty
        if self.sleeping_beauty.deeply_asleep:
            self.window.blit(self.images["asleep"], self.positions["figure"])
        elif self.sleeping_beauty.almost_awake:
            self.window.blit(self.images["almost_awake"], self.positions["figure"])
        else:
            self.window.blit(self.images["awake"], self.positions["figure"])
        # draw alarm
        if self.sleeping_beauty.alarm_enabled:
            self.window.blit(self.images["alarm_enabled"], self.positions["alarm"])
            if self.sleeping_beauty.ringing:
                self.window.blit(self.images["alarm_ringing"], self.positions["alarm"])
        elif self.sleeping_beauty.alarm_disabled:
            self.window.blit(self.images["alarm_disabled"], self.positions["alarm"])
        # Update the display
        pygame.display.flip()

