# Author: Wenyi Gong, Jiakai Hu, Shanlin Li 
# Date: 12/7/2024  
#Description: Using pygame to build a battle game.

import threading
import time
import math
from queue import Queue
import pygame
import sys

from Altdorf_EMPandTK_TuiVersion import *

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

turn = "user"  # The game starts with the user's turn
aiwin = False
userwin = False
fight_in_progress = False


def checkrepeat(unit_list):
    """
    To check if there's repeated units in list
    :param unit_list: The list which store units
    :return: return the units in list which has no repeated units
    """
    unique_units = []
    seen = {}
    for unit in unit_list:
        if unit.name in seen:
            seen[unit.name].append(unit)
        else:
            seen[unit.name] = [unit]
            unique_units.append(unit)
    return unique_units


# In[2]:


def aichooseunit():
    """
    The function which let the ai, which is the enemy choice units
    :return: None
    """
    global totalmoney
    aimoneyleft = totalmoney
    global aiunits
    aiunits = []
    while True:
        numaichosen = int(random.uniform(0, len(unitroster)))
        if(numaichosen==len(unitroster)):
            numaichosen-=1
        aichosen = copy.copy(unitroster[numaichosen])
        aichosen.name += " ai"
        if(aimoneyleft>=aichosen.cost):
            aiunits.append(aichosen)
            aimoneyleft -= aichosen.cost
        if(aimoneyleft<325):
            break





aichooseunit()
checkrepeat(aiunits)
print("\nHere are the units chosen by the ai:\n")
sortandprint(aiunits)
battle_logs = []
message_queue = Queue()

def crumblingdmg(crumbling_unit: MeleeUnit, other_unit: MeleeUnit):
    """
    The function which set the damage to the crumbling unit
    :param crumbling_unit: the unit has a crumbling status
    :param other_unit: the other unit
    :return:
    """
    if crumbling_unit.remainhealth > 0 and other_unit.remainhealth > 0:
        dmgdealt = int(random.uniform(14, 28))
        crumbling_unit.remainhealth -= dmgdealt
        if crumbling_unit.remainhealth < 0:
            crumbling_unit.remainhealth = 0
        message = (f"{crumbling_unit.name} is crumbling, it took {dmgdealt} damage, remain health is {crumbling_unit.remainhealth}.")
        message_queue.put(message)
        threading.Timer(1, crumblingdmg, [crumbling_unit, other_unit]).start()

def attack(unit1, unit2, chargeland):
    """
    the function which allows unit attack to each other
    :param unit1: one unit do or take the attack
    :param unit2: one unit do or take the attack
    :param chargeland: if user or ai want to use charge
    :return:
    """
    starttime = time.time()
    countu2 = 1
    countu1 = 1
    while (unit1.remainhealth > 0 and unit2.remainhealth > 0):
        currenttime = round(time.time() - starttime, 2)

        # Handle crumbling damage
        if unit2.crumbling:
            if (unit2.remainhealth <= unit2.totalhealth / 2 and countu2 == 1):
                crumblingdmg(unit2, unit1)
                countu2 += 1
        if unit1.crumbling:
            if (unit1.remainhealth <= unit1.totalhealth/2 and countu1 ==1):
                crumblingdmg(unit1,unit2)
                countu1 += 1
        if chargeland and currenttime <= 15:
            dmgdealt = totaldmghit(unit1, unit2, 1)
            unit2.remainhealth -= dmgdealt
            if unit2.remainhealth < 0:
                unit2.remainhealth = 0

            message = (f"At time {currenttime}s, {unit1.name} did a charge attack on {unit2.name} "
                       f"with {dmgdealt} damage, {unit2.name} remain health is {unit2.remainhealth}.")
            message_queue.put(message)

            if unit2.chargedefvsl and unit1.islarge:
                message = "But charge defense vs large triggered, charge bonus from large unit got reduced."
                message_queue.put(message)

            if unit2.remainhealth == 0:
                break
            time.sleep(unit1.meleecd - ((time.time() - starttime) % unit1.meleecd))
        else:
            dmgdealt = totaldmghit(unit1, unit2, 0)
            unit2.remainhealth -= dmgdealt
            if unit2.remainhealth < 0:
                unit2.remainhealth = 0

            message = (f"At time {currenttime}s, {unit1.name} did an attack on {unit2.name} "
                       f"with {dmgdealt} damage, {unit2.name} remain health is {unit2.remainhealth}.")
            message_queue.put(message)

            if unit2.remainhealth == 0:
                break
            
            time.sleep(unit1.meleecd - ((time.time() - starttime) % unit1.meleecd))

def fight(unit1, unit2, achargeb, bchargea):
    """
    The function which let the units fight each other, and check if there is a defeated unit
    :param unit1: one unit
    :param unit2: one unit
    :param achargeb: to see if unit1 wants charge unit2
    :param bchargea: to see if unit2 wants charge unit 1
    :return:
    """
    global fight_in_progress
    fight_in_progress = True  # Fight is starting
    p1 = threading.Thread(target=attack, args=(unit1, unit2, achargeb))
    p2 = threading.Thread(target=attack, args=(unit2, unit1, bchargea))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    # Post-fight logic
    fight_in_progress = False  # Fight is complete
    if defeatcheck(unit1):
        msg = f"{unit2.name} wins!"
        message_queue.put(msg)
        unit2.totalhealth = unit2.remainhealth
        unit2.unitsize = math.ceil(unit2.totalhealth / unit2.health)
        msg = f"{unit2.name} still have {unit2.totalhealth} health and {unit2.unitsize} entities"
        message_queue.put(msg)
        unit2.damaged = True

    if defeatcheck(unit2):
        msg = f"{unit1.name} wins!"
        message_queue.put(msg)
        unit1.totalhealth = unit1.remainhealth
        unit1.unitsize = math.ceil(unit1.totalhealth / unit1.health)
        msg = f"{unit1.name} still have {unit1.totalhealth} health and {unit1.unitsize} entities"
        message_queue.put(msg)
        unit1.damaged = True


# Button class
class Button:
    def __init__(self, x, y, w, h, text):
        """
        The initial status of button
        :param x: x coordinate
        :param y: y coordinate
        :param w: width
        :param h: height
        :param text: the text on the button
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        """
        the function allows us to draw the button on the screen
        :param screen: screen
        :param font: font size
        :return: None
        """
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = font.render(self.text, True, BLACK)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        """
        allow us to check if the button is clicked
        :param pos: pos
        :return: if the button is clicked
        """
        return self.rect.collidepoint(pos)


class UnitButton:
    def __init__(self, unit, x, y, is_user=True):
        """
        The initial status of button
        :param unit: unit
        :param x: x coordinate
        :param y: y coordinate
        :param is_user: if it's user
        """
        self.unit = unit
        self.rect = pygame.Rect(x, y, 330, 30)
        self.color = BLUE if is_user else RED
        self.selected = False

    def draw(self, surface):
        """
        the function which allow us to draw the unit button on the screen
        :param surface: screen
        :return: None
        """
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
        """
        allow us to check if the button is clicked
        :param pos: pos
        :return: if the button is clicked
        """
        return self.rect.collidepoint(pos)


# InputBox class for interactive fields
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        """
        The initial status of input box
        :param x: x coordinate
        :param y: y coordinate
        :param w: width
        :param h: height
        :param text: the text on the screen
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = font_small.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        """
        to handle events when we press the mouse
        :param event: event
        :return:None
        """
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
        """
        the function allows us to draw the input box
        :param screen: screen
        :return: None
        """
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_value(self):
        """
        return the text value of the input box
        :return: text
        """
        return self.text

    def set_value(self, text):
        """
        set the text value of the input box
        :param text: text
        :return: None
        """
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
    magicShield = False

    def __init__(self, name, faction, unitsize, cost, health, meleeatk, meleedef, chargebonus,
                 fireres, magres, phyres, misres, wardsave, basedmg, apdmg, meleecd,
                 antiinfantry, antilarge, armor, magatk, fireatk, isinfantry, islarge):
        """
        The initial status of melee unit
        :param name: name
        :param faction: faction
        :param unitsize: how many single soldier in a unit
        :param cost: cost
        :param health: health
        :param meleeatk: the melee attack
        :param meleedef: the melee defense
        :param chargebonus: charge bonus
        :param fireres: fire resistance
        :param magres: magic resistance
        :param phyres: physics resistance
        :param misres: missile resistance
        :param wardsave: ward save
        :param basedmg: base damage
        :param apdmg: ap damage
        :param meleecd: melee cd
        :param antiinfantry: anti infantry
        :param antilarge: anti large
        :param armor: armor
        :param magatk: magic attack
        :param fireatk: fire attack
        :param isinfantry: if it's infantry
        :param islarge: if it's large
        """
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
        
        # for reset
        self.original_name = name
        self.original_basedmg = basedmg
        self.original_apdmg = apdmg
        self.original_meleedef = meleedef
        self.original_meleeatk = meleeatk
        self.original_charbonus = chargebonus
        self.original_cost = cost
        self.original_max_health = health * unitsize


# Button instances with adjusted positions
start_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 20, 100, 40, "Start")
setting_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 80, 100, 40, "Setting")
reset_button = Button(WIDTH - 180, HEIGHT - 70, 80, 30, "Reset")
confirm_button = Button(WIDTH - 90, HEIGHT - 70, 80, 30, "Confirm")
quit_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 140, 100, 40, "Quit")

# InputBox instances for settings
totalmoney_input = InputBox(300, 130, 140, 32, str(totalmoney))
userchargechance_input = InputBox(300, 180, 140, 32, str(userchargechance))
aichargechance_input = InputBox(300, 230, 140, 32, str(aichargechance))

# Flag to track which page is active
page = "welcome"

# all_units = [
#     MeleeUnit("Greatswords", "Empire", 120, 900, 68, 32, 30, 18, 0, 0, 0, 0, 0, 9, 23, 4.3, 10, 0, 95, False, False,
#               True, False),
#     MeleeUnit("Halberdiers", "Empire", 120, 550, 65, 26, 42, 8, 0, 0, 0, 0, 0, 8, 20, 5.6, 0, 16, 30, False, False,
#               True, False),
# ]
# Objects of MeleeUnit class
Greatswords = MeleeUnit("Greatswords","Empire", 120,900,68,32,30,18,0,0,0,0,0,9,23,4.3,10,0,95,False,False,True,False)
# print(Greatswords.frenzy)
Halberdiers = MeleeUnit("Halberdiers","Empire", 120,550,65,26,42,8,0,0,0,0,0,8,20,5.6,0,16,30,False,False,True,False)
Halberdiers.chargedefvsl=True
Flagellants = MeleeUnit("Flagellants","Empire", 120,600,65,32,12,24,0,0,0,0,0,25,8,4.5,0,0,0,False,False,True,False)
Flagellants.frenzy = True
# print(Greatswords.frenzy)
# print(Flagellants.frenzy)
Swordsman = MeleeUnit("Swordsman","Empire", 120,400,61,32,32,14,0,0,0,0,0,21,7,4.3,0,0,30,False,False,True,False)
SpearmanShields = MeleeUnit("Spearman(Shields)","Empire", 120,375,61,20,42,4,0,0,0,0,0,19,6,4.4,0,15,30,False,False,True,False)
SpearmanShields.chargedefvsl=True
SpearmanEMP = MeleeUnit("Spearman(Empire)","Empire", 120,325,61,20,34,4,0,0,0,0,0,19,6,5.7,0,15,30,False,False,True,False)
SpearmanEMP.chargedefvsl=True
EmpireKnights = MeleeUnit("Empire Knights","Empire", 60,900,92,26,30,48+48,0,0,0,0,0,21,9,5.1,0,0,110,False,False,False,True)
Reiksguard = MeleeUnit("Reiksguard","Empire", 60,1150,100,34,31,62+66,0,0,0,0,0,28,12,5.1,0,0,120,False,False,False,True)
DemigryphKnights = MeleeUnit("Demigryph Knights","Empire", 32,1400,202,38,38,60+75,0,0,0,0,0,19,39,4.7,0,0,125,False,False,False,True)
DemigryphKnightsHalberds = MeleeUnit("Demigryph Knights(Halberds)","Empire", 32,1500,202,32,32,48+62,0,0,0,0,0,17,35,4.8,0,25+2,125,False,False,False,True)
KnightsOfTheBlazingSun = MeleeUnit("Knights of the Blazing Sun","Empire", 60,1200,100,40,26,78+100,0,25,0,0,0,29,13,5.1,0,0,100,False,False,False,True)
# Testunit = MeleeUnit("Testunit","Test", 120,900,68,32,30,18,15,23,31,5,26,9,23,4.3,10,0,95,True,True,False,True)

all_units = [Greatswords, Halberdiers, Flagellants, Swordsman, SpearmanShields, SpearmanEMP,
             EmpireKnights, Reiksguard, DemigryphKnights, DemigryphKnightsHalberds, KnightsOfTheBlazingSun]
SkeletonSpearmenTK = MeleeUnit("SkeletonSpearmen(Tomb Kings)","Tomb Kings", 160,350,53,14,30,3,0,0,0,0,0,18,6,4.5,0,14,20,False,False,True,False)
SkeletonSpearmenTK.chargedefvsl=True
SkeletonSpearmenTK.crumbling = True #14-28
all_units.append(SkeletonSpearmenTK)
SkeletonWarriorsTK = MeleeUnit("Skeleton Warriors(Tomb Kings)","Tomb Kings", 160,325,53,18,22,5,0,0,0,0,0,20,6,4.3,0,0,20,False,False,True,False)
SkeletonWarriorsTK.crumbling = True
all_units.append(SkeletonWarriorsTK)
NehekharaWarriors = MeleeUnit("Nehekhara Warriors","Tomb Kings", 120,525,68,32,22,15,0,0,0,0,0,26,7,4.5,0,0,45,False,False,True,False)
NehekharaWarriors.crumbling = True
all_units.append(NehekharaWarriors)
TombGuard = MeleeUnit("Tomb Guard","Tomb Kings", 120,750,74,32,41,8,0,0,0,0,0,33,9,4.4,0,0,55,False,False,True,False)
TombGuard.crumbling = True
all_units.append(TombGuard)
TombGuardHalberds = MeleeUnit("Tomb Guard(Halberds)","Tomb Kings", 120,850,74,25,47,5,0,0,0,0,0,9,20,4.9,0,19,55,False,False,True,False)
SkeletonSpearmenTK.chargedefvsl=True
TombGuardHalberds.crumbling = True
all_units.append(TombGuardHalberds)

SkeletonHorsemen = MeleeUnit("Skeleton Horsemen","Tomb Kings", 60,400,73,24,26,34+40,0,0,0,0,0,21,7,4.5,0,0,30,False,False,False,True)
SkeletonHorsemen.crumbling = True
all_units.append(SkeletonHorsemen)
NehekharaHorsemen = MeleeUnit("Nehekhara Horsemen","Tomb Kings", 60,650,98,28,34,26+32,0,0,0,0,0,28,10,5,0,0,50,False,False,False,True)
NehekharaHorsemen.crumbling = True
all_units.append(NehekharaHorsemen)
NecropolisKnights = MeleeUnit("Necropolis Knights","Tomb Kings", 24,1425,295,40,43,52+56,0,0,0,0,0,21,40,5.4,0,0,110,False,False,False,True)
NecropolisKnights.crumbling = True
all_units.append(NecropolisKnights)
NecropolisKnightsHalberds = MeleeUnit("Necropolis Knights(Halberds)","Tomb Kings", 24,1575,295,32,37,40+44,0,0,0,0,0,19,36,5.4,0,28+3,110,False,False,False,True)
NecropolisKnightsHalberds.crumbling = True
all_units.append(NecropolisKnightsHalberds)

# Function to display unit details on the screen (transfer from TUI)
def display_unit_info(unit_button):
    """
    display the information about the unit
    :param unit_button: the button of the unit
    :return: print the information about the unit
    """
    unit = unit_button.unit
    font = font_medium
    y_offset = 420

    # Left Column - Basic Info
    info_text_left = [
        f"Unit: {unit.name}",
        f"Faction: {unit.faction}",
        f"Size: {unit.unitsize}",
        f"Cost: ${unit.cost}",
        f"Health: {unit.totalhealth}",
        f"Melee Attack: {unit.meleeatk}",
        f"Melee Defense: {unit.meleedef}",
        f"Charge Bonus: {unit.chargebonus}",
        f"Base Damage: {unit.basedmg}",
        f"Armor-piercing Damage: {unit.apdmg}",
        f"Melee Interval: {unit.meleecd}",
        f"Armor: {unit.armor}",
    ]

    # Right Column - Stats Info
    info_text_right = [
        f"Fire Resistance: {unit.fireres}",
        f"Magic Resistance: {unit.magres}",
        f"Missile Resistance: {unit.misres}",
        f"Physical Resistance: {unit.phyres}",
        f"Ward Save: {unit.wardsave}",
        f"Anti-infantry Value: {unit.antiinfantry}",
        f"Anti-large Value: {unit.antilarge}",
        f"Is infantry: {unit.isinfantry}",
        f"Is large: {unit.islarge}",
        f"Category: {unit.category}",
        f"Frenzy: {unit.frenzy}",
        f"Charge defense vs large: {unit.chargedefvsl}",
    ]

    # Display each piece of information for left column
    for text in info_text_left:
        info_surface = font.render(text, True, BLACK)
        screen.blit(info_surface, (50, y_offset))
        y_offset += 30

    # Display each piece of information for right column
    y_offset = 420  # Reset the offset for the right column
    for text in info_text_right:
        info_surface = font.render(text, True, BLACK)
        screen.blit(info_surface, (430, y_offset))  # Position the right column info
        y_offset += 30


# Function to toggle window size
def toggle_window_size(fullscreen=False):
    """
    function to toggle window size
    :param fullscreen: check if the window is fullscreen
    :return: None
    """
    global screen
    if fullscreen:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 500), pygame.RESIZABLE)
skills = [
    {"name": "Frenzy", "cost": 50, "attribute": "Increase damage by 10%"},
    {"name": "Magic Shield", "cost": 50, "attribute": "Increase melee defense by 10%"},
    #{"name": "Speed Boost", "cost": 25, "attribute": "Increase movement speed by 15%"},
    # {"name": "Ice Blast", "cost": 30, "attribute": "Slow enemy by 20%"},
    # {"name": "Thunder Strike", "cost": 40, "attribute": "Stun enemy for 2 seconds"}
]
# Helper function to render text

def render_text(text, font, color, x, y, max_width=None):
    """
    Renders text on the screen at the specified position.
    If max_width is provided, the text is wrapped to fit within the specified width.

    Args:
        text (str): The text to render.
        font (pygame.font.Font): The font to use for rendering the text.
        color (tuple): The color of the text as an RGB tuple.
        x (int): The x-coordinate for rendering the text.
        y (int): The y-coordinate for rendering the text.
        max_width (int, optional): The maximum width for the text before wrapping.
    """
    if max_width:
        words = text.split()
        line = ""
        y_offset = 0
        for word in words:
            test_line = f"{line} {word}".strip()
            if font.size(test_line)[0] > max_width:
                label = font.render(line, True, color)
                screen.blit(label, (x, y + y_offset))
                line = word
                y_offset += font.size(line)[1] + 5
            else:
                line = test_line
        label = font.render(line, True, color)
        screen.blit(label, (x, y + y_offset))
    else:
        label = font.render(text, True, color)
        screen.blit(label, (x, y))

def battle_start():
    """
    Displays the 'Battle Start!' screen for a duration of 3 seconds.
    Transitions back to the main menu or another interface after the duration.

    This function clears the screen, renders the battle message, and uses a timer
    to manage the duration of the display.
    """
    # running = True
    # start_time = pygame.time.get_ticks()

    # while running:
    screen.fill(WHITE)
    battle_text = font_large.render("Battle Start!", TITLE_FONT, BLACK)
    # welcome_text = font_large.render("Welcome!", True, BLACK)
    screen.blit(battle_text, battle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()

        # Wait for 3 seconds, then return to main menu
        # if pygame.time.get_ticks() - start_time > 2000:
        #     # running = False
        #     # print("battle_text finish")
        #     page = "Battle"



# In[6]:


# Main loop
def main():
    """
    the main method for the game
    :return: None
    """
    # the global variable which needed
    global page, totalmoney, userchargechance, aichargechance, preset, unit_buttons, confirm_button, start_button, setting_button
    global battle_logs, turn, aiwin, userwin, fight_in_progress
    user_can_interact = True
    running = True
    fullscreen = False
    selected_unit_button = None
    selected_confirmed_button = None
    confirmed_units = {}
    confirmed_units_list = []
    confirmed_buttons = []
    confirmed_buttons_list = []
    selected_skill = None 
    selected_skills = [] 
    unit_buttons = []
    start_x, start_y = 50, 70
    column_gap, row_gap = 350, 40
    buttons_per_column = 7  # Two buttons per column
    mouse_pos = (0, 0)
    final_units = []
    name_tracker = {unit.name: [] for unit in all_units}
    selected_user_unit = None
    selected_enemy_unit = None

    def recalculate_button_positions():
        """
        Recalculates the button positions so that they won't block each other on the screen
        :return: None
        """
        start_x, start_y = 750, 420  # Starting position
        row_gap = 40  # Gap between rows

        for i, button in enumerate(confirmed_buttons):
            button.rect.topleft = (start_x, start_y + i * row_gap)

    #print the unit buttons on the screen
    for i, unit in enumerate(all_units):
        row = i % buttons_per_column  # Row index (0 or 1)
        col = i // buttons_per_column  # Column index
        x = start_x + col * column_gap
        y = start_y + row * row_gap
        unit_buttons.append(UnitButton(unit, x, y))

    while running:
        screen.fill(WHITE)

        # Welcome Page
        if page == "welcome":
            # Display Welcome message
            welcome_text = font_large.render("Welcome!", True, BLACK)
            screen.blit(welcome_text, welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

            # Draw buttons
            start_button.draw(screen, font_small)
            setting_button.draw(screen, font_small)
            quit_button.draw(screen, font_small)

        # Settings Page
        elif page == "setting":
            # Display setting message
            setting_text = font_medium.render("Settings", True, BLACK)
            screen.blit(setting_text, (50, 20))

            # the setting of the game
            preset_text = font_small.render("Select Preset:", True, BLACK)
            screen.blit(preset_text, (50, 80))
            preset1_button = Button(300, 80, 80, 30, "Preset 1")
            preset2_button = Button(400, 80, 80, 30, "Preset 2")
            preset1_button.draw(screen, font_small)
            preset2_button.draw(screen, font_small)

            totalmoney_label = font_small.render("Total Money:", True, BLACK)
            screen.blit(totalmoney_label, (50, 130))
            totalmoney_input.draw(screen)

            userchargechance_label = font_small.render("User Charge Chance:", True, BLACK)
            screen.blit(userchargechance_label, (50, 180))
            userchargechance_input.draw(screen)

            aichargechance_label = font_small.render("AI Charge Chance:", True, BLACK)
            screen.blit(aichargechance_label, (50, 230))
            aichargechance_input.draw(screen)

            reset_button.draw(screen, font_small)
            confirm_button.draw(screen, font_small)

        # Page that user choose their units
        elif page == "Prepare Your Units":
            prepare_unit_text = font_large.render("Prepare Your Units", True, BLACK)
            screen.blit(prepare_unit_text, (400, 10))
            gold_text = font_medium.render(f"Gold: {totalmoney}", True, BLACK)
            screen.blit(gold_text, (980, 10))
            warning_text = font_medium.render(f"Save money for skills", True, RED)
            screen.blit(warning_text, (980, 30))
            delete_button = Button(840, 760, 100, 30, "Delete")
            delete_button.draw(screen, font_medium)
            confirm_button = Button(960, 760, 100, 30, "Confirm")
            confirm_button.draw(screen, font_medium) 
            nextstep_button = Button(1080, 760, 100, 30, "Next")
            nextstep_button.draw(screen, font_medium)

            # unit_buttons = [UnitButton(unit, 50, 60 + i * 30) for i, unit in enumerate(all_units)]
            # Draw the units button for the user to choose
            for unit in unit_buttons:
                unit.draw(screen)
            # Draw the units button that the user chose
            for unit in confirmed_buttons:
                unit.draw(screen)
            for button in confirmed_buttons:
                button.draw(screen)  # Draw the button normally
                unit_name = button.unit.name
                # count = confirmed_units[unit_name]['count']
                # Draw the count near the button
                # count_text = font_medium.render(f"x{count}", True, BLACK)
                # screen.blit(count_text, (button.rect.x + button.rect.width + 10, button.rect.y + 10))
            if selected_unit_button:
                display_unit_info(selected_unit_button)
            pygame.display.flip()

        # Skill Page (next)
        # Updated Skill Page Layout
        elif page == "next":
            # Draw title
            render_text("Prepare Your Skills", TITLE_FONT, BLACK, WIDTH // 2 - 200, 20)

            # Draw gold label
            render_text(f"Gold: {totalmoney}", FONT, BLACK, WIDTH - 250, 40)

            # Draw skills display block
            pygame.draw.rect(screen, BLACK, pygame.Rect(50, 100, 1100, 200), 2)
            render_text("Skills", FONT, BLACK, 60, 110)
            for idx, skill in enumerate(skills):
                skill_button = pygame.Rect(60 + (idx % 4) * 270, 160 + (idx // 4) * 70, 250, 50)
                pygame.draw.rect(screen, BLUE if skill == selected_skill else BLACK, skill_button, 2)
                render_text(skill["name"], FONT, BLACK, 70 + (idx % 4) * 270, 170 + (idx // 4) * 70)

            # Draw information block
            # Draw information block
            pygame.draw.rect(screen, BLACK, pygame.Rect(50, 350, 550, 300), 2)
            render_text("Information", FONT, BLACK, 60, 360)

            # Render selected_skill information
            if selected_skill:  # Ensure selected_skill is not None
                render_text(f"Name: {selected_skill['name']}", FONT, BLACK, 60, 410)
                render_text(f"Cost: {selected_skill['cost']}", FONT, BLACK, 60, 460)
                render_text(f"Attribute: {selected_skill['attribute']}", FONT, BLACK, 60, 510, max_width=530)
            else:
                render_text("No skill selected", FONT, BLACK, 60, 410)  # Show placeholder text if no skill selected
            # Draw pick block
            pygame.draw.rect(screen, BLACK, pygame.Rect(650, 350, 450, 300), 2)
            render_text("Pick", FONT, BLACK, 660, 360)
            for idx, picked in enumerate(selected_skills):
                render_text(picked, FONT, BLACK, 660, 410 + idx * 40)

            # for i, unit in enumerate(confirmed_units_list):
            #     button = UnitButton(unit, 750, 420 + i * 40)
            #     confirmed_buttons_list.append(button)

            start_x, start_y = 660, 395  # Starting position for the first button
            button_height, button_gap = 30, 5  # Height of each button and gap between buttons

            # draw the unit button the user chose
            for i, unit_button in enumerate(confirmed_buttons_list):
                y = start_y + i * (button_height + button_gap)  # Position each button vertically
                unit_button.rect.topleft = (start_x, y)  # Set the top-left position of the button
                unit_button.rect.height = button_height  # Ensure consistent button height
                unit_button.color = YELLOW if unit_button.selected else BLUE
                unit_button.draw(screen)  # Draw the button


            # Draw buttons equidistantly below information and pick blocks
            confirm_button = pygame.Rect(250, 700, 200, 60)
            delete_button = pygame.Rect(500, 700, 200, 60)
            start_button = pygame.Rect(750, 700, 200, 60)

            pygame.draw.rect(screen, DARK_GREEN, confirm_button)
            pygame.draw.rect(screen, RED, delete_button)
            pygame.draw.rect(screen, BLUE, start_button)

            render_text("Confirm", FONT, WHITE, 280, 715)
            render_text("Delete", FONT, WHITE, 530, 715)
            render_text("Start!", FONT, BLACK, 780, 715)

            # Event handling for skill page
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Left-click
                    pos = event.pos
                    for unit_button in confirmed_buttons_list:
                        if unit_button.is_clicked(pos):
                            for other_button in confirmed_buttons_list:
                                other_button.selected = False  # Deselect others
                            unit_button.selected = True
                            selected_unit_button = unit_button  # Update the selected unit
                            print(f"Selected unit: {unit_button.unit.name}")
                            break
                    # Check skill selection
                    for idx, skill in enumerate(skills):
                        skill_button = pygame.Rect(60 + (idx % 4) * 270, 160 + (idx // 4) * 70, 250, 50)
                        if skill_button.collidepoint(pos):
                            selected_skill = skill
                            print(f"Selected skill: {selected_skill}")  # Debugging
                            break

                        # Confirm button
                        if confirm_button.collidepoint(pos):
                            if selected_unit_button and selected_skill:
                                unit = selected_unit_button.unit  # Ensure this references the selected unit

                                # Apply "Frenzy" skill effect
                                if selected_skill["name"] == "Frenzy":
                                    if not hasattr(unit, "frenzy") or not unit.frenzy:
                                        unit.basedmg = math.ceil(1.1 * unit.basedmg)
                                        unit.apdmg = math.ceil(1.1 * unit.apdmg)
                                        unit.chargebonus = math.ceil(1.1 * unit.chargebonus)
                                        unit.meleeatk = math.ceil(1.1 * unit.meleeatk)
                                        unit.frenzy = True
                                        unit.name += " (Frenzy)"
                                        unit.cost += 50
                                        print(f"Frenzy applied to {unit.name}")
                                    else:
                                        print(f"{unit.name} already has Frenzy!")

                                # Apply "Magic Shield" skill effect
                                elif selected_skill["name"] == "Magic Shield":
                                    if not hasattr(unit, "magicShield") or not unit.magicShield:
                                        unit.meleedef = math.ceil(1.1 * unit.meleedef)
                                        unit.magicShield = True
                                        unit.name += " (Magic Shield)"
                                        unit.cost += 50
                                        print(f"Magic Shield applied to {unit.name}")
                                    else:
                                        print(f"{unit.name} already has Magic Shield!")

                                # Add the skill to the unit's applied skills list
                                if not hasattr(unit, "applied_skills"):
                                    unit.applied_skills = []
                                if selected_skill["name"] not in unit.applied_skills:
                                    unit.applied_skills.append(selected_skill["name"])

                                # Deduct the cost of the skill from total money
                                if totalmoney >= selected_skill["cost"]:
                                    totalmoney -= selected_skill["cost"]
                                else:
                                    print("Not enough money!")

                                # Clear the selected skill after application
                                selected_skill = None

                        # Delete button
                        if delete_button.collidepoint(pos):
                            if selected_unit_button:
                                unit = selected_unit_button.unit

                                if hasattr(unit, "applied_skills") and unit.applied_skills:
                                    total_refund = 0
                                    for skill_name in unit.applied_skills:
                                        for skill in skills:
                                            if skill["name"] == skill_name:
                                                total_refund += skill["cost"]
                                    totalmoney += total_refund
                                    print(f"Refunded {total_refund} gold. Total money: {totalmoney}")

                                # Reset stats to their original values
                                unit.basedmg = unit.original_basedmg
                                unit.apdmg = unit.original_apdmg
                                unit.chargebonus = unit.original_charbonus
                                unit.meleeatk = unit.original_meleeatk
                                unit.meleedef = unit.original_meleedef
                                unit.cost = unit.original_cost

                                unit.magicShield = False
                                unit.frenzy = False

                                # Reset name to remove skill names
                                unit.name = unit.original_name

                                # Clear all applied skills
                                unit.applied_skills = []
                                if hasattr(unit, "frenzy"):
                                    del unit.frenzy
                                if hasattr(unit, "magicShield"):
                                    del unit.magicShield

                        # Start button
                        if start_button.collidepoint(pos):
                            # Transition to the next stage or logic
                            for unit_button in confirmed_buttons_list:
                                unit = unit_button.unit
                                final_units.append(unit)  # Append the unit object directly

                                # Print the final units for debugging
                            print("Final Units (Modified Data):")
                            for unit in final_units:
                                print(
                                    f"Name: {unit.name}, Cost: {unit.cost}, Base Damage: {unit.basedmg}, Melee Def: {unit.meleedef}")
                            confirmed_buttons_list.clear()
                            for i, unit in enumerate(final_units):
                                button = UnitButton(unit, 750, 420 + i * 40)
                                confirmed_buttons_list.append(button)
                            print(f"Current confirmed buttons: {[btn.unit.name for btn in confirmed_buttons_list]}")
                            page = "battle start"
                            # start_time = pygame.time.get_ticks()
                            # if pygame.time.get_ticks() - start_time > 2000:
                            #     page = "battle"

        elif page =="battle start":
            screen.fill(WHITE)
            battle_text = font_large.render("Battle Start!", TITLE_FONT, BLACK)
            continue_text = font_small.render("Click Anywhere To Continue", True, BLACK)
            # welcome_text = font_large.render("Welcome!", True, BLACK)
            screen.blit(battle_text, battle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            screen.blit(continue_text, continue_text.get_rect(center=(WIDTH // 2, 700)))
            pygame.display.flip()
            start_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # press anywhere to the battle page
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    page = "battle"





        # Battle page




        
        elif page == "battle":
            screen.fill(WHITE)
            render_text("Battle", font_large, BLACK, 550, 10)
        
            # Display user units
            user_unit_buttons = []
            for i, user_unit in enumerate(confirmed_units_list):
                if user_unit.remainhealth == 0:
                    continue
                user_rect = pygame.Rect(50 + i * 200, HEIGHT - 200, 150, 80)
                color = YELLOW if user_unit == selected_user_unit else BLUE
                pygame.draw.rect(screen, color, user_rect)
                health_bar_width = int(150 * (user_unit.remainhealth / user_unit.original_max_health))
                health_bar_rect = pygame.Rect(50 + i * 200, HEIGHT - 120, health_bar_width, 10)
                pygame.draw.rect(screen, GREEN, health_bar_rect)
                render_text(user_unit.name, font_small, BLACK, 55 + i * 200, HEIGHT - 190)
                user_unit_buttons.append((user_unit, user_rect))
        
            # Display enemy units
            enemy_unit_buttons = []
            for i, enemy_unit in enumerate(aiunits):
                if enemy_unit.remainhealth == 0:
                    continue
                enemy_rect = pygame.Rect(50 + i * 200, 100, 150, 80)
                color = YELLOW if enemy_unit == selected_enemy_unit else RED
                pygame.draw.rect(screen, color, enemy_rect)
                health_bar_width = int(150 * (enemy_unit.remainhealth / enemy_unit.original_max_health))
                health_bar_rect = pygame.Rect(50 + i * 200, 190, health_bar_width, 10)
                pygame.draw.rect(screen, GREEN, health_bar_rect)
                render_text(enemy_unit.name, font_small, BLACK, 55 + i * 200, 110)
                enemy_unit_buttons.append((enemy_unit, enemy_rect))
        
            # Display charge chances
            render_text(f"AI Charge Chance: {aichargechance}", font_medium, BLACK, WIDTH - 300, 20)
            render_text(f"User Charge Chance: {userchargechance}", font_medium, BLACK, WIDTH - 300, HEIGHT - 285)
        
            # Action Buttons
            charge_button = Button(WIDTH - 300, HEIGHT - 250, 120, 50, "Charge")
            attack_button = Button(WIDTH - 450, HEIGHT - 250, 120, 50, "Attack")
            charge_button.draw(screen, font_medium)
            attack_button.draw(screen, font_medium)
        
            # Battle Logs box
            pygame.draw.rect(screen, GREY, pygame.Rect(50, 300, WIDTH - 100, 200))
            render_text("Battle Logs", font_medium, BLACK, 60, 310)
            for i, log in enumerate(battle_logs[-6:]):
                render_text(log, font_small, BLACK, 60, 340 + i * 20)
        
            # Player Turn
            if turn == "user" and not fight_in_progress:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
        
                    elif event.type == pygame.MOUSEBUTTONDOWN and user_can_interact:
                        pos = event.pos
        
                        # User Turn Actions
                        for user_unit, rect in user_unit_buttons:
                            if rect.collidepoint(pos):
                                if selected_user_unit == user_unit:
                                    selected_user_unit = None
                                    battle_logs.append(f"Deselected {user_unit.name}")
                                else:
                                    selected_user_unit = user_unit
                                    battle_logs.append(f"Selected {user_unit.name}")
                                break
        
                        for enemy_unit, rect in enemy_unit_buttons:
                            if rect.collidepoint(pos):
                                if selected_enemy_unit == enemy_unit:
                                    selected_enemy_unit = None
                                    battle_logs.append(f"Deselected {enemy_unit.name}")
                                else:
                                    selected_enemy_unit = enemy_unit
                                    battle_logs.append(f"Selected {enemy_unit.name}")
                                break
        
                        if attack_button.is_clicked(pos) and selected_user_unit and selected_enemy_unit:
                            battle_logs.append(f"{selected_user_unit.name} attacked {selected_enemy_unit.name}")
                            user_can_interact = False  # Disable interactions
                            fight_thread = threading.Thread(target=fight, args=(selected_user_unit, selected_enemy_unit, False, False))
                            fight_thread.start()
                            selected_user_unit = None
                            selected_enemy_unit = None
                            turn = "ai_waiting"
        
                        elif charge_button.is_clicked(pos) and selected_user_unit and selected_enemy_unit and userchargechance > 0:
                            battle_logs.append(f"{selected_user_unit.name} charged {selected_enemy_unit.name}")
                            user_can_interact = False  # Disable interactions
                            userchargechance -= 1
                            fight_thread = threading.Thread(target=fight, args=(selected_user_unit, selected_enemy_unit, True, False))
                            fight_thread.start()
                            selected_user_unit = None
                            selected_enemy_unit = None
                            turn = "ai_waiting"
        
            elif turn == "ai_waiting" and not fight_in_progress:
                turn = "ai"
        
            # AI Turn
            elif turn == "ai" and not fight_in_progress:
                ai_unit = random.choice([unit for unit in aiunits if unit.remainhealth > 0])
                user_target = random.choice([unit for unit in confirmed_units_list if unit.remainhealth > 0])
        
                ai_action = "charge" if random.random() > 0.5 and aichargechance > 0 else "attack"
                if ai_action == "charge":
                    battle_logs.append(f"{ai_unit.name} charged {user_target.name}")
                    aichargechance -= 1
                    fight_thread = threading.Thread(target=fight, args=(ai_unit, user_target, True, False))
                else:
                    battle_logs.append(f"{ai_unit.name} attacked {user_target.name}")
                    fight_thread = threading.Thread(target=fight, args=(ai_unit, user_target, False, False))
        
                fight_thread.start()
                turn = "user"
                user_can_interact = True  # Re-enable interactions when it's the user's turn
        
            # Check Victory
            if not any(unit.remainhealth > 0 for unit in confirmed_units_list):
                aiwin = True
                page = "results"
        
            elif not any(unit.remainhealth > 0 for unit in aiunits):
                userwin = True
                page = "results"
        
            # Display Updates
            pygame.display.flip()
        
            # Handle real-time message_queue for battle logs
            while not message_queue.empty():
                msg = message_queue.get()
                battle_logs.append(msg)
            pygame.display.flip()
        ##################################################################################################################
        
        elif page == "results":
            screen.fill(WHITE)
            render_text("Game Over!", font_large, BLACK, WIDTH // 2 - 100, HEIGHT // 3)
            if aiwin:
                battle_logs.append("User has no remaining units! AI wins!")
            if userwin:
                battle_logs.append("AI has no remaining units! User wins!")
            render_text(f"{battle_logs[-1]}", font_medium, BLACK, WIDTH // 2 - 200, HEIGHT // 2)
            quit_button.draw(screen, font_small)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if quit_button.is_clicked(pos):
                        running = False
                        pygame.quit()
                        sys.exit()









        ##################################################################################################################


        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Press 'F' to toggle fullscreen
                    fullscreen = not fullscreen
                    toggle_window_size(fullscreen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if page == "welcome":
                    if start_button.is_clicked(event.pos):
                        print("Start button clicked")
                        page = "Prepare Your Units"
                    elif setting_button.is_clicked(event.pos):
                        page = "setting"
                    elif quit_button.is_clicked(event.pos):
                        running = False
                        pygame.quit()
                        sys.exit()
                elif page == "setting":
                    if reset_button.is_clicked(event.pos):
                        # Reset to preset 1
                        totalmoney = 3000
                        userchargechance = 1
                        aichargechance = 1
                        preset = "preset1"
                        totalmoney_input.set_value(str(totalmoney))
                        userchargechance_input.set_value(str(userchargechance))
                        aichargechance_input.set_value(str(aichargechance))
                    elif confirm_button.is_clicked(event.pos):
                        # Confirm settings and go back to welcome page
                        try:
                            totalmoney = int(totalmoney_input.get_value())
                            userchargechance = int(userchargechance_input.get_value())
                            aichargechance = int(aichargechance_input.get_value())
                        except ValueError:
                            pass  # Handle invalid input
                        page = "welcome"
                    elif preset1_button.is_clicked(event.pos):
                        preset = "preset1"
                        totalmoney = 3000
                        userchargechance = 1
                        aichargechance = 1
                        totalmoney_input.set_value(str(totalmoney))
                        userchargechance_input.set_value(str(userchargechance))
                        aichargechance_input.set_value(str(aichargechance))
                    elif preset2_button.is_clicked(event.pos):
                        preset = "preset2"
                        totalmoney = 10000
                        userchargechance = 5
                        aichargechance = 5
                        totalmoney_input.set_value(str(totalmoney))
                        userchargechance_input.set_value(str(userchargechance))
                        aichargechance_input.set_value(str(aichargechance))
                elif page == "Prepare Your Units":
                    pos = event.pos
                    # Handle unit selection
                    for unit in unit_buttons:
                        if unit.is_clicked(pos):
                            if unit.selected:
                                unit.selected = False
                                selected_unit_button = None
                            else:
                                for other_button in unit_buttons:
                                    other_button.selected = False
                                unit.selected = True
                                selected_unit_button = unit
                            break
                    for unit in confirmed_buttons:
                        if unit.is_clicked(pos):
                            if unit.selected:
                                unit.selected = False
                                selected_confirmed_button = None
                            else:
                                for other_button in confirmed_buttons:
                                    other_button.selected = False
                                unit.selected = True
                                selected_confirmed_button = unit
                            break
                    pygame.display.flip()
                    
                    if confirm_button.is_clicked(pos) and selected_unit_button:
                        recalculate_button_positions()
                        unit_base_name = selected_unit_button.unit.name
                        unit_cost = selected_unit_button.unit.cost
                    
                        if totalmoney >= unit_cost:
                            # Check if a suffix is needed
                            if unit_base_name in name_tracker:
                                suffix_list = name_tracker[unit_base_name]
                    
                                # Find the next available suffix
                                if not suffix_list:
                                    unique_name = unit_base_name  # First unit gets the base name
                                    suffix_list.append(0)  # Mark suffix 0 as used
                                else:
                                    suffix = max(suffix_list) + 1
                                    unique_name = f"{unit_base_name} {suffix}"
                                    suffix_list.append(suffix)  # Mark this suffix as used
                    
                            # Create a copy of the unit with the unique name
                            unit_copy = MeleeUnit(
                                unique_name,
                                selected_unit_button.unit.faction,
                                selected_unit_button.unit.unitsize,
                                unit_cost,
                                selected_unit_button.unit.health,
                                selected_unit_button.unit.meleeatk,
                                selected_unit_button.unit.meleedef,
                                selected_unit_button.unit.chargebonus,
                                selected_unit_button.unit.fireres,
                                selected_unit_button.unit.magres,
                                selected_unit_button.unit.misres,
                                selected_unit_button.unit.phyres,
                                selected_unit_button.unit.wardsave,
                                selected_unit_button.unit.basedmg,
                                selected_unit_button.unit.apdmg,
                                selected_unit_button.unit.meleecd,
                                selected_unit_button.unit.antiinfantry,
                                selected_unit_button.unit.antilarge,
                                selected_unit_button.unit.armor,
                                selected_unit_button.unit.magatk,
                                selected_unit_button.unit.fireatk,
                                selected_unit_button.unit.isinfantry,
                                selected_unit_button.unit.islarge
                            )
                            unit_copy.original_max_health = selected_unit_button.unit.original_max_health
                            unit_copy.damaged = selected_unit_button.unit.damaged
                            unit_copy.defeated = selected_unit_button.unit.defeated
                            unit_copy.frenzy = selected_unit_button.unit.frenzy
                            unit_copy.chargedefvsl = selected_unit_button.unit.chargedefvsl
                            unit_copy.crumbling = selected_unit_button.unit.crumbling
                            unit_copy.magicShield = selected_unit_button.unit.magicShield
                            # Update trackers and UI
                            confirmed_units_list.append(unit_copy)
                            new_button = UnitButton(unit_copy, 750, 420 + len(confirmed_buttons) * 40)
                            confirmed_buttons.append(new_button)
                    
                            # Deduct cost
                            totalmoney -= unit_cost


                    if delete_button.is_clicked(pos):
                        if selected_confirmed_button:
                            unit = selected_confirmed_button.unit
                            unit_name = unit.name
                            unit_base_name = unit.original_name
                            unit_cost = unit.cost
                    
                            # Find the matching unit by name
                            matching_unit = next((u for u in confirmed_units_list if u.name == unit_name), None)
                            if matching_unit:
                                # Remove this unit from the confirmed list and button list
                                confirmed_units_list.remove(matching_unit)
                                confirmed_buttons.remove(selected_confirmed_button)
                    
                                # Update name tracker for units with suffixes
                                if unit_name != unit_base_name:
                                    try:
                                        suffix = int(unit_name.split()[-1])  # Extract the numeric suffix
                                        name_tracker[unit_base_name].remove(suffix)
                                    except ValueError:
                                        print(f"Error parsing suffix for unit name: {unit_name}")
                                else:
                                    # Clear suffixes if the base unit is deleted
                                    name_tracker[unit_base_name] = []
                    
                                # Refund cost
                                totalmoney += unit_cost
                                recalculate_button_positions()
                            else:
                                print(f"Unit {unit_name} not found in confirmed units.")


                    if nextstep_button.is_clicked(event.pos):
                        for i, unit in enumerate(confirmed_units_list):
                            button = UnitButton(unit, 750, 420 + i * 40)
                            confirmed_buttons_list.append(button)
                        page = "next"
                        #TODO
            # Pass events to input boxes
            pygame.display.flip()
            totalmoney_input.handle_event(event)
            userchargechance_input.handle_event(event)
            aichargechance_input.handle_event(event)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# In[ ]:





