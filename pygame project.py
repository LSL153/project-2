# Author: Wenyi Gong, Jiakai Hu, Shanlin Li 
# Date: 12/7/2024  
#Description: Using pygame to build a battle game.

import pygame
import sys

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (128, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 128)
DARK_GREEN = (0, 150, 0)

# Default display size
WIDTH, HEIGHT = 1200, 800  # Slightly larger size to fit all elements
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Game Settings")
