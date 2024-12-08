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

# Fonts
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 30)
font_small = pygame.font.Font(None, 20)
FONT = pygame.font.Font(None, 48) # This creates a Font object named FONT with the default system font (None) and a size of 48
TITLE_FONT = pygame.font.Font(None, 64) # This creates a Font object named TITLE_FONT with the default system font (None) and a larger size of 64（Prepare your skills).



# Global settings variables
totalmoney = 3000
userchargechance = 1
aichargechance = 1
preset = "preset1"


# Button class
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
