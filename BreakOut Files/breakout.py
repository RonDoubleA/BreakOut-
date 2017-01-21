'''Name: Aaron Leung
Date: April 16, 2015
Subject: BreakOut!
Enhancements: Differing Brick Point Values
              Moving Layers Down the Screen (Available in Medium and Hard Difficulties)
              Cutting Width of Paddle (Available in Hard Difficulty)
              2 Paddles (Available in Two Player Mode) (Second player controlled by mouse)
              Title Screen and Main Menu
              Difficulty Settings
              Single Player vs. Multiplayer
              High Scores'''

#I - Import / Initialize
import pygame, breakoutSprites, menuSprites, pygameTyper
pygame.init()
pygame.mixer.init()

#COLOURS
RED = (255,0,0)
GREEN = (0,255,0)
GREEN2 = (0, 204, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
VIOLET = (204,0,240)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (153, 153, 102)

#D - Display
screen = pygame.display.set_mode((640, 480))

def main():
    '''This function contains the mainline code, consisting of the 
    menu, the game, and the high score'''
    
    pygame.display.set_caption("Break-Out!")
    
    #E - Entities
    
    #background
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, screen.get_size())
    background = background.convert()
    screen.blit(background, (0,0))
    
    #A - Action
    
        #A - Assign values to Variables
    
    game_playing = True
    
        #L - Loop
    while game_playing:
        #E - Event Handling
        
        #launches menu screen
        game_playing, player_count, difficulty = menu_screen(background)
        
        if game_playing == True:
            #launches game
            game_playing, score, lives = main_game(player_count, difficulty, background)
            
        #high scores are only stored for single player
        if game_playing == True and player_count == 1:
            #launches high scores
            game_playing = high_score_screen(score, lives, difficulty, background)
    
    pygame.quit()
    
def main_game(player_count, difficulty, background):
    '''This function is the main game. It takes 3 parameters, the player_count, the difficulty,
    and the background. It adjusts the number of players and the difficulty accordingly.
    It then returns the number of points, the number the lives, and whether or not
    the user has exited the application or not'''
    #E - Entities
    
    #physical entities
    scorekeeper = breakoutSprites.ScoreKeeper()
    ball = breakoutSprites.Ball(screen)
    player1 = breakoutSprites.Player(screen, 420)
    
    #creats a second player if multiplayer
    if player_count == 2:
        player2 = breakoutSprites.Player(screen, 450)
    
    endzone = breakoutSprites.EndZone(screen)
    
    #borders
    left_border = breakoutSprites.Border("vert", (0, 30))
    top_border = breakoutSprites.Border("hor", (0,30))
    right_border = breakoutSprites.Border("vert", (screen.get_width()-5, 30))
    
    borders = [left_border, top_border, right_border]
    
    #the win/lose sign at the end
    winlosetext = breakoutSprites.GiantText(screen)
    
    #bricks
    all_bricks = []
    row = 0
    
    for rows in range(35, 161, 25):
        
        brick_colours = [VIOLET, RED, YELLOW, ORANGE, GREEN, BLUE]
        for bricks in range(6, 603, 35):
            brick = breakoutSprites.Brick(brick_colours[row], (bricks, rows), 6-row, (35,25))
            all_bricks.append(brick)
        row += 1
        
    #groups
    brickSprites = pygame.sprite.Group(all_bricks)
    borderSprites = pygame.sprite.Group(borders)
    endTextSprites = pygame.sprite.Group(winlosetext)
    
    #sets the group based on the players
    if player_count == 1:
        ingameSprites = pygame.sprite.Group(all_bricks, scorekeeper, player1, endzone, ball, borders)
    else:
        ingameSprites = pygame.sprite.Group(all_bricks, scorekeeper, player1, player2, endzone, ball, borders)
    
    #Music based on difficulty
    if difficulty == "easy":
        pygame.mixer.music.load("No Spring Chicken.wav")
    elif difficulty == "medium":
        pygame.mixer.music.load("Birdland.wav")
    else:
        pygame.mixer.music.load("Get In Line.mp3")
        
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    
    #Win/Lose Sounds
    win_sound = pygame.mixer.Sound("MOM_GET_THE_CAMERA.wav")
    win_sound.set_volume(0.5)
    
    lose_sound = pygame.mixer.Sound("2SAD4ME.wav")
    lose_sound.set_volume(0.5)
    
    #A - Action
         #A - Assign values to variables
    clock = pygame.time.Clock()
    keepGoing = True
    direction1 = 0  
    direction2 = 0
    win = False
    continue_game = True
    left_button_down = False
    right_button_down = False
    original_brick_count= len(all_bricks)
    shrinked = False
    
    pygame.mouse.set_visible(False)
        #L - Loop
    while keepGoing:
        
        #T - Timer for frame rate
        clock.tick(30)
        
        #E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                continue_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_button_down = True
                if event.key == pygame.K_RIGHT:
                    right_button_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_button_down = False
                if event.key == pygame.K_RIGHT:
                    right_button_down = False
                    
        #checks which buttons are pressed and changes direction accordingly for player 1
        if left_button_down == right_button_down:
            direction1 = 0
        elif left_button_down == True:
            direction1 = -1
        elif right_button_down == True:
            direction1 = 1
            
        #checks where the mouse is in relation to the second paddle if there
        if player_count == 2:
            if pygame.mouse.get_pos()[0] > player2.get_centerx():
                direction2 = 1
            elif pygame.mouse.get_pos()[0] < player2.get_centerx():
                direction2 = -1
            else:
                direction2 = 0
              
        #preventing paddle from overlapping with borders
        for border in borders:
            if player1.movement(direction1, border):
                break
        
        if player_count == 2:
            for border in borders:
                if player2.movement(direction2, border):
                    break
        
        #ball colliding with blocks
        blocks_hit_list = pygame.sprite.spritecollide(ball, brickSprites, True)
        blocks_hit = len(blocks_hit_list)
        for block in blocks_hit_list:
            points = block.get_point()
            scorekeeper.scored(points)
            
        #checks how many bricks it collided with; adjusts collisions accordingly  
        #if it hits 3 blocks at a time
        if blocks_hit == 3:
            ball.reverse_direction()
            
        #if it hits 2 blocks at a time        
        elif blocks_hit == 2:
            #if it hit 2 blocks on top of each other
            if blocks_hit_list[0].get_left_rect() == blocks_hit_list[1].get_left_rect():
                temp_y = min(blocks_hit_list[0].get_top_rect(), blocks_hit_list[1].get_top_rect())
                #creates temporary block for collision calculations
                temp_block = breakoutSprites.Brick(BLACK, (blocks_hit_list[0].get_left_rect(), temp_y), 0, (35, 50))
                ball.change_direction(temp_block)
            #if it hits 2 blocks beside each other
            elif blocks_hit_list[0].get_top_rect() == blocks_hit_list[1].get_top_rect():
                temp_x = min(blocks_hit_list[0].get_left_rect(), blocks_hit_list[1].get_left_rect())
                #creates temporary block for collision calculations
                temp_block = breakoutSprites.Brick(BLACK, (temp_x, blocks_hit_list[0].get_top_rect()), 0, (70, 25))
                ball.change_direction(temp_block)
            else:
                ball.reverse_direction()
                
        #if it hits 1 block at a time       
        elif blocks_hit == 1:
            ball.change_direction(blocks_hit_list[0])
            
        #moves bricks down depending on difficulty
        if difficulty == "medium" or difficulty == "hard":
            for brick in range(len(all_bricks)):
                all_bricks[brick].move(blocks_hit)
                
        #ball colliding with walls
        border_hit_list = pygame.sprite.spritecollide(ball, borderSprites, False)
        for border in border_hit_list:
            ball.change_direction(border)
        
        #ball colliding with paddle
        if ball.rect.colliderect(player1.rect):
            ball.change_direction(player1)
        
        #ball colliding with second paddle if its there
        if player_count == 2:
            if ball.rect.colliderect(player2.rect):
                ball.change_direction(player2)
        
        #ball colliding with endzone
        if ball.rect.colliderect(endzone.rect):
            ball.change_direction(endzone)
            scorekeeper.miss()
            pygame.time.delay(2000)
            
        #shrinks the bar in half when half the bricks are gone and on hard difficulty
        if len(brickSprites) != 0 and original_brick_count / (len(brickSprites) * 1.0) == 2 and difficulty == "hard"\
           and shrinked == False:
            
            shrinked = True
            player1.change_size()
            if player_count == 2:
                player2.change_size()
        
        #checks to end game
        #no lives
        if scorekeeper.get_lives() == 0:
            win = False
            keepGoing = False
            
        #all bricks hit
        elif len(brickSprites) == 0:
            win = True
            keepGoing = False
            
            
        #determines if game is over and displays the appropriate screen    
        if keepGoing == False and continue_game == True:
            pygame.mixer.music.fadeout(5)
            #win screen
            if win == True:
                win_sound.play(0)
                winlosetext.set_text("YOU WIN!", YELLOW)
            #lose screen
            else:
                lose_sound.play(0)
                winlosetext.set_text("GAME OVER", RED)
        
        #R - Refresh
            
        ingameSprites.clear(screen, background)
        ingameSprites.update()
        ingameSprites.draw(screen)
        
        pygame.display.flip()
    
    #shows the end screen
    if continue_game == True:
        endTextSprites.update()
        endTextSprites.draw(screen)
        pygame.display.flip()
    
        if win == True:
            pygame.time.delay(5000)
        else:
            pygame.time.delay(22000)
            
    pygame.mouse.set_visible(True)
    
    #clears screen for high score screen
    ingameSprites.clear(screen, background)
    endTextSprites.clear(screen, background)
        
    return continue_game, scorekeeper.get_score(), scorekeeper.get_lives()
        


def menu_screen(background):
    '''This function displays the start-up screen and all the menus. It takes
    the background as a parameter. It then returns the difficulty, the number of 
    players and whether the use exited the game or not'''
    
    #E - Entities
    mouse = menuSprites.Mouse()
    
    #Start-up Screen 
    title = menuSprites.Flickering_Text(screen, "Break Out!", "airstrike.ttf", 60, 100, [GREEN, GREEN2])
    press_enter = menuSprites.Flickering_Text(screen, "PRESS ENTER TO START", "DS-DIGI.ttf", 30, 450, [WHITE, GREY])
    
    #Main Screen Options
    singleplayer = menuSprites.Options(screen, "One Player", 190)
    multiplayer = menuSprites.Options(screen, "Two Player", 235)
    highscores = menuSprites.Options(screen, "High Scores", 280)
    quitgame = menuSprites.Options(screen, "Quit Game", 325)
    main_options = [singleplayer, multiplayer, highscores, quitgame]
    
    #Back Button
    back = menuSprites.Options(screen, "back", 425)
    
    #Difficulty Settings
    easy = menuSprites.Options(screen, "easy", 235)
    medium = menuSprites.Options(screen, "medium", 280)
    hard = menuSprites.Options(screen,"hard", 325)
    
    difficulty_options = [easy, medium, hard, back]
    
    #High Score Listings
    easy_top = menuSprites.HighScores(screen, 235, "easy")
    medium_top = menuSprites.HighScores(screen, 280, "medium")
    hard_top = menuSprites.HighScores(screen, 325, "hard")
    
    high_score_list = [easy_top, medium_top, hard_top]
    
    #Groups
    start_screen_group = pygame.sprite.Group(mouse, title, press_enter)
    
    #Main Screen Groups
    main_screen_group = pygame.sprite.Group(mouse, title, main_options)
    main_options_group = pygame.sprite.Group(main_options)
    
    #Difficulty Screen Groups
    difficulty_group = pygame.sprite.Group(mouse, title, difficulty_options)
    difficulty_options_group = pygame.sprite.Group(difficulty_options)
    
    #High Score Groups
    high_scores_group = pygame.sprite.Group(mouse, title, high_score_list, back)
    high_scores_options_group = pygame.sprite.Group(back)
    
    #screens and options lists
    screens = [start_screen_group, main_screen_group, difficulty_group, high_scores_group]
    options = [main_options_group, difficulty_options_group, high_scores_options_group]
    options_list = [main_options, difficulty_options, [back]]
    
    #Menu Audio
    
    pygame.mixer.music.load("Virtual is Where We Live.wav")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)
    
    #A - Action
    
        #A - Assign values to variables
    clock = pygame.time.Clock()
    keepGoing = True
    flicker_timer = 0
    to_change_screen = 0
    play_game = True
    player_count = 1
    difficulty = "easy"
    current_screen = 0
    option = 0

        #L - Loop
    while keepGoing:
        
        #T - Timer
        clock.tick(30)
        
        #E - Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                play_game = False
            if event.type == pygame.KEYDOWN:
                if current_screen == 0 and event.key == pygame.K_RETURN:
                    to_change_screen = 1
                    start_screen_group.clear(screen, background)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen > 0:
                    if pygame.sprite.spritecollide(mouse, options[current_screen-1], False):
                        #gets what the text is
                        option = pygame.sprite.spritecollide(mouse, options[current_screen-1], False)[0].get_text()
                        #chooses number of players
                        if option == "One Player" or option == "Two Player":
                            if option == "One Player":
                                player_count = 1
                            else:
                                player_count = 2
                            #sends to difficulty screen
                            to_change_screen = 2
                        
                        #sends to high score screen
                        elif option == "High Scores":
                            to_change_screen = 3
                        
                        #stop application                            
                        elif option == "Quit Game":
                            keepGoing = False
                            play_game = False
                            
                        #goes back to main menu
                        elif option == "back":
                            to_change_screen = 1
                        
                        #difficulty is chosen; stops menu and goes to game
                        else:
                            difficulty = option
                            keepGoing = False
                        
        #checks if screen is not the start-up screen
        if current_screen > 0:
            #goes through buttons on screen
            for button in range(len(options_list[current_screen - 1])):
                #if the mouse is on the button, it enlarges and brightens text
                if mouse.rect.colliderect(options_list[current_screen-1][button].rect):
                    options_list[current_screen-1][button].hover_on()
                #if the mouse is not, it shrinks and darkens text
                else:
                    options_list[current_screen-1][button].hover_off()
        
        #timer for how often the title and the press enter texts flicker
        flicker_timer += 1
        if flicker_timer == 1 or flicker_timer == 16:
            title.flicker(flicker_timer)
            if current_screen == 0:
                press_enter.flicker(flicker_timer)
        
        #resets flicker_timer every second
        if flicker_timer == 30:
            flicker_timer = 0
            
        #clears all existing screens 
        for dif_screen in screens:
            dif_screen.clear(screen, background)
            
        #changes to the next screen if it is different
        current_screen = to_change_screen
        
        #R - Refresh
        screens[current_screen].clear(screen, background)
        screens[current_screen].update()
        screens[current_screen].draw(screen)
    
        pygame.display.flip()
    
    pygame.mixer.music.fadeout(50)
    pygame.time.delay(50)
    
    #clears screen for actual game
    screens[current_screen].clear(screen, background)
    
    return play_game, player_count, difficulty


def determine_high_score(score, lives, difficulty):
    '''This function determines if the player has beaten the previous high score. It takes the score,
    the lives remaining, and the difficulty as parameters. It then compares the scores,
    and if the player won the game, all the remaining lives added in, and compares it 
    with the respective winner in that difficulty. If the player has the new high
    score, it returns that the player is the new champ, and if not, it returns that 
    the champion still reigns and their score'''
    
    beat_it = False
    
    #tests if high score file exists
    try:
        high_score_file = open(difficulty+".txt", 'r')
        line = high_score_file.readline().strip()
        old_score = int(line.split()[1])
        if score >= old_score:
            beat_it = True
        
    except IOError:
        beat_it = True
        
    if beat_it == True:
        return beat_it, ""
    
    else:
        return beat_it, line
    
def high_score_screen(score, lives, difficulty, background):
    '''This function takes in 4 parameters, the score, the lives remaining, the 
    difficulty, and the background. It runs the determine_high_score function
    and takes the results from it. It then displays the high score screen. If the user
    has the new high score, it prompts them to enter in their name to be stored.
    This function returns whether or not the application is still running or not.'''
    
    #E - Entities
    
    #the function and if/else statement determine what will be in the labels
    top_points, current_top = determine_high_score(score, lives, difficulty)
    
    #if the user has the new high score
    if top_points == True:
        first_line = "High Score!"
        second_line = "Enter Name:"
        third_line = ""
    
    #if the user doesn't have the new high score
    else:
        first_line = "Try Again!"
        second_line = "High Score:"
        third_line = current_top + " points"
    
    mouse = menuSprites.Mouse()
    
    #text
    top_heading = menuSprites.Label(screen, first_line, 70, 120)
    middle_line = menuSprites.Label(screen, second_line, 40, 250)
    last_line = menuSprites.Label(screen, third_line, 50, 300)
    
    done = menuSprites.Options(screen, "done", 425)
    
    allSprites = pygame.sprite.Group(mouse, top_heading, middle_line, last_line, done)
    
    #A - Action
        #A - Assigning values to variables
    clock = pygame.time.Clock()
    keepGoing = True
    restart_game = True
    shift_down = False
    
        #L - Loop
    while keepGoing:
        #T - Timer
        clock.tick(30)
        #E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                restart_game = False
                
            #name input for new high score winner
            if top_points == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        shift_down = True
                    last_line.set_text(pygameTyper.pygame_typer(last_line.get_text(), event.key, shift_down))
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        shift_down = False
                        
            #returns to menu screen
            if event.type == pygame.MOUSEBUTTONDOWN and mouse.rect.colliderect(done.rect):
                keepGoing = False
                
        #updates high score file        
        if keepGoing == False and restart_game == True and top_points == True:
            update_file = open(difficulty + ".txt", 'w')
            update_file.write(last_line.get_text() + "  " + str(score) )
        
        #R - Refresh
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
        
    #clears screen for menu
    allSprites.clear(screen, background)
    return restart_game
    
main()
