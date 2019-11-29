import pygame
from collections import deque
from random import randint
from Tree import *
from Player import *

class TreeManager(object):

    def __init__(self, player):
        self.player = player
        t1desc = ["Parry/foil left arm", "Parry/foil right arm"]
        t2desc = ["Parry/foil left leg", "Parry/foil right leg"]
        t3desc = ["Parry/foil against head", "Parry/foil against torso", "Parry/foil against arms", "Parry/foil against legs"]
        t4desc = ["High block", "Low block"]
        t5desc = ["Block", "Parry", "Foil"]
        #t6desc = ["Attack combo 1", "Attack combo 2", "Attack combo 3", "Attack combo 4", "Attack combo 5", "Attack combo 6"]
        t6desc = self.player.learnedMoves.keys()
        t7desc = ["Attack left leg", "Attack right leg"]
        t8desc = ["Attack left arm", "Attack right arm"]
        t9desc = ["Target: head", "Target: torso", "Target: arms", "Target: legs"]
        t10desc = ["Light attack", "Heavy attack", "Charged attack"]
        t11desc = ["Quick use slot 1", "Quick use slot 2", "Quick use slot 3", "Quick use slot 4"]
        t12desc = ["Access backpack", "Quick use item"]
        t13desc = ["Left handed attack", "Right handed attack"]
        t14desc = ["Left handed block", "Right handed block"]
        t15desc = ["Special key combo one", "Special key combo 2", "Special key combo 3", "Special key combo 4", "Special key combo 5", "Special key combo 6"]
        t16desc = ["Off hand special move", "Main hand special move"]
        t17desc = ["Use item", "Attack", "Block", "Dodge", "Special"]
        self.t1 = Tree("LEFT", "RIGHT", None, None, None, None, ["RIGHT"], t1desc, 1)
        self.t2 = Tree("LEFT", "RIGHT", None, None, None, None, ["DOWN"], t2desc, 2)
        self.t3 = Tree("UP", "LEFT", self.t2, self.t1, None, None, ["RIGHT", "RIGHT RIGHT"], t3desc, 3)
        self.t4 = Tree("UP", "DOWN", None, None, None, None, ["LEFT"], t4desc, 4)
        self.t5 = Tree(self.t4, self.t3, self.t3, None, None, None, ["RIGHT", "LEFT", "RIGHT RIGHT"], t5desc, 5)
        self.t6 = Tree(self.player.learnedMoves["Swing"], self.player.learnedMoves["Thrust"], self.player.learnedMoves["Lunge"], None, None, None, ["UP", "RIGHT"], t6desc, 6)
        self.t7 = Tree(self.t6, self.t6, None, None, None, None, ["DOWN"], t7desc, 7)
        self.t8 = Tree(self.t6, self.t6, None, None, None, None, ["LEFT"], t8desc, 8)
        self.t9 = Tree(self.t6, self.t6, self.t8, self.t7, None, None, ["LEFT", "RIGHT", "UP"], t9desc, 9)
        self.t10 = Tree(self.t9, self.t9, self.t9, None, None, None, ["LEFT", "RIGHT"], t10desc, 10)
        self.t11 = Tree("LEFT", "RIGHT", "UP", "DOWN", None, None, ["RIGHT"], t11desc, 11)
        self.t12 = Tree("LEFT", self.t11, None, None, None, None, ["DOWN"], t12desc, 12)
        self.t13 = Tree(self.t10, self.t10, None, None, None, None, ["RIGHT"], t13desc, 13)
        self.t14 = Tree(self.t5, self.t5, self.t5, None, None, None, ["LEFT"], t14desc, 14)
        self.t15 = Tree(None, None, None, None, None, None, ["RIGHT", "LEFT"], t15desc, 15)
        self.t16 = Tree(self.t15, self.t15, None, None, None, None, ["UP"], t16desc, 16)
        self.t17 = Tree(self.t12, self.t13, self.t14, "LEFT LEFT", self.t16, None, ["UP"], t17desc, 17)
        self.currentTree = self.t17

        self.keyCombo = []

        self.comboIndex = 0

        self.validAttack = False

    def getNumber(self):
        return self.currentTree.number

    def returnChoices(self):
        choices = []
        if self.currentTree != None:
            if isinstance(self.currentTree.c1, str) or self.currentTree.c1 == None:
                choices.append(self.currentTree.c1)
            else:
                choices.append(self.currentTree.c1.kc)
            if isinstance(self.currentTree.c2, str) or self.currentTree.c2 == None:
                choices.append(self.currentTree.c2)
            else:
                choices.append(self.currentTree.c2.kc)
            if isinstance(self.currentTree.c3, str) or self.currentTree.c3 == None:
                choices.append(self.currentTree.c3)
            else:
                choices.append(self.currentTree.c3.kc)
            if isinstance(self.currentTree.c4, str) or self.currentTree.c4 == None:
                choices.append(self.currentTree.c4)
            else:
                choices.append(self.currentTree.c4.kc)
            if isinstance(self.currentTree.c5, str) or self.currentTree.c5 == None:
                choices.append(self.currentTree.c5)
            else:
                choices.append(self.currentTree.c5.kc)
            if isinstance(self.currentTree.c6, str) or self.currentTree.c6 == None:
                choices.append(self.currentTree.c6)
            else:
                choices.append(self.currentTree.c6.kc)
            return choices
        else:
            print("Invalid")
            return choices

    

    def checkInput(self, keyInput):
        
        choices = self.returnChoices()
        print("Choices:")
        print(choices)
        
        isValid = "False"
        for choice in choices:
            if isinstance(choice, str):
                    
                    if self.getNumber() == 6 or self.getNumber() == 4:
                        
                        combos = choice.split(" ")
                        
                        print(combos)
                        if len(self.keyCombo) >= len(combos):
                            print("Invalid!")
                            continue
                        else:
                            if combos[self.comboIndex] == keyInput:
                                self.keyCombo.append(combos[self.comboIndex])
                                print(self.keyCombo)
                                self.comboIndex += 1
                                self.validAttack = True

                                if self.listEqualityChecker(combos, self.keyCombo) == True:
                                    isValid = choices.index(choice)
                                    
                                    
                                
                                break
                        
                    
                
                    if keyInput == choice:
                        isValid = choices.index(choice)

            elif isinstance(choice, list):    
                if (keyInput in choice):
                    if len(choice) > 1: 
                        index = choice.index(keyInput)
                        return index
                    else:
                        isValid = choices.index(choice)
                        
                        break

        
                    
        if self.validAttack == False:
            print("Error: Invalid key combo!!!!!")
            self.keyCombos = []
            self.comboIndex = 0

        return isValid

    

    def listEqualityChecker(self, list1, list2):
        print("list 1")
        print(list1)
        if(len(list1) > 1):
            del[list1[len(list1) - 1]]
        print("list 2")
        
        print(list2)
        if(len(list1) != len(list2)):
            return False
        else:
            index1 = 0
            index2 = 0
            while index1 < len(list1):
                
                if(list1[index1] != list2[index2]):
                    return False
                else:
                    index1 += 1
                    index2 += 1
        return True
                

    def handleInput(self, keyInput):
        index = self.checkInput(keyInput)
        
        if isinstance(index, int):
            branchesList = [self.currentTree.c1, self.currentTree.c2, self.currentTree.c3, self.currentTree.c4, self.currentTree.c5, self.currentTree.c6]
            if isinstance(branchesList[index], Tree):
                self.currentTree = branchesList[index]
        else:
            print("Invalid input entered!")

    def resetCurrentTree(self):
        self.keyCombo = []
        self.comboIndex = 0
        self.currentTree = self.t17

    def getCurrentTreeDesc(self):
        return self.currentTree.desc

    def enemy_turn(self):
        new_t17_desc = ["Use Item", "", "Block", "Dodge", ""]
        self.t17.c2 = None
        self.t17.c3 = self.t14
        self.t17.c4 = "LEFT LEFT"
        self.t17.c5 = None
        self.t17.desc = new_t17_desc

    def horace_turn(self):
        new_t17_desc = ["Use Item", "Attack", "", "", "Special"]
        self.t17.c1 = self.t12
        self.t17.c2 = self.t13
        self.t17.c3 = None
        self.t17.c4 = None
        self.t17.c5 = self.t16
        self.t17.desc = new_t17_desc
        
