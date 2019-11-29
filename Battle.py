import pygame
from collections import deque
from random import randint
from Player import *
from Enemy import *
from Tree import *
from Animatable import *
from enemyStatusBar import *
from Attack import *
from enemy_attack import *
from textWrapper import *
from TreeManager import *

class Battle(pygame.sprite.Sprite):

    def __init__(self, game, player, enemy, x, y):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        
        self.game = game

        self.player = player

        self.enemy = enemy

        self.image = pygame.image.load("img/misc/battle_screen.png").convert_alpha()

        self.bg = pygame.image.load("img/misc/battle_screen.png").convert_alpha()

        self.x = x

        self.y = x

        self.rect = self.image.get_rect()

        self.rect.x = x

        self.rect.y = y

        self.player_clock = Animatable(355, 150, self.game, "Clock", 998, False, "img/battle/game_clock.png", "img/battle/game_clock_spritesheet.png", 12, 1, 0, "img/misc/battle_screen.png", True, None)

        #self.image.blit(self.clock.image, (self.clock.x, self.clock.y))

        self.player_clock.add(self.game.clock_group)

        self.enemy_clock = Animatable(0, 150, self.game, "Clock", 998, False, "img/battle/game_clock.png", "img/battle/game_clock_spritesheet.png", 12, 1, 0, "img/misc/battle_screen.png", True, None)

        

        self.enemy_clock.add(self.game.clock_group)

        self.enemy_status_bar = enemyStatusBar(self.game, self.enemy, 0, 0)

        self.enemy_status_bar.add(self.game.active_enemy_status_bar)

        self.player_turn_length = 0

        self.enemy_turn_length = 0 #these variables describe seconds since turn began

        self.turn_count = 1 #describes whose turn it is

        self.turn_indicator("Horace")


        self.combos = []

        
        
        self.keystrokesX = 14 #14 

        self.keystrokesY = 213 #63 + 150
        

        self.game_clock = pygame.time.Clock()

        self.moveset_tree = TreeManager(self.player)

        self.moveset_tree.horace_turn()

        self.displayCurrentMoves()

        self.KEYRIGHT = pygame.image.load("img/battle/right_arrow_key.png").convert_alpha()

        self.KEYRIGHT_TRANSITION = "img/battle/right_arrow_key_transition.png"

        self.KEYLEFT = pygame.image.load("img/battle/left_arrow_key.png").convert_alpha()

        self.KEYLEFT_TRANSITION = "img/battle/left_arrow_key_transition.png"

        self.KEYUP = pygame.image.load("img/battle/up_arrow_key.png").convert_alpha()

        self.KEYUP_TRANSITION = "img/battle/up_arrow_key_transition.png"

        self.KEYDOWN = pygame.image.load("img/battle/down_arrow_key.png").convert_alpha()

        self.KEYDOWN_TRANSITION = "img/battle/down_arrow_key_transition.png"

        self.keystrokes_background = "img/battle/keystrokes_bg.png"

        self.attack_background = "img/battle/attack_bg.png"

        self.displayed_keystrokes = []

        self.displayCurrentKeyCombos()

        self.enemy_idle_anim = Animatable(80, 325, self.game, "Enemy idle animation", 69, False, self.enemy.idle_background, self.enemy.idleAnim, 9, 1, None, self.enemy.idle_background, True, None)     

        self.enemy_hurt_anim = Animatable(80, 325, self.game, "Enemy hurt animation", 70, False, self.enemy.hurt_background, self.enemy.hurtAnim, 5, 1, None, self.enemy.hurt_background, True, None)
    
        self.enemy_idle_anim.add(self.game.clock_group)

        #self.enemy_attack_clock = Animatable(257, 225, self.game, "Enemy attack clock", 73, False, "img/battle/attack_clock_bg.png", "img/battle/attack_clock.png", 32, 1, None, "img/battle/attack_clock_bg.png", True, None)

        self.isIdling = True

        self.isAttacking = False

        self.isHurt = False

        self.successfulAttack = False

        self.unsuccessfulAttack = False

        self.currentAnimation = Animatable(80, 325, self.game, "Enemy idle animation", 69, False, self.enemy.idle_background, self.enemy.idleAnim, 9, 1, None, self.enemy.idle_background, True, None)

        self.currentAnimation.add(self.game.clock_group)

        self.secondaryCurrentAnimation = None

        self.pendingAttack = None

        self.battleLogX = 440

        self.battleLogY = 328
        

        #self.slash_effect = Animatable(0, 0, self.game, "Slash effect", 70, False

    

    def chooseAnimation(self, mode, effectX, effectY):
        if mode == "idling":
            self.currentAnimation = Animatable(80, 325, self.game, "Enemy idle animation", 69, False, self.enemy.idle_background, self.enemy.idleAnim, 9, 1, None, self.enemy.idle_background, True, None) 
            self.currentAnimation.add(self.game.clock_group)
        elif mode == "hurt":
            self.currentAnimation = Prop(80, 325, "Enemy hurt prop", 76, False, self.enemy.hurt_background)
            self.currentAnimation.add(self.game.clock_group)
            self.secondaryCurrentAnimation = Animatable(effectX, effectY, self.game, "slash", 71, False, self.attack_background, "img/battle/slash.png", 5, 1, 30, self.attack_background, False, None)
            self.secondaryCurrentAnimation.add(self.game.clock_group)
        elif mode == "attacking":
            if self.pendingAttack.region == "Target: head":
                self.currentAnimation = Animatable(80, 325, self.game, "head attack", 72, False, self.enemy.idle_background, self.enemy.attackHeadAnim, 2, 1, None, self.enemy.idle_background, True, None)
            elif self.pendingAttack.region == "Target: arms":
                if self.pendingAttack.specificRegion == "Left":
                    self.currentAnimation = Animatable(80, 325, self.game, "left arm attack", 72, False, self.enemy.idle_background, self.enemy.attackLeftArmAnim, 2, 1, None, self.enemy.idle_background, True, None)
                elif self.pendingAttack.specificRegion == "Right":
                    self.currentAnimation = Animatable(80, 325, self.game, "right arm attack", 72, False, self.enemy.idle_background, self.enemy.attackRightArmAnim, 2, 1, None, self.enemy.idle_background, True, None)
            elif self.pendingAttack.region == "Target: legs":
                if self.pendingAttack.specificRegion == "Left":
                    self.currentAnimation = Animatable(80, 325, self.game, "left leg attack", 72, False, self.enemy.idle_background, self.enemy.attackLeftLegAnim, 2, 1, None, self.enemy.idle_background, True, None)
                elif self.pendingAttack.specificRegion == "Right":
                    self.currentAnimation = Animatable(80, 325, self.game, "head attack", 72, False, self.enemy.idle_background, self.enemy.attackRightLegAnim, 2, 1, None, self.enemy.idle_background, True, None)
            elif self.pendingAttack.region == "Target: torso":
                    self.currentAnimation = Animatable(80, 325, self.game, "head attack", 72, False, self.enemy.idle_background, self.enemy.attackTorsoAnim, 2, 1, None, self.enemy.idle_background, True, None)
            self.secondaryCurrentAnimation = Animatable(257, 225, self.game, "Enemy attack clock", 73, False, "img/battle/attack_clock_bg.png", "img/battle/enemy_clock.png", 40, 1, None, "img/battle/attack_clock_bg.png", True, None)
            self.currentAnimation.add(self.game.clock_group)
            self.secondaryCurrentAnimation.add(self.game.clock_group)
        elif mode == "successful attack":
            if self.pendingAttack.region == "Target: head":
                self.currentAnimation = Animatable(80, 325, self.game, "successful head attack", 72, False, self.enemy.idle_background, self.enemy.attackHeadSuccessfulAnim, 5, 1, None, self.enemy.idle_background, True, None)
            elif self.pendingAttack.region == "Target: arms":
                if self.pendingAttack.specificRegion == "Left":
                    self.currentAnimation = Animatable(80, 325, self.game, "successful left arm attack", 72, False, self.enemy.idle_background, self.enemy.attackLeftArmSuccessfulAnim, 5, 1, None, self.enemy.idle_background, True, None)
                elif self.pendingAttack.specificRegion == "Right":
                    self.currentAnimation = Animatable(80, 325, self.game, "successful right arm attack", 72, False, self.enemy.idle_background, self.enemy.attackRightArmSuccessfulAnim, 5, 1, None, self.enemy.idle_background, True, None)
            elif self.pendingAttack.region == "Target: legs":
                if self.pendingAttack.specificRegion == "Left":
                    self.currentAnimation = Animatable(80, 325, self.game, "successful left arm attack", 72, False, self.enemy.idle_background, self.enemy.attackLeftLegSuccessfulAnim, 5, 1, None, self.enemy.idle_background, True, None)
                elif self.pendingAttack.specificRegion == "Right":
                    self.currentAnimation = Animatable(80, 325, self.game, "successful right arm attack", 72, False, self.enemy.idle_background, self.enemy.attackRightLegSuccessfulAnim, 5, 1, None, self.enemy.idle_background, True, None)
            elif self.pendingAttack.region == "Target: torso":
                    self.currentAnimation = Animatable(80, 325, self.game, "successful torso attack", 72, False, self.enemy.idle_background, self.enemy.attackTorsoSuccessfulAnim, 5, 1, None, self.enemy.idle_background, True, None)
            self.currentAnimation.add(self.game.clock_group)
        elif mode == "unsuccessful attack":
            self.currentAnimation = Animatable(80, 325, self.game, "blocked attack", 72, False, self.enemy.idle_background, self.enemy.hurtAnim, 5, 1, None, self.enemy.idle_background, True, None)  
            self.currentAnimation.add(self.game.clock_group)
            
    def enemyAnimation(self):
        if self.currentAnimation.name != "Enemy hurt prop":
            
            self.currentAnimation.animate()
        
        if self.secondaryCurrentAnimation != None:
            self.secondaryCurrentAnimation.animate()
        self.checkDurations()

    def checkDurations(self):
        if self.isHurt == True:
            if self.secondaryCurrentAnimation.animationCount == 4:
                print("Condition met!")
                self.currentAnimation.remove(self.game.clock_group)
                self.chooseAnimation("idling", None, None)                
                self.secondaryCurrentAnimation = None
                self.isHurt = False
        elif self.isAttacking == True:
            if self.secondaryCurrentAnimation.animationCount == 39:
                print("Enemy turn over")
                self.currentAnimation.remove(self.game.clock_group)
                self.chooseAnimation("idling", None, None)
                self.secondaryCurrentAnimation.remove(self.game.clock_group)
                self.secondaryCurrentAnimation.permaErase()
                self.secondaryCurrentAnimation = None
                if self.pendingAttack != None:
                    damage = self.pendingAttack.calculateDamage()
                    self.game.callUpdateStatusBar(-1 * damage, 1)
                    self.logDamage(damage, self.pendingAttack.player.name, self.pendingAttack.enemy.name)
                    self.chooseAnimation("successful attack", None, None)
                    self.successfulAttack = True
                    self.unsuccessfulAttack = False
                else:
                    self.chooseAnimation("unsuccessful attack", None, None)
                    self.successfulAttack = False
                    self.unsuccessfulAttack = True
                self.isAttacking = False
        elif self.successfulAttack == True:
            if self.currentAnimation.animationCount == 4:
                print("Attack animation over")
                self.currentAnimation.remove(self.game.clock_group)
                self.chooseAnimation("idling", None, None)
                self.successfulAttack = False
                self.logAttack(self.pendingAttack)
        elif self.unsuccessfulAttack == True:
            if self.currentAnimation.animationCount == 4:
                print("Attack animation over")
                self.currentAnimation.remove(self.game.clock_group)
                self.chooseAnimation("idling", None, None)
                self.unsuccessfulAttack = False
        

    def logAttack(self, attack):
        playerName = attack.player.name
        enemyName = attack.enemy.name
        if isinstance(attack.move, str) == True:
            moveName = attack.move
        else:
            print("This option was chosen for some reason")
            moveName = attack.move.name
            print(moveName)
        print(moveName)
        regionName = attack.region
        specificRegionName = attack.specificRegion
        if regionName == "Target: head":
            regionName = "head"
        elif regionName == "Target: torso":
            regionName = "torso"
        elif regionName == "Target: arms":
            if specificRegionName == "Attack left arm" or specificRegionName == "Left":
                regionName = "left arm"
                specificRegionName = ""
            elif specificRegionName == "Attack right arm" or specificRegionName == "Right":
                regionName = "right arm"
                specificRegionName = ""
        elif regionName == "Target: legs":
            if specificRegionName == "Attack left leg" or specificRegionName == "Left":
                regionName = "left leg"
                specificRegionName = ""
            elif specificRegionName == "Attack right leg" or specificRegionName == "Right":
                regionName = "right leg"
                specificRegionName = ""
        outputString = playerName + " used " + moveName + " at " + enemyName + "'s " + regionName + "." 

        self.drawToLog(outputString)

    def logDamage(self, damage, combatant1, combatant2):
        outputString = combatant1 + " dealt " + str(damage) + " damage to " + combatant2 + " with this attack."
        self.drawToLog(outputString)

    def drawToLog(self, outputString):
        textwrapper = textWrapper()
        
        textwrapper.blitText(self.image, self.battleLogX, self.battleLogY, outputString, 200, 15, 12, (255, 255, 255))
        text_size = textwrapper.textsize
        text_height = text_size[1]

        self.battleLogY += (text_height + 20)
            
    def player_clock_tick(self):
        self.player_clock.animate()

    def enemy_clock_tick(self):
        self.enemy_clock.animate()

    def enemy_turn(self):
        available_enemy_attacks = self.enemy.attack_moves

        attack_index = randint(0, len(available_enemy_attacks) - 1)

        attack = available_enemy_attacks[attack_index] #randomly generate an attack to use
        print("Attack choice:")
        print(attack.name)
        is_successful = attack.hitDeterminer()

        if(is_successful): #if the attack doesn't miss
            dmg = attack.getDMG()
            dmg_type = attack.getDMGType()
            elemental = attack.getElemental()
            isCrit = attack.critDeterminer()
            if isCrit == True:
                dmg *= 2
            regions = ["Target: arms", "Target: legs", "Target: head", "Target: torso"]
            sides = ["Left", "Right"]
            body_part_index = randint(0, len(regions) - 1)
            body_part = regions[body_part_index]
            specific_body_part_index = None
            specific_body_part = None
            if body_part_index == 0 or body_part_index == 1:
                specific_body_part_index = randint(0, 1)
                specific_body_part = sides[specific_body_part_index]

            magnitudes = ["Light attack", "Heavy attack", "Charged attack"]
            magnitude_index = randint(0, len(magnitudes) - 1)
            magnitude = magnitudes[magnitude_index]
            #self.player.takeDamage(dmg, dmg_type, body_part, elemental)
            attack = Attack(self.enemy, self.player, "Enemy attack", magnitude, body_part, specific_body_part, False, attack)  
            print("Bruh")

            self.pendingAttack = attack
            self.chooseAnimation("attacking", None, None)
            self.isAttacking = True
            self.isIdling = False
            self.isHurt = False
            
            #damage = attack.calculateDamage()
            #print("Damage taken!")
            #self.game.callUpdateStatusBar(-1 * damage, 1)
        else:
            print("Attack missed!")
            pass

    
    
            

    def turn_determiner(self):
        if self.turn_count % 2 != 0:
            self.modifyOptions(1)
            self.player_clock_tick()
            self.player_turn_length += 1
            if self.player_turn_length == 12:
                self.turn_count += 1
                self.player_turn_length = 0
                self.turn_indicator("Goblin")
        elif self.turn_count % 2 == 0:
            self.modifyOptions(2)
            self.enemy_clock_tick()
            self.enemy_turn_length += 1
            if self.enemy_turn_length == 5:
                print("Enemy turn executed.")
                self.enemy_turn()
                
            if self.enemy_turn_length == 12:
                self.chooseAnimation("idling", None, None)
                self.turn_count += 1
                self.enemy_turn_length = 0
                self.turn_indicator("Horace")
    
    

    def turn_indicator(self, combatant):
        
        turnMessage = combatant + "'s turn"
        textwrapper = textWrapper()

        self.image.blit(self.bg, (106, 34), (106, 34, 211, 58))

        textwrapper.blitText(self.image, 106, 34, turnMessage, 211, 30, 10, (255, 255, 255))

    def modifyOptions(self, turn):
        if turn == 1:
            self.moveset_tree.horace_turn()
        else:
            self.moveset_tree.enemy_turn()
        self.eraseCurrentTree()
        self.displayCurrentMoves()
        self.displayCurrentKeyCombos()
        
    def keyInputHandler(self, keyPress):
        key = keyPress[0]
        print("KEY: " + key)
        delay = keyPress[1]
        checkedKey = self.moveset_tree.checkInput(key) 
        print(checkedKey)
        if checkedKey == "False":
            if(self.moveset_tree.getNumber() == 6):
                self.displayPastKeystrokes(key)
            else:
                print("Wrong key pressed")
                pass
        else:
            self.displayPastKeystrokes(key)
            options = [self.moveset_tree.currentTree.c1, self.moveset_tree.currentTree.c2, self.moveset_tree.currentTree.c3, self.moveset_tree.currentTree.c4, self.moveset_tree.currentTree.c5, self.moveset_tree.currentTree.c6]
            #print(options)
            kc_list = self.moveset_tree.returnChoices()
            #print(kc_list)
            selection = kc_list[checkedKey]
            
            if isinstance(selection, list):

                movesList = self.moveset_tree.getCurrentTreeDesc()
                print(movesList)
                move = movesList[checkedKey]
                self.handleFinalKeyInput(move)
                
                self.moveset_tree.currentTree = options[checkedKey]
                self.eraseCurrentTree()
                self.displayCurrentMoves()
                self.displayCurrentKeyCombos()
            elif isinstance(selection, str):
                movesList = self.moveset_tree.getCurrentTreeDesc()
                print(self.moveset_tree.getNumber())
                if(self.moveset_tree.getNumber() == 6):
                    keys = list(self.player.learnedMoves.keys())
                    move = keys[checkedKey]
                    print("Move:" + move)
                    self.handleFinalKeyInput(move)
                else:
                    move = movesList[checkedKey]
                    self.handleFinalKeyInput(move)
            else:
                print("Do nothing")

    def displayPastKeystrokes(self, keystroke):
        
        if keystroke == "LEFT":
            leftKeyStroke = Animatable(self.keystrokesX, self.keystrokesY, self.game, keystroke, 69, False, self.keystrokes_background, self.KEYLEFT_TRANSITION, 10, 1, 3, self.keystrokes_background, False, None)    
            leftKeyStroke.add(self.game.clock_group)
            self.displayed_keystrokes.append(leftKeyStroke)
        elif keystroke == "RIGHT":
            rightKeyStroke = Animatable(self.keystrokesX, self.keystrokesY, self.game, keystroke, 69, False, self.keystrokes_background, self.KEYRIGHT_TRANSITION, 10, 1, 3, self.keystrokes_background, False, None)    
            rightKeyStroke.add(self.game.clock_group)
            self.displayed_keystrokes.append(rightKeyStroke)
        elif keystroke == "UP":
            upKeyStroke = Animatable(self.keystrokesX, self.keystrokesY, self.game, keystroke, 69, False, self.keystrokes_background, self.KEYUP_TRANSITION, 10, 1, 3, self.keystrokes_background, False, None)    
            upKeyStroke.add(self.game.clock_group)
            self.displayed_keystrokes.append(upKeyStroke)
        elif keystroke == "DOWN":
            print("Down keystroke registered!")
            downKeyStroke = Animatable(self.keystrokesX, self.keystrokesY, self.game, keystroke, 69, False, self.keystrokes_background, self.KEYDOWN_TRANSITION, 10, 1, 3, self.keystrokes_background, False, None)    
            downKeyStroke.add(self.game.clock_group)
            self.displayed_keystrokes.append(downKeyStroke)
        self.keystrokesX += 17


        
    def handleFinalKeyInput(self, move):
        print("Move: " + move)
        self.combos.append(move)
        print("Combos: ")
        print(self.combos)
        print(self.moveset_tree.getNumber())
        if self.moveset_tree.getNumber() == 6:
            print("Attack ready to be executed!")
            print(self.combos)
            hand = self.combos[1]
            magnitude = self.combos[2]
            region = self.combos[3]
            if region == "Target: head" or region == "Target: torso":
                specRegion = None
                isSpecAttack = False
                move = self.combos[4]
            else:
                specRegion = self.combos[4]
                isSpecAttack = False
                move = self.combos[5]
            statEffectBonus = False
            attack = Attack(self.player, self.enemy, hand, magnitude, region, specRegion, isSpecAttack, move)
            self.logAttack(attack)
            #self.attackVisuals()
            self.newMethod(attack)
            damage = attack.calculateDamage()
            self.logDamage(damage, attack.player.name, attack.enemy.name)
            self.game.callUpdateStatusBar(-1 * damage, 2)
            self.moveset_tree.resetCurrentTree()
            self.eraseCurrentTree()
            self.displayCurrentMoves()
            self.displayCurrentKeyCombos()
            self.combos = []
        elif self.moveset_tree.getNumber() == 4:
            print("Blocked!")
            if self.pendingAttack != None:
                isValidBlock = False
                if self.pendingAttack.region == "Target: head" or self.pendingAttack.region == "Target: torso":
                    if self.combos[3] == "High block":
                        isValidBlock = True
                elif self.pendingAttack.region == "Target: arms" or self.pendingAttack.region == "Target: legs":
                    if self.combos[3] == "Low block":
                        isValidBlock = True
                if isValidBlock == True:
                    self.blockAttack()
                self.moveset_tree.resetCurrentTree()
                #self.attackAnimations.clear()
                #self.enemy_hurt_anim.add(self.game.clock_group)
                #self.attackAnimations.append(self.enemy_hurt_anim)    

    def blockAttack(self):
        self.pendingAttack = None
        print("Attack successfully blocked!")
   

    def newMethod(self, attack):
        targetRect = None
        attackX = 0
        attackY = 0
        if attack.region == "Target: arms":
            if attack.specificRegion == "Attack left arm":
                
                attackX = 278
                attackY = 395
            elif attack.specificRegion == "Attack right arm":
                attackX = 90
                attackY = 372
        elif attack.region == "Target: legs":
            if attack.specificRegion == "Attack left leg":
                attackX = 235
                attackY = 508
            elif attack.specificRegion == "Attack right leg":
                attackX = 163
                attackY = 490
        elif attack.region == "Target: torso":
            attackX = 200
            attackY = 392
        elif attack.region == "Target: head":
            attackX = 204
            attackY = 337

        

        self.isHurt = True
        self.chooseAnimation("hurt", attackX, attackY)
        
        

    def animateAttack(self):
        print("Animated?")
        for animation in self.attackAnimations:
            print("Animated")
            animation.animate()
    

    def displayCurrentMoves(self):
        movesList = self.moveset_tree.getCurrentTreeDesc()
        textwrapper = textWrapper()
        x = 432
        y = 9
        for message in movesList:
            textwrapper.blitText(self.image, x, y, message, 125, 15, 15, (255, 255, 255))
            y = y + 25

    def displayCurrentKeyCombos(self):
        keyCombosList = self.moveset_tree.returnChoices()
        x = 567
        y = 9
        tempX = 0
        combo = 0
        while combo < len(keyCombosList):
            if isinstance(keyCombosList[combo], str):
                if keyCombosList[combo] == "LEFT":
                    self.image.blit(self.KEYLEFT, (x, y))
                elif keyCombosList[combo] == "RIGHT":
                    self.image.blit(self.KEYRIGHT, (x, y))
                elif keyCombosList[combo] == "UP":
                    self.image.blit(self.KEYUP, (x, y))
                elif len(keyCombosList[combo]) > 5:
                    self.handleKeyRepeats(keyCombosList[combo], x, y) #handle key combinations like "LEFT LEFT" or "UP DOWN"
                else:
                    self.image.blit(self.KEYDOWN, (x, y))
                y = y + 25
            elif isinstance(keyCombosList[combo], list):
                #tempX = x
                
                for key in keyCombosList[combo]:
                    
                    if key == "LEFT":
                        self.image.blit(self.KEYLEFT, (x, y))
                    elif key == "RIGHT":
                        self.image.blit(self.KEYRIGHT, (x, y))
                    elif key == "UP":
                        self.image.blit(self.KEYUP, (x, y))
                    else:
                        self.image.blit(self.KEYDOWN, (x, y))
                    y = y + 25
                    
                if len(keyCombosList[combo]) > 1:
                    combo += 1 #skip next iteration 
                    
                #x = tempX
                
            else:
                pass
                y = y + 25
            combo += 1

    def eraseCurrentTree(self):
        self.image.blit(self.bg, (432, 6), (432, 6, 206, 151))
                
    def handleKeyRepeats(self, inputKeys, x, y):
        tempX = x
        keysSplit = inputKeys.split()
        for key in keysSplit:
            print(key)
            if key == "LEFT":
                self.image.blit(self.KEYLEFT, (tempX, y))
            elif key == "RIGHT":
                self.image.blit(self.KEYRIGHT, (tempX, y))
            elif key == "UP":
                self.image.blit(self.KEYUP, (tempX, y))
            else:
                self.image.blit(self.KEYDOWN, (tempX, y))
            tempX = tempX + 20
