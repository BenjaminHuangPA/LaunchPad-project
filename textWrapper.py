import pygame
from collections import deque
from random import randint

class textWrapper(object):

    #The purpose of this class is thus: Pygame does not natively implement a way
    #to write text on multiple lines, and new line characters are ignored. Thus,
    #I wrote this class to format text that would be too long to fit a given width
    #into a paragraph.

    
    def __init__(self):
        pass #no need to pass anything into the constructor
        self.textsize = None

    def blitText(self, surface, x, y, text, width, font_size, line_height, color):
        R = color[0]

        G = color[1] #pass in the color as an RGB tuple

        B = color[2]

        pygame.font.init() #initialize pygame's font module

        textArray = text.split() #split the inputted text into separate words

        font = pygame.font.SysFont("Times New Roman", font_size) #initialize font object using the font size module

        yCoord = y #this variable will store the y coordinate of the lines we draw the text on.

        currentLineLength = 0 #this variable will store the length of the current line of text, for checking if we've exceeded the target width.

        textToDraw = "" #this variable (initialized to an empty String) will store the text to be written for each line.

        textSize = font.size(text) #this method returns a tuple of its argument's dimensions in the form (width, height)
        self.textsize = textSize
        if textSize[0] < width:
            #check if the text passed in is no more than a single line's worth. If that's the case, we can just blit it directly to the surface without having to worry about
            #new lines
            line = font.render(text, False, (R, G, B))
            surface.blit(line, (x, yCoord))
        else:
            #now we need to handle if the text passed in has a length greater than a single line
            for word in textArray:
                wordSize = font.size(word) #get the tuple describing each word's dimensions
                wordLength = wordSize[0] + 15 #get the word's length. Add +15 pixels to account for spaces.
                
                if currentLineLength + wordLength < width:
                    currentLineLength += wordLength
                    textToDraw = textToDraw + word + " "
                    #if we can add this word to the current line of text to be drawn (textToDraw) without exceeding the width of a single line, do so
                elif currentLineLength + wordLength > width:
                    #else, if adding the word would go over the limit imposed:
                    line = font.render(textToDraw, False, (R, G, B)) #render the text onto a surface
                    surface.blit(line, (x, yCoord)) #draw the surface containing the text onto the surface passed in
                    yCoord += line_height #increment yCoord to go to a new line.
                    currentLineLength = wordLength  #add the word's length to the currentLineLength variabel
                    textToDraw = word + " " #move the word that would have caused the line of text to go over the width to the start of the new line.
       
        lastLine = font.render(textToDraw, False, (R, G, B)) #finally, blit the last line of text onto the screen (which is almost always shorter than width and as a result is
        #not drawn by the above if statement
        surface.blit(lastLine, (x, yCoord))
