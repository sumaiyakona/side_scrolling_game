import pygame
from game_logic import main_game_loop
from interface import home_page

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Impact")

# Display home page
home_page(screen, WHITE)

# Start the main game loop
main_game_loop(screen, WHITE)