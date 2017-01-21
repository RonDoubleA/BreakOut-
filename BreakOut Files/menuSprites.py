'''Name: Aaron Leung
Date: April 25, 2015
Subject: Menu Sprites'''

import pygame

class Label(pygame.sprite.Sprite):
    '''This class represents the sprite for the label'''
    def __init__(self, screen, text, size, y_coord):
        '''This method takes the screen, the text, the size, and the y_coord as 
        parameters. It initializes the font, the text, the center of the text, the image,
        and the rect attributes.'''
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("DS-DIGI.ttf", size)
        self.__text = text
        self.__center = (screen.get_width()/2, y_coord)
        self.image = self.__font.render(self.__text, 1, (255,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.__center
        
    def get_text(self):
        '''This method returns the text in the label'''
        return self.__text
        
    def set_text(self,text):
        '''This method takes the text as a parameter. It sets the text to the 
        parameter'''
        self.__text = text
        
    def update(self):
        '''This method updates the image and rect attributes to the new text'''
        self.image = self.__font.render(self.__text, 1, (255,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.__center

class Animated_Label(pygame.sprite.Sprite):
    '''This class represents the sprite of an animated label'''
    def __init__(self, screen, text, font, size, y_coord, colour, colour_options):
        '''This method takes the screen, the text, the font, the size, the y_coord, 
        the colour, and the colour options as parameters. It initializes the font, the text,
        the center, the colour, and the colour options attributes'''
        pygame.sprite.Sprite.__init__(self)
        self.__font_style = font
        self.__font = pygame.font.Font(font, size)
        self.__text = text
        self.__center = (screen.get_width()/2, y_coord)
        self.__colour = colour
        self.__colour_options = colour_options
        
    def set_colour(self, colour):
        '''This method takes a colour as a parameter and sets the colour attribute
        to the parameter colour'''
        self.__colour = colour
        
    def set_font(self, font_style, size):
        '''This method takes a font style and a size as parameters and sets the font
        using those parameters'''
        self.__font = pygame.font.Font(font_style, size)
        
    def set_text(self, text):
        '''This method takes text as a parameter and sets the text attribute to that text'''
        self.__text = text
        
    def get_colour_options(self):
        '''This method returns the colour options attribute of the sprite'''
        return self.__colour_options
    
    def get_font_style(self):
        '''This method returns the font style attribute of the sprite'''
        return self.__font_style
    
    def get_text(self):
        '''This method returns the text attribute of the sprite'''
        return self.__text
    
    def get_colour(self):
        '''This method returns the colour attribute of the sprite'''
        return self.__colour
    
    def update(self):
        '''This method initializes and updates the image and rect attributes'''
        self.image = self.__font.render(self.__text, 1, self.__colour)
        self.rect = self.image.get_rect()
        self.rect.center = self.__center
    

        
class Flickering_Text(Animated_Label):
    def __init__(self, screen, text, font, size, y_coord, colour_options):
        Animated_Label.__init__(self, screen, text, font, size, y_coord, colour_options[0], colour_options)
        
    def flicker(self, half_second_check):
        '''This function takes one parameter, how far in the second the current second is in.
        It flickers the title and the start texts between two different colours based
        on which half of the second it is in. It does not return anything'''
        self.set_colour(self.get_colour_options()[half_second_check/15])
        
class Options(Animated_Label):
    def __init__(self, screen, text, y_coord):
        Animated_Label.__init__(self, screen, text, "DS-DIGI.ttf", 35, y_coord, (204,153,0), [(204,153,0), (255,255,0)])
        self.__hover_noise = pygame.mixer.Sound("whoop.wav")
        self.__hover_noise.set_volume(1.0)
        
        
    def hover_on(self):
        if self.get_colour() != self.get_colour_options()[1]:
            self.__hover_noise.play(0)
        self.set_font(self.get_font_style(), 40)
        self.set_colour(self.get_colour_options()[1])
        
    def hover_off(self):
        self.set_font(self.get_font_style(), 30)
        self.set_colour(self.get_colour_options()[0])
        
        
class HighScores(pygame.sprite.Sprite):
    def __init__(self, screen, y_coord, difficulty):
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("DS-DIGI.ttf", 25)
        
        try:
            self.__file = open(difficulty + ".txt", 'r')
            self.__text = difficulty.capitalize() + ": "  + self.__file.readline().strip() + " points"
            self.__file.close()
        
        except IOError:
            self.__text = difficulty.capitalize() + ": NOBODY"
            
        self.__center = (screen.get_width()/2, y_coord)
        
    def update(self):
        self.image = self.__font.render(self.__text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.__center
        
    
        
class Mouse(pygame.sprite.Sprite):
    '''This class represents the sprite for the mouse'''
    def __init__(self):
        '''This method initializes the image and rect attributes of the mouse sprite'''
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((1,1))
        self.image.fill((255,0,0))
        self.image.set_colorkey((255,0,0))
        self.rect = self.image.get_rect()
        
    def update(self):
        '''This method updates the position of the sprite using the mouse's position'''
        self.rect.center = pygame.mouse.get_pos()
    

        
    
        
        

   