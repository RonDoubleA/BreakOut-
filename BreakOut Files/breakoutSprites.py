'''Name: Aaron Leung
Date: April 14, 2015
Subject: breakoutSprites'''

import pygame

class Rect(pygame.sprite.Sprite):
    '''This class represents the sprite for rectangle-based classes which can
    collide with other sprites. All methods which are useful for all sprites
    relating to collision with other sprites are grouped here for ease of reuse
    and a sense of encapsulation to not directly access the sides of the rect without
    an accessor method
    This class is not intended to be created as an object'''
    
    def __init__(self):
        '''This method runs the pygame sprite initializer for the child sprites
        of this class'''
        pygame.sprite.Sprite.__init__(self)
    
    def get_left_rect(self):
        '''This method returns the self.rect.left value of the sprite. It takes
        no parameters'''
        return self.rect.left
    
    def get_right_rect(self):
        '''This method returns the self.rect.right value of the sprite. It takes
        no parameters'''
        return self.rect.right
    
    def get_top_rect(self):
        '''This method returns the self.rect.top value of the sprite. It takes
        no parameters'''
        return self.rect.top
    
    def get_bottom_rect(self):
        '''This method returns the self.rect.bottom value of the sprite. It takes
        no parameters'''
        return self.rect.bottom

class Ball(Rect):
    '''This class defines the sprite for our Ball.'''
    def __init__(self, screen):
        '''This method takes the screen as a parameter. It initializes the image and rect attributes,
        x,y direction of the ball, sound effects, and other variables'''
        #initializes the Rect parent class
        Rect.__init__(self)
        
        #sets the image and rect attributes
        self.image = pygame.Surface((20,20))
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (255, 255, 0), (10, 10), 10, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2,screen.get_height()/2 + 25)
        
        #sound effects for collision
        #when it hits a wall or a paddle
        self.__hit_wall_paddle_sound = pygame.mixer.Sound("wall or paddle bounce.wav")
        self.__hit_wall_paddle_sound.set_volume(0.5)
        
        #when it hits the endzone
        self.__hit_endzone_sound = pygame.mixer.Sound("hit_endzone.wav")
        self.__hit_endzone_sound.set_volume(0.9)
        
        #when it hits a brick
        self.__hit_brick_sound = pygame.mixer.Sound("brick_hit.wav")
        self.__hit_brick_sound.set_volume(0.5)
         
        # Instance variables to keep track of the screen surface
        # and set the initial x and y vector for the ball.
        self.__dx = 5
        self.__dy = 4
        
        #variable for checking if ball hits the bottom of the paddle or not
        self.__ignore_hit_bottom_collision = False
        
    def change_direction(self, rectangle):
        '''This method takes a rectangle in the game as a parameter. Based on 
        where the ball hits the object, it will adjust its direction'''
        
        #sound effects
        if isinstance(rectangle, Player) and self.__dy < 0 or isinstance(rectangle, Border):
            self.__hit_wall_paddle_sound.play(0)
        elif isinstance(rectangle, Brick):
            self.__hit_brick_sound.play(0)
        else:
            self.__hit_endzone_sound.play(0)
        
        #checks if ball is colliding with Player, and ignores collision with bottom of paddle
        if isinstance(rectangle, Player) and self.__dy > 0:
            self.__ignore_hit_bottom_collision = True
        
        #colliding with bottom of entity
        if self.__ignore_hit_bottom_collision == False:
            if self.rect.top <= rectangle.get_bottom_rect() and rectangle.get_bottom_rect() - self.rect.top <= self.__dy:
                self.rect.top = rectangle.get_bottom_rect()
                self.__dy = -self.__dy
            
        
        #colliding with top of entity
        if self.rect.bottom >= rectangle.get_top_rect() and self.rect.bottom - rectangle.get_top_rect() <= -self.__dy:
            self.rect.bottom = rectangle.get_top_rect()
            self.__dy = -self.__dy
                
        #colliding with left side of entity
        if self.rect.right >= rectangle.get_left_rect() and self.rect.right - rectangle.get_left_rect() <= self.__dx:
            self.rect.right = rectangle.get_left_rect()
            self.__dx = -self.__dx
          
        #colliding with right side of entity
        if self.rect.left <= rectangle.get_right_rect() and rectangle.get_right_rect() - self.rect.left <= -self.__dx:
            self.rect.left = rectangle.get_right_rect()
            self.__dx = -self.__dx
        
        self.__ignore_hit_bottom_collision = False
        
    def reverse_direction(self):
        '''This method is a special method designed for the rare circumstance
        of the ball hitting 3 bricks at a time. To avoid unnecessary calculations
        of where the ball should go, it simply reverses the direction of the ball
        as expected. This method takes no parameters and does not return anything'''
        self.__dx = -self.__dx
        self.__dy = -self.__dy
        
        #sound effect
        self.__hit_brick_sound.play(0)
    
    def update(self):
        '''This method will be called automatically to reposition the ball'''
        self.rect.left += self.__dx
        self.rect.top -= self.__dy
        
        

class Player(Rect):
    '''This class defines the sprite of the player paddle'''
    
    def __init__(self, screen, y):
        '''This initializer takes a screen surface, and player number as
        parameters. It initializes the image and rect attributes, and the x velocity'''
        # Call the parent __init__() method
        Rect.__init__(self)
            
        # Define the image attributes for a black rectangle.
        self.image = pygame.image.load("paddle1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (98, 20))
        self.rect = self.image.get_rect()   
        self.__y = y

        self.rect.center = (screen.get_width()/2, y)
        
        self.__dx = 0
        
    def movement(self, direction, border):
        '''This method takes the direction of the paddle and any borders the paddles hit. 
        It then changes the direction of the paddle and if it hits a border,
        it does not go past the border and returns True'''
        
        #left
        if direction == -1:
            self.__dx = -5
        #right
        elif direction == 1:
            self.__dx = 5
        #immobile
        else:
            self.__dx = 0
            
        #stopping it from passing the left border
        if self.rect.left + self.__dx < border.get_right_rect() and\
           border.get_right_rect() - (self.rect.left + self.__dx) < -(self.__dx-1) and\
           self.__dx < 0:
            
            
            self.rect.left = border.get_right_rect()
            self.__dx = 0
            
            return True
        
        #stopping the paddle from passing the right border
        if self.rect.right + self.__dx > border.get_left_rect() and \
           self.rect.right + self.__dx - border.get_left_rect() < self.__dx+1 and\
           self.__dx > 0:

            
            self.rect.right = border.get_left_rect()
            self.__dx = 0
            
            return True
        
    def get_centerx(self):
        '''This method returns the center x value of the paddle'''
        return self.rect.centerx
    
    def change_size(self):
        '''This method changes the size of the paddle'''
        self.__saved_x = self.get_centerx()
        self.image = pygame.transform.scale(self.image, (49, 20))
        self.rect = self.image.get_rect() 
        self.rect.center = (self.__saved_x, self.__y)
    
    def update(self):
        '''This method is called automatically to move the paddle. It then resets
        the velocity of the paddle'''
        self.rect.left += self.__dx
        self.__dx = 0
    


class Brick(Rect):
    '''this class defines the sprite for the Brick'''
    def __init__(self, colour, coords, point, size):
        '''This method takes the colour, the coordinates, the point value, and the size
        as parameters. It initializes the image and rect attributes, along with the point and 
        y velocity.'''
        Rect.__init__(self)
        self.image = pygame.Surface(size)
        self.image = self.image.convert()
        self.image.fill((255,255,255))
        pygame.draw.rect(self.image, colour, ((1,1), (33,23)), 0)
        self.rect = self.image.get_rect()
        
        self.rect.left = coords[0]
        self.rect.top = coords[1]
    
        self.__point = point
        self.__dy = 0
        
    def move(self, move):
        '''This method takes the number of bricks which were hit
        by the ball as a parameter.
        It then moves the bricks down several pixels by the number of bricks
        multiplied by 2'''
        self.__dy -= move * 2
        
    
    def update(self):
        '''This method updates the position of the brick. It moves them down
        by the y velocity before resetting the y velocity to 0'''
        self.rect.top -= self.__dy
        self.__dy = 0
        
    
    def get_point(self):
        '''This method returns the number of points that brick is worth'''
        return self.__point    

class Border(Rect):
    '''This class represents the sprite of the borders'''
    def __init__(self, hor_or_vert, coords):
        '''This method initializes the image and rect attributes. It takes whether
        or not the border is horizontal or vertical and the coordinates the border
        is at for the rect attributes'''
        Rect.__init__(self)
        
        #sets the border to be vertical
        if hor_or_vert == "vert":
            self.image = pygame.Surface((5, 480))
        #sets the border to be horizontal 
        else:
            self.image = pygame.Surface((640, 5))
        
        self.image = self.image.convert()
        self.image.fill((102, 153, 153))
        self.rect = self.image.get_rect()
        
        self.rect.left = coords[0]
        self.rect.top = coords[1]
        
        
class EndZone(Rect):
    '''This class represents the sprite for the end zone'''
    def __init__(self,screen):
        '''This method takes the screen as a parameter. It initializes the image and rect
        attributes'''
        Rect.__init__(self)
        
        self.image = pygame.Surface((630, 5))
        
        self.image = self.image.convert()
        
        self.image.fill((0,0,0))
        
        self.rect = self.image.get_rect()
        
        self.rect.left = 5
        self.rect.bottom = screen.get_height()
        
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class represents the sprite for the scorekeeper'''
    def __init__(self):
        '''This method initializes the font, the score, and the lives attributes'''
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.Font("DS-DIGI.ttf", 30)
        self.__score = 0
        self.__lives = 3
        
        
    def scored(self, point):
        '''This method takes the number of points as a paramater and
        adds it to the scorekeeper'''
        self.__score += point
        
    def miss(self):
        '''This method lowers the number of lives by one'''
        self.__lives -= 1
    
    def get_lives(self):
        '''This method returns the number of lives'''
        return self.__lives
    
    def get_score(self):
        '''This method returns the score'''
        return self.__score
    
    def update(self):
        '''This method creates the image and rect attributes and updates the text'''
        message = "Score: %d   Lives: %d" % (self.__score, self.__lives)
        self.image = self.__font.render(message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.centerx = 320
        
        
class GiantText(pygame.sprite.Sprite):
    '''This class represents the sprite for the end text'''
    def __init__(self, screen):
        '''This class takes the screen as a parameter. It initializes the font and the center
        of the text'''
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("DS-DIGI.ttf", 100)
        self.__center = (screen.get_width()/2, screen.get_height()/2)
        
    def set_text(self, text, colour):
        '''This method takes the text and the colour as parameters. It sets the
        text to the text and the colour to the colour'''
        self.__text = text
        self.__colour = colour
        
    def update(self):
        '''This method initializes the image and rect attributes and updates the 
        text in the rect.'''
        message = self.__text
        self.image = self.__font.render(message, 1, self.__colour)
        self.rect = self.image.get_rect()
        self.rect.center = self.__center
        
        
