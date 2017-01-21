'''Name: Aaron Leung
Date: April 4, 2015
Subject: Pygame Typer'''

import pygame

def pygame_typer(phrase, key, shift):
    '''This function takes 3 parameters, the initial phrase, the key pressed, and 
    whether or not the shift button is held. This is intended as a live-action
    typing program in pygame, returning the string along with what is typed after each character or deleting
    a character from the backspace'''
    copy = phrase
    
    character = ""
    
    other_punctuation = ['!','@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '{', '}', '|', ':', '"', '<','>', '?', '~']  
    
    correspondents = ['1', '2','3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '[', ']', '\\', ';', "'", ',', '.', '/', '`']
    
    #valid keys for typing
    if key < 256:
    
        #lowercase letters
        if key >= 97 and key <= 122 and shift == False:
            character = chr(key)
        
        #uppercase letters
        elif key>= 97 and key<= 122 and shift == True:
            character = chr(key-32)
            
        #comma, minus sign, period, forward slash and numbers
        elif key>= 44 and key <= 57 and shift == False:
            character = chr(key)
        
        
        #other non-shift lowercase punctuation
        elif (key == 39 or key == 59 or key == 61 or key == 91 or key == 92 or key == 93 or key == 96) and shift == False:
            character = chr(key)
        
        #backspace
        elif key == pygame.K_BACKSPACE:
            copy = copy[:-1]
            
        elif key == pygame.K_SPACE:
            character = "_"
        
        #other punctuation characters with shift
        elif chr(key) in correspondents and shift == True:
            character = other_punctuation[correspondents.index(chr(key))]
        
    copy += character
        
    return copy
    
        