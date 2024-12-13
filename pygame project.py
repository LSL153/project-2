# Author: Wenyi Gong, Jiakai Hu, Shanlin Li 
# Date: 12/7/2024  
#Description: Using pygame to build a battle game.
#This is the old version of our code, please use the attach file called phaseBattleUI to run the program.
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
    def draw(self, screen, font):
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = font.render(self.text, True, BLACK)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class UnitButton:
    def __init__(self, unit, x, y, is_user=True):
        self.unit = unit
        self.rect = pygame.Rect(x, y, 330, 30)
        self.color = BLUE if is_user else RED
        self.selected = False

    def draw(self, surface):
        # Draw unit rectangle with selected color
        color = YELLOW if self.selected else self.color
        pygame.draw.rect(surface, color, self.rect)

        # Draw health bar (for now just using full health)
        health_bar_width = int(self.rect.width)
        health_bar_rect = pygame.Rect(self.rect.x, self.rect.y, health_bar_width, 5)
        pygame.draw.rect(surface, GREEN, health_bar_rect)

        # Draw name
        text = font_medium.render(self.unit.name, True, BLACK)
        surface.blit(text, (self.rect.x + 5, self.rect.y + 8))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# InputBox class for interactive fields
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = font_small.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = GREY if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font_small.render(self.text, True, BLACK)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_value(self):
        return self.text

    def set_value(self, text):
        self.text = text
        self.txt_surface = font_small.render(self.text, True, BLACK)
    
class MeleeUnit():
    # Class Variable
    category = 'Melee Unit'
    damaged = False
    defeated = False
    frenzy = False
    chargedefvsl = False
    crumbling = False

    def __init__(self, name, faction, unitsize, cost, health, meleeatk, meleedef, chargebonus,
                 fireres, magres, phyres, misres, wardsave, basedmg, apdmg, meleecd,
                 antiinfantry, antilarge, armor, magatk, fireatk, isinfantry, islarge):
        # Instance Variable
        self.name = name
        self.faction = faction
        self.unitsize = unitsize
        self.cost = cost
        self.health = health
        self.totalhealth = health * unitsize
        self.remainhealth = health * unitsize
        self.meleeatk = meleeatk
        self.meleedef = meleedef
        self.chargebonus = chargebonus
        self.fireres = fireres
        self.magres = magres
        self.misres = misres
        self.phyres = phyres
        self.wardsave = wardsave
        self.basedmg = basedmg
        self.apdmg = apdmg
        self.meleecd = meleecd
        self.antiinfantry = antiinfantry
        self.antilarge = antilarge
        self.armor = armor
        self.magatk = magatk
        self.fireatk = fireatk
        self.isinfantry = isinfantry
        self.islarge = islarge


# Button instances with adjusted positions
start_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 20, 100, 40, "Start")
setting_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 80, 100, 40, "Setting")
reset_button = Button(WIDTH - 180, HEIGHT - 70, 80, 30, "Reset")
confirm_button = Button(WIDTH - 90, HEIGHT - 70, 80, 30, "Confirm")

# InputBox instances for settings
totalmoney_input = InputBox(300, 130, 140, 32, str(totalmoney))
userchargechance_input = InputBox(300, 180, 140, 32, str(userchargechance))
aichargechance_input = InputBox(300, 230, 140, 32, str(aichargechance))
