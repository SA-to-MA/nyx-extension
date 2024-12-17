import pygame
import sys

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (224, 247, 250)
PASTEL_GREEN = (241, 248, 233)
DARK_GREEN = (0, 77, 64)
BUTTON_COLOR = (0, 121, 107)
BUTTON_HOVER = (0, 77, 64)

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MA-PDDL+ Solver")

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.hover_color if self.is_hovered else self.color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

# Create buttons
manual_button = Button("Manual Configuration", 150, 150, 300, 50, BUTTON_COLOR, BUTTON_HOVER)
upload_button = Button("Upload File", 150, 250, 300, 50, BUTTON_COLOR, BUTTON_HOVER)

# Main loop
running = True
while running:
    screen.fill(LIGHT_BLUE)

    # Draw title
    title_surface = font.render("Welcome to the MA-PDDL+ Solver", True, DARK_GREEN)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title_surface, title_rect)

    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    manual_button.is_hovered = manual_button.rect.collidepoint(mouse_pos)
    upload_button.is_hovered = upload_button.rect.collidepoint(mouse_pos)

    manual_button.draw(screen)
    upload_button.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if manual_button.is_clicked(event):
            print("Manual Configuration selected")
            # Add logic for manual configuration here

        if upload_button.is_clicked(event):
            print("Upload File selected")
            # Add logic for file upload here

    pygame.display.flip()

pygame.quit()
sys.exit()
