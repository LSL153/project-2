#!/usr/bin/env python
# coding: utf-8

# In[1]:


#note: 
# 1. charge defense vs large needed to be bracing, but you can still charge while bracing here for balancing, 
#     however, it only reduces more than half of the chargebonus now.
# 2. Also for balancing, Knights all got buffed because they lost the ability to maneuver and cycle charging.
# totalmoney = 10000
# userchargechance = 5
# aichargechance = 5


# In[2]:


import decimal
import random
import time
import threading
import copy
import math
from colorama import Fore, Back, Style
        
class MeleeUnit():
 
    # Class Variable
    category = 'Melee Unit'
    damaged = False
    defeated = False
    frenzy = False
    chargedefvsl =False
    crumbling = False
    def __init__(self,name, faction ,unitsize, cost, health, meleeatk, meleedef, chargebonus, 
                 fireres, magres, phyres, misres, wardsave, basedmg, apdmg, meleecd, 
                 antiinfantry, antilarge, armor, magatk, fireatk,isinfantry,islarge):
 
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
        self.isinfantry =isinfantry
        self.islarge =islarge
        self.original_max_health = health * unitsize


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

unitroster = [Greatswords,Halberdiers,Flagellants,Swordsman,SpearmanShields,SpearmanEMP,
              EmpireKnights,Reiksguard,DemigryphKnights,DemigryphKnightsHalberds,KnightsOfTheBlazingSun]


# In[3]:


SkeletonSpearmenTK = MeleeUnit("SkeletonSpearmen(Tomb Kings)","Tomb Kings", 160,350,53,14,30,3,0,0,0,0,0,18,6,4.5,0,14,20,False,False,True,False)
SkeletonSpearmenTK.chargedefvsl=True
SkeletonSpearmenTK.crumbling = True #14-28
unitroster.append(SkeletonSpearmenTK)
SkeletonWarriorsTK = MeleeUnit("Skeleton Warriors(Tomb Kings)","Tomb Kings", 160,325,53,18,22,5,0,0,0,0,0,20,6,4.3,0,0,20,False,False,True,False)
SkeletonWarriorsTK.crumbling = True
unitroster.append(SkeletonWarriorsTK)
NehekharaWarriors = MeleeUnit("Nehekhara Warriors","Tomb Kings", 120,525,68,32,22,15,0,0,0,0,0,26,7,4.5,0,0,45,False,False,True,False)
NehekharaWarriors.crumbling = True
unitroster.append(NehekharaWarriors)
TombGuard = MeleeUnit("Tomb Guard","Tomb Kings", 120,750,74,32,41,8,0,0,0,0,0,33,9,4.4,0,0,55,False,False,True,False)
TombGuard.crumbling = True
unitroster.append(TombGuard)
TombGuardHalberds = MeleeUnit("Tomb Guard(Halberds)","Tomb Kings", 120,850,74,25,47,5,0,0,0,0,0,9,20,4.9,0,19,55,False,False,True,False)
SkeletonSpearmenTK.chargedefvsl=True
TombGuardHalberds.crumbling = True
unitroster.append(TombGuardHalberds)

SkeletonHorsemen = MeleeUnit("Skeleton Horsemen","Tomb Kings", 60,400,73,24,26,34+40,0,0,0,0,0,21,7,4.5,0,0,30,False,False,False,True)
SkeletonHorsemen.crumbling = True
unitroster.append(SkeletonHorsemen)
NehekharaHorsemen = MeleeUnit("Nehekhara Horsemen","Tomb Kings", 60,650,98,28,34,26+32,0,0,0,0,0,28,10,5,0,0,50,False,False,False,True)
NehekharaHorsemen.crumbling = True
unitroster.append(NehekharaHorsemen)
NecropolisKnights = MeleeUnit("Necropolis Knights","Tomb Kings", 24,1425,295,40,43,52+56,0,0,0,0,0,21,40,5.4,0,0,110,False,False,False,True)
NecropolisKnights.crumbling = True
unitroster.append(NecropolisKnights)
NecropolisKnightsHalberds = MeleeUnit("Necropolis Knights(Halberds)","Tomb Kings", 24,1575,295,32,37,40+44,0,0,0,0,0,19,36,5.4,0,28+3,110,False,False,False,True)
NecropolisKnightsHalberds.crumbling = True
unitroster.append(NecropolisKnightsHalberds)


# In[4]:


def printunitdetail(unit: MeleeUnit):
    """
    Prints detailed information about a specific unit.
    
    Parameters:
        unit (MeleeUnit): The unit to display details for.
    
    Returns:
        None
    """
    print('unit details:')
    print('unit: ', unit.name)
    print('faction: ', unit.faction)
    print('size: ', unit.unitsize)
    print('cost: ', unit.cost)
    print('health: ', unit.totalhealth)
    print('melee attack: ', unit.meleeatk)
    print('melee defense: ', unit.meleedef)
    print('charge bonus: ', unit.chargebonus)
    print('fire resistance: ', unit.fireres)
    print('magic resistance: ', unit.magres)
    print('missle resistance: ', unit.misres)
    print('physical resistance: ', unit.phyres)
    print('ward save: ', unit.wardsave)
    print('base damage: ', unit.basedmg)
    print('armor-piercing damage: ', unit.apdmg)
    print('melee interval: ', unit.meleecd)
    print('anti-infantry value: ', unit.antiinfantry)
    print('anti-large value: ', unit.antilarge)
    print('armor: ', unit.armor)
    print('have magic attak: ', unit.magatk)
    print('have fire attack: ', unit.fireatk)
    print('is infantry: ', unit.isinfantry)
    print('is large: ', unit.islarge)
    print('category: ',unit.category)
    print('skill info: ')
#     print('frenzy: ',unit.skills.frenzy)
    print('frenzy: ',unit.frenzy)
    print('charge defense vs large: ',unit.chargedefvsl)
    print('\n')    


# In[5]:


def printfactionunits():
    """
    Displays all units available in the current faction.
    
    Parameters:
        None
    
    Returns:
        None
    """
    global factionname
    factionname=str(input("Enter the faction you want to look at, type \"exit\" to exit: "))
    for factions in unitroster:
        if(factions.faction==factionname):
            printunitdetail(factions)


# In[6]:


def buyfrenzy(unit1: MeleeUnit):
    """
    Adds the frenzy ability to a unit if eligible.
    
    Parameters:
        unit1 (MeleeUnit): The unit to which the frenzy ability will be added.
    
    Returns:
        bool: True if frenzy was successfully added, False otherwise.
    """
    if(unit1.frenzy==True):
        print("You already have frenzy, can't add again.")
    else:
        tempbdmg = unit1.basedmg
        tempapdmg = unit1.apdmg
        tempcb = unit1.chargebonus
        tempmatk = unit1.meleeatk
        tempname = unit1.name
        tempcost = unit1.cost
        addfrenzy(unit1)
        unit1.cost += 50
        unit1.name += " Frenzy"
        print(f"{tempname} becomes {unit1.name}, its cost {tempcost} becomes {unit1.cost},base damage {tempbdmg} becomes {unit1.basedmg},"
              f"ap damage {tempapdmg} becomes {unit1.apdmg},charge bonus {tempcb} becomes {unit1.chargebonus},"
              f"melee atk {tempmatk} becomes {unit1.meleeatk}, all +10%")


# In[7]:


def addfrenzy(unit1: MeleeUnit):
    """
    Applies the effects of the frenzy ability to a unit.
    
    Parameters:
        unit1 (MeleeUnit): The unit to modify with frenzy effects.
    
    Returns:
        None
    """
    unit1.basedmg = math.ceil(1.1*(unit1.basedmg))
    unit1.apdmg = math.ceil(1.1*(unit1.apdmg))
    unit1.chargebonus = math.ceil(1.1*(unit1.chargebonus))
    unit1.meleeatk = math.ceil(1.1*(unit1.meleeatk))
    unit1.frenzy = True


addfrenzy(Flagellants)


# In[8]:


def dmgtoarmor(bdmg: int, armor: int,usize: int) -> int:
    """
    Calculates the effective damage to a unit after accounting for its armor.
    
    Parameters:
        bdmg (float): The base damage dealt.
        armor (int): The armor value of the target unit.
        usize (int): How many entities are left in this unit.
    
    Returns:
        int: The effective damage after armor reduction.
    """
    armordmg = armor * random.uniform(0.5, 1)
    if(armordmg>100):
        armordmg=100
#     print(armordmg)
    actualdmg = int(usize * (bdmg * ((100-armordmg)/100)))
#     print((100-armordmg)/100,bdmg * ((100-armordmg)/100),usize * (bdmg * ((100-armordmg)/100)))
    return actualdmg


# In[9]:


def totaldmghit(attacker: MeleeUnit, defender: MeleeUnit,chargeland: bool)->int:
    """
    Computes the total damage dealt during a single attack.
    
    Parameters:
        attacker (MeleeUnit): The unit initiating the attack.
        defender (MeleeUnit): The unit being attacked.
        cchargeland (bool): Indicates if a charge landed during the attack.
    
    Returns:
        int: The total damage inflicted on the defender.
    """
    hitlandnum = numhitland(attacker, defender, chargeland)
    if(chargeland==False):
        if(defender.isinfantry and attacker.antiinfantry!=0):
            totalweaponstr = attacker.basedmg + attacker.apdmg + attacker.antiinfantry
            newbasedmg = totalweaponstr * (attacker.basedmg/(attacker.basedmg + attacker.apdmg))
            newapdmg = totalweaponstr * (attacker.apdmg/(attacker.basedmg + attacker.apdmg))
            totaldmg = dmgtoarmor(newbasedmg, defender.armor,hitlandnum) + newapdmg*hitlandnum
#             print('fanbu no charge')
        elif(defender.islarge and attacker.antilarge!=0):
            totalweaponstr = attacker.basedmg + attacker.apdmg + attacker.antilarge
            newbasedmg = totalweaponstr * (attacker.basedmg/(attacker.basedmg + attacker.apdmg))
            newapdmg = totalweaponstr * (attacker.apdmg/(attacker.basedmg + attacker.apdmg))
            totaldmg = dmgtoarmor(newbasedmg, defender.armor,hitlandnum) + newapdmg*hitlandnum
#             print('fanda no charge')
        else:
            totaldmg = dmgtoarmor(attacker.basedmg, defender.armor,hitlandnum) + attacker.apdmg*hitlandnum
#             print('no charge')
    else:
        if(defender.chargedefvsl and attacker.islarge):
            newcb = math.ceil(attacker.chargebonus*0.4)
        else:
            newcb = attacker.chargebonus
        totalchargeweaponstr = attacker.basedmg + attacker.apdmg + newcb
        newbasedmg = totalchargeweaponstr * (attacker.basedmg/(attacker.basedmg + attacker.apdmg))
        newapdmg = totalchargeweaponstr * (attacker.apdmg/(attacker.basedmg + attacker.apdmg))
        if(defender.isinfantry and attacker.antiinfantry!=0):
            totalweaponstr = newbasedmg + newapdmg + attacker.antiinfantry
            newbasedmg = totalweaponstr * (attacker.basedmg/(attacker.basedmg + attacker.apdmg))
            newapdmg = totalweaponstr * (attacker.apdmg/(attacker.basedmg + attacker.apdmg))
            totaldmg = dmgtoarmor(newbasedmg, defender.armor,hitlandnum) + newapdmg*hitlandnum
#             print('fanbu charge')
        elif(defender.islarge and attacker.antilarge!=0):
            totalweaponstr = newbasedmg + newapdmg + attacker.antilarge
            newbasedmg = totalweaponstr * (attacker.basedmg/(attacker.basedmg + attacker.apdmg))
            newapdmg = totalweaponstr * (attacker.apdmg/(attacker.basedmg + attacker.apdmg))
            totaldmg = dmgtoarmor(newbasedmg, defender.armor,hitlandnum) + newapdmg*hitlandnum
#             print('fanda charge')
        else:
            totaldmg = dmgtoarmor(newbasedmg, defender.armor,hitlandnum) + newapdmg*hitlandnum
#             print('charge')
    jianshang = 0
    if(attacker.magatk==False and defender.phyres !=0):
        jianshang += defender.phyres
#         print('+wukang',jianshang)
    if(attacker.magatk and defender.magres !=0):
        jianshang += defender.magres
#         print('+fakang',jianshang)
    if(attacker.fireatk and defender.fireres !=0):
        jianshang += defender.fireres
#         print('+huokang',jianshang)
    if(defender.wardsave !=0):
        jianshang += defender.wardsave
#         print('+tebao',jianshang)
    if(jianshang>90):
        jianshang=90
    jianshang = (100-jianshang)/100
#     print(jianshang)
    totaldmg = jianshang*totaldmg
    return int(totaldmg)


# In[10]:


def numhitland(attacker: MeleeUnit, defender: MeleeUnit, chargeland: bool)->int:
    """
    Determines the number of hits landed by the attacker on the defender.
    
    Parameters:
        attacker (MeleeUnit): The unit attacking.
        defender (MeleeUnit): The unit defending.
        chargeland (bool): Indicates if a charge landed during the attack.
    
    Returns:
        int: The number of successful hits landed.
    """
    if(chargeland==False):
        matk = attacker.meleeatk
#         print(f"no charge, matk = {matk}")
    elif(defender.chargedefvsl and attacker.islarge):
        matk = attacker.meleeatk + math.ceil(attacker.chargebonus*0.4)
#         print(f"chargeland,but chargedef, matk = {matk}")
    else:
        matk = attacker.meleeatk + attacker.chargebonus
#         print(f"chargeland, matk = {matk}")
    chancetohit = ((35+(matk-defender.meleedef))/100)
#     print(chancetohit)
    if(chancetohit<0.08):
        chancetohit=0.08
    elif(chancetohit>0.9):
        chancetohit=0.9
#     print(chancetohit)
    numpplhit=0
    maxpplhit = math.ceil(attacker.unitsize/2)
    if(attacker.unitsize<30):
        maxpplhit = attacker.unitsize
    for i in range (0,maxpplhit,1):
        hitornot = random.choices([1,0], weights=(chancetohit, 1-chancetohit), k=1)
        if(hitornot[0]==1):
            numpplhit+=1
#         print(numpplhit)
#     print(hitornot)
    return numpplhit


# In[11]:


def crumblingdmg(unit2: MeleeUnit,unit1: MeleeUnit):
    """
    Calculates the damage taken by a unit due to crumbling effects.
    
    Parameters:
        unit2 (MeleeUnit): The unit affected by crumbling.
        unit1 (MeleeUnit): The unit causing the crumbling effect.
    
    Returns:
        float: The damage taken due to crumbling.
    """
    if(unit2.remainhealth>0 and unit1.remainhealth>0):
        dmgdealt = int(random.uniform(14, 28))
        unit2.remainhealth -= dmgdealt
        if(unit2.remainhealth<0):
            unit2.remainhealth=0
        print(f"{unit2.name} is crumbling, it took {dmgdealt} damage, its remain health is {unit2.remainhealth}.")
        threading.Timer(1,crumblingdmg,[unit2,unit1],).start()


# In[12]:


def attack(unit1: MeleeUnit, unit2: MeleeUnit,chargeland: bool):
    """
    Simulates an attack from one unit to another.
    
    Parameters:
        unit1 (MeleeUnit): The attacking unit.
        unit2 (MeleeUnit): The defending unit.
        chargeland (bool): Indicates if a charge landed during the attack.
    
    Returns:
        dict: A summary of the attack, including damage dealt and hits landed.
    """
    starttime = time.time()
    currenttime = starttime
    countu2 = 1
    countu1 = 1
    while (unit1.remainhealth>0 and unit2.remainhealth>0):
        currenttime = round(time.time()-starttime,2)
        if(unit2.crumbling):
            if(unit2.remainhealth <= unit2.totalhealth/2 and countu2 ==1):
                crumblingdmg(unit2,unit1)
                countu2 += 1
        if(unit1.crumbling):
            if(unit1.remainhealth <= unit1.totalhealth/2 and countu1 ==1):
                crumblingdmg(unit1,unit2)
                countu1 += 1
        if(chargeland and currenttime<= 15):
            dmgdealt = totaldmghit(unit1, unit2,1)
            unit2.remainhealth -= dmgdealt
            if(unit2.remainhealth<0):
                unit2.remainhealth=0
            print(f"At time {currenttime}s, {unit1.name} did a charge attack on {unit2.name} with {dmgdealt} damage,"
                  f" {unit2.name} remain health is {unit2.remainhealth}.\n")
            if(unit2.chargedefvsl and unit1.islarge):
                print("But charge defense vs large triggered, charge bouns from large unit got reduced.")
            if(unit2.remainhealth==0):
                break
            time.sleep(unit1.meleecd - ((time.time() - starttime) % unit1.meleecd))
        else:
            dmgdealt = totaldmghit(unit1, unit2,0)
            unit2.remainhealth -= dmgdealt
            if(unit2.remainhealth<0):
                unit2.remainhealth=0
            print(f"At time {currenttime}s, {unit1.name} did an attack on {unit2.name} with {dmgdealt} damage,"
                  f" {unit2.name} remain health is {unit2.remainhealth}.\n")
            if(unit2.remainhealth==0):
                break
            time.sleep(unit1.meleecd - ((time.time() - starttime) % unit1.meleecd))


# In[13]:


def defeatcheck(unit1):
    """
    Checks if a unit has been defeated.
    
    Parameters:
        unit1 (MeleeUnit): The unit to check for defeat.
    
    Returns:
        bool: True if the unit is defeated, False otherwise.
    """
    if(unit1.remainhealth==0):
        unit1.totalhealth = 0
        unit1.name+=" defeated"
        unit1.defeated = True
    return unit1.defeated


# In[14]:


def fight(unit1: MeleeUnit, unit2: MeleeUnit,achargeb: bool, bchargea: bool) -> MeleeUnit:
    """
    Executes a fight between two units, potentially with charging effects.
    
    Parameters:
        unit1 (MeleeUnit): The first unit participating in the fight.
        unit2 (MeleeUnit): The second unit participating in the fight.
        achargeb (bool): Indicates if the first unit successfully charged the second.
        bchargea (bool): Indicates if the second unit successfully charged the first.
    
    Returns:
        None
    """
    p1 = threading.Thread(target = attack,args=(unit1,unit2,achargeb))
    p2 = threading.Thread(target = attack,args=(unit2,unit1,bchargea))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    if(defeatcheck(unit1)):
        print(f"{unit2.name} wins!")
        unit2.totalhealth = unit2.remainhealth
        unit2.unitsize = math.ceil(unit2.totalhealth/unit2.health)
        print(f"{unit2.name} still have {unit2.totalhealth} health and {unit2.unitsize} entities")
        unit2.damaged = True
    if(defeatcheck(unit2)):
        print(f"{unit1.name} wins!")
        unit1.totalhealth = unit1.remainhealth
        unit1.unitsize = math.ceil(unit1.totalhealth/unit1.health)
        print(f"{unit1.name} still have {unit1.totalhealth} health and {unit1.unitsize} entities")
        unit1.damaged =True


# In[15]:


def briefdetail():
    """
    Prints a brief summary of all units in the roster.
    
    Parameters:
        None
    
    Returns:
        None
    """
    for units in unitroster:
        print(units.name,end=' ')
        print(f"${units.cost}",end='')
        if(units.isinfantry):
            print(" {infantry}",end='')
        if(units.islarge):
            print(" {large}",end='')
        if(units.antiinfantry!=0):
            print(" [anti-infantry]",end='')
        if(units.antilarge!=0):
            print(" [anti-large]",end='')
        if(units.magatk):
            print(" *magic attack*",end='')
        if(units.fireatk):
            print(" *fire attack*",end='')
        if(units.frenzy):
            print(" |Frenzy|",end='')
        if(units.chargedefvsl):
            print(" |Charge defense vs. large|",end='')
        print()


# In[16]:


def checkrepeat(chosenroster):
    """
    Checks for duplicate units in the chosen roster.
    
    Parameters:
        chosenroster (list): The roster of units to check.
    
    Returns:
        bool: True if duplicates are found, False otherwise.
    """
    num =1
    for i in range(len(chosenroster)-1,-1,-1):
            for j in range(i):
                if(chosenroster[j].name==chosenroster[i].name and i!=j):
                    chosenroster[j].name = chosenroster[j].name + " " + str(num)
                    num+=1      


# In[17]:


def aichooseunit():
    """
    Make ai randomly pick their unit.
    
    Parameters:
        None
    
    Returns:
        None
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
        


# In[18]:


def sortandprint(sortroster):
    """
    Sorts a roster of units by their name and prints their details.

    Parameters:
        sortroster (list of MeleeUnit): The roster of units to be sorted and displayed.
    
    Returns:
        None
    """
    sortroster = sorted(sortroster, key=lambda x: x.name)
    for units in sortroster:
        if(units.damaged):
            print(f"{units.name}, health {units.remainhealth}, is damaged.")
        else:
            print(f"{units.name}, health {units.remainhealth}.")
    print("\n")


# In[19]:


def doyouhavetheunit(unitaddskill)->bool:
    """
    Checks if the user has a specific unit.

    Parameters:
        unitaddskill (str): Name of the unit to check.
    
    Returns:
        havethisunit (bool): True if the unit is found, False otherwise.
    """
    global userChosen
    global addskillunit
    havethisunit = False
    for unit in userChosen:
        if(unitaddskill==unit.name):
            havethisunit = True
            addskillunit = unit
    return havethisunit


# In[20]:


def isaliveunit(unitget)->bool:
    """
    Checks if a unit is alive.

    Parameters:
        unitget (str): Name of the unit to check.
    
    Returns:
        unitisvalid (bool): True if the unit is alive (health is not 0), False otherwise.
    """
    global userChosen
    global unitisalive
    unitisvalid = False
    for unit in userChosen:
        if(unitget==unit.name and unit.remainhealth!=0):
            unitisvalid = True
            unitisalive = unit
    return unitisvalid


# In[21]:


def istargetalive(targetget)->bool:
    """
    Checks if a target is alive.

    Parameters:
        targetget (str): Name of the target to check.
    
    Returns:
        targetisvalid (bool): True if the target is alive (health is not 0), False otherwise.
    """
    global aiunits
    global targetisalive
    targetisvalid = False
    for unit in aiunits:
        if(targetget==unit.name and unit.remainhealth!=0):
            targetisvalid = True
            targetisalive = unit
    return targetisvalid


# In[22]:


def aichooseunit2(units)-> int:
    """
    Randomly selects a unit that is still alive.

    Parameters:
        units (list): List of units to choose from.
    
    Returns:
        numairand (int): Index of the selected unit.
    """
    while True:
        numairand = int(random.uniform(0, len(units)))
        if(units[numairand].remainhealth!=0):
            if(numairand==len(units)):
                numairand-=1
            break
            
    return numairand


# In[23]:


def checkifdefeated():
    """
    Checks if the AI or the user has been defeated by counting their defeated units.

    Returns:
        None
    """
    global userChosen
    global aiunits
    defeadnumai = 0
    defeatednumuser = 0
    global aiisdefeated
    global userisdefeated
    aiisdefeated =False
    userisdefeated = False
    for unit in aiunits:
        if(unit.defeated):
            defeadnumai+=1
    if(defeadnumai==len(aiunits)):
        aiisdefeated=True
        
    for unit in userChosen:
        if(unit.defeated):
            defeatednumuser+=1
    if(defeatednumuser==len(userChosen)):
        userisdefeated=True
        


# In[24]:


def calculateallhealth(roster)->int:
    """
    Calculates the total health of all units in a roster.

    Parameters:
        roster (list): List of units to calculate health for.
    
    Returns:
        allhealth (int): Total health of all units in the roster.
    """
    allhealth=0
    for unit in roster:
        allhealth += unit.totalhealth
    return allhealth


# In[25]:


def victoryconditioncheckai(roster):
    """
    Checks the AI's victory condition based on remaining health percentage.

    Parameters:
        roster (list): List of AI units to evaluate.
    
    Returns:
        None
    """
    global aiallhealth
    totalhealthleft = 0
    for unit in roster:
        totalhealthleft += unit.remainhealth
    if(totalhealthleft/aiallhealth <= 0.25):
        print("\nWhat a pity, all of your units are defeated.\nValiant Defeat!")
    if(0.25 < totalhealthleft/aiallhealth <= 0.50):
        print("\nWhat a pity, all of your units are defeated.\nClose Defeat!")
    if(0.50 < totalhealthleft/aiallhealth <= 0.75):
        print("\nWhat a pity, all of your units are defeated.\nDecesive Defeat!")
    if(0.75 < totalhealthleft/aiallhealth <= 1):
        print("\nWhat a pity, all of your units are defeated.\nCrushing Defeat!")   


# In[26]:


def victoryconditioncheckuser(roster):
    """
    Checks the user's victory condition based on remaining health percentage.

    Parameters:
        roster (list): List of user's units to evaluate.
    
    Returns:
        None
    """
    global userallhealth
    totalhealthleft = 0
    for unit in roster:
        totalhealthleft += unit.remainhealth 
    if(totalhealthleft/userallhealth <= 0.25):
        print("\n Congratulations, all of AI's units are defeated!\nPyrrhic Vcitory!")
    if(0.25 < totalhealthleft/userallhealth <= 0.50):
        print("\n Congratulations, all of AI's units are defeated!\nClose Vcitory!")
    if(0.50 < totalhealthleft/userallhealth <= 0.75):
        print("\n Congratulations, all of AI's units are defeated!\nDecesive Vcitory!")
    if(0.75 < totalhealthleft/userallhealth <= 1):
        print("\n Congratulations, all of AI's units are defeated!\nHeroic Vcitory!")


# In[27]:


def settings():
    """
    Configures game settings, including presets, total money, and charge chances.

    Allows the user to choose between predefined presets or manually set the 
    total money, user's charge chances, and AI's charge chances.

    Returns:
        None
    """
    global totalmoney
    global userchargechance
    global aichargechance
    usepreset("preset2")
    settings="no"
    while (settings!="exit"):
        settings=input("Enter \"Yes\" if you want to change settings, or \"exit\" if you don't:")
        if(settings=="Yes" or settings=="yes"):
            while True:
                print("preset 1 is the quick game mode, where the maxium money can be spent on units is 3000, and only 1 charge chance.")
                print("preset 2 is the normal or long game mode, where the maxium money can be spent on units is 10000, and 5 charge chance.")
                presetnum=input("Enter \"preset1\" or \"preset2\" if you want ot use preset, or \"exit\" if you don't:")
                if(presetnum=="exit"):
                    break
                if(presetnum=="preset1"):
                    usepreset(presetnum)
                    print("preset 1 is applied.")
                    break
                if(presetnum=="preset2"):
                    usepreset(presetnum)
                    print("preset 2 is applied.")
                    break
            if(presetnum=="preset1" or presetnum=="preset2"):
                break
            while True:
                money=input("Enter total number of money you want to have, or \"exit\":")
                if(money=="exit"):
                    break
                if(money.isnumeric()):
                    totalmoney = int(money)
                    break
            while True:
                usercc=input("Enter number of charge you want to have, or \"exit\":")
                if(usercc=="exit"):
                    break
                if(usercc.isnumeric()):
                    userchargechance = int(usercc)
                    break
            while True:
                aicc=input("Enter number of charge you want ai to have, or \"exit\":")
                if(aicc=="exit"):
                    break
                if(aicc.isnumeric()):
                    aichargechance = int(aicc)
                    break
                    


# In[28]:


def play():
    """
    Executes the main game loop, allowing the user and AI to select units, configure 
    their skills, and engage in a turn-based battle.

    Features:
    - Unit selection and customization with skill additions.
    - Turn-based attacks between user and AI.
    - Victory and defeat conditions based on remaining unit health.
    - Real-time decision-making for charging during attacks.

    Returns:
        None
    """
    print("Welcome to Estalia, gentlemen!")
    global totalmoney
#     totalmoney = 10000
    print(f"You have ${totalmoney}, please choose your units wisely.\n")
    needetail1=input("Enter \"Yes\" if you want to see units information")
    if(needetail1=="Yes" or needetail1=="yes"):
        print("Here is the brief detail of all units:\n")
        briefdetail()
    needetail=input("Enter \"Yes\" if you want to see detail information")
    global factionname
    global userChosen
    global aiunits
    userChosen = []
    moneyleft = totalmoney
    while(needetail=="Yes" or needetail=="yes"):
        printfactionunits()
        if(factionname=="exit"):
            break
    print(Fore.RED + "\nNow you can choose your unit, but remember to save some "
          "money if you want to add skills to them, skills costs $50 each.")
    print(Style.RESET_ALL)
    while True:
        unitchoosed=input("Enter the name of unit to select the Unit that you want to choose, type \"exit\" to exit:")
        nosuchunit=True
        if(unitchoosed=="exit"):
            break
        for units in unitroster:
            if(unitchoosed==units.name and moneyleft<units.cost):
                print(Fore.YELLOW + "Not enough minerals. You have not enough minerals. Not enough minerals.")
                print(Style.RESET_ALL)
                nosuchunit = False
            if(unitchoosed==units.name and moneyleft>=units.cost):
                moneyleft -= units.cost
                newunit = copy.copy(units)
                userChosen.append(newunit)
                print(f"You choosed {units.name}, it costs {units.cost}, you still have ${moneyleft}")
                nosuchunit = False
        if(nosuchunit):
            print("There is no unit match this name, please match its actual id.")
    
    checkrepeat(userChosen)
    print("\nThese are the units you choosed:\n")
    sortandprint(userChosen)
    addskill=input("Enter \"Yes\" if you wish to add skills:")
    if(addskill=="Yes" or addskill=="yes"):
        global addskillunit
        while True:
            unitaddskill=input("Enter the name of unit you want to add skill to, type \"exit\" to exit:")
            if(unitaddskill=="exit"):
                break
            while (doyouhavetheunit(unitaddskill)):
                skilladding=input("Enter the name of skill you want to add, type \"exit\" to exit:")
                if(skilladding=="exit"):
                    break
                if(moneyleft<50):
                    print(Fore.YELLOW + "Not enough minerals. You have not enough minerals. Not enough minerals.")
                    print(Style.RESET_ALL)
                    break
                if(skilladding=="Frenzy" or skilladding == "frenzy"):
                    buyfrenzy(addskillunit)
                    moneyleft-=50
                    print(f"You still have ${moneyleft} left")
                
    aichooseunit()
    checkrepeat(aiunits)
    print("\nHere are the units chosen by the ai:\n")
    sortandprint(aiunits)
    global aiallhealth
    aiallhealth = calculateallhealth(aiunits)
    global userallhealth
    userallhealth = calculateallhealth(userChosen)
    
    global userchargechance
    global aichargechance
#     userchargechance = 5
#     aichargechance = 5

    global unitisalive
    global targetisalive
    global aiisdefeated
    global userisdefeated
    aiisdefeated = False
    userisdefeated = False
    
    print("Please wait about 5s, and we will show your units in blue and enemy units in red.")
    time.sleep(5)
    while True:
        battleresult=0
        checkifdefeated()
        if(aiisdefeated):
            victoryconditioncheckuser(userChosen)
            break
        if(userisdefeated):
            victoryconditioncheckai(aiunits)
            break
        usercharged = 0
        aichargeback = 0
        aicharge2 = 0
        usercharge2 = 0
        print(Fore.CYAN)
        sortandprint(userChosen)
        print(Style.RESET_ALL)
        print(Fore.RED)
        sortandprint(aiunits)
        print(Style.RESET_ALL)
        while True:
            validunit=input("It's your turn, select your unit that you want to launch the attack: ")
            if(isaliveunit(validunit)):
                break
        targetunit=input("Select the enemy unit you want to attck: ")
        while(istargetalive(targetunit)==False):
            targetunit=input("Not valid target, reselect the enemy unit you want to attck: ")

        aichargeguess = random.choices([0,1], weights=(0.65, 0.35), k=1)
        aichargeback = aichargeguess[0]
        if(aichargeback==0 or aichargechance<=0):
            aichargeback = 0
            print("AI didn't choose to charge back.")
        if(aichargeback==1):
            aichargechance -=1
            print("AI choosed to charge back.")

        while True:
            userchargecheck=input(f"You have {userchargechance} chances of charge left,"
                              " do use want to charge the enemy this time? (Enter yes or no)")
            if(userchargecheck=="yes" and userchargechance>0):
                userchargechance-=1
                usercharged =1
                fight(unitisalive,targetisalive,usercharged,aichargeback)
                break
            if(userchargecheck=="no"):
                usercharged =0
                fight(unitisalive,targetisalive,usercharged,aichargeback)
                break
        
        checkifdefeated()
        if(aiisdefeated):
            victoryconditioncheckuser(userChosen)
            break
        if(userisdefeated):
            victoryconditioncheckai(aiunits)
            break
        
        print("It's AI's turn now.")
        aichargeguess2 = random.choices([0,1], weights=(0.65, 0.35), k=1)
        aicharge2 = aichargeguess2[0]
        if(aichargechance<=0):
            aicharge2=0
        if(aicharge2==1):
            aichargechance-=1
        aiattackernum = aichooseunit2(aiunits)
        aitargetnum = aichooseunit2(userChosen)
        while True:
            userchargecheck = input(f"AI use {aiunits[aiattackernum].name} to attack {userChosen[aitargetnum].name},"
                                    f" you still have {userchargechance} charge chances left,do you want to charge back? (yes or no)")
            if(userchargecheck=="yes" and userchargechance>0):
                userchargechance-=1
                usercharge2 =1
                fight(aiunits[aiattackernum],userChosen[aitargetnum],aicharge2,usercharge2)
                break
            if(userchargecheck=="no"):
                usercharge2 =0
                fight(aiunits[aiattackernum],userChosen[aitargetnum],aicharge2,usercharge2)
                break
            
            


# In[29]:


def usepreset(presetname):
    """
    Applies a preset configuration for the game, setting total money and charge chances.

    Parameters:
        presetname (str): The name of the preset to apply ("preset1" or "preset2").
    
    Returns:
        None
    """
    global totalmoney
    global userchargechance
    global aichargechance
    if(presetname=="preset1"):
        totalmoney =3000
        userchargechance =1
        aichargechance=1
    if(presetname=="preset2"):
        totalmoney =10000
        userchargechance =5
        aichargechance=5

