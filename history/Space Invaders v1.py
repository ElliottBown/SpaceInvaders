# Version 1

import sys, pygame

# Globals
TITLE="Space Invaders"
SCREEN_HEIGHT=600
SCREEN_WIDTH=64*11
FPS=30

TILE_HEIGHT=64
TILE_WIDTH=64

#Colours
BLACK=(0,0,0)
WHITE=(255,255,255)

# Sounds
SOUND_FROG_JUMP='ring.wav'


# Graphics

GRAPHIC_BUSH= 'bush.png'
GRAPHIC_HOME= 'home.png'
GRAPHIC_FROG= 'frog2.png'
GRAPHIC_GUN= 'Graphics\Gun.png'
GUN_SPEED=1

#-------------------------------------------------------
# class:  Gun
#-------------------------------------------------------
class Gun(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_GUN)
        self.rect=self.image.get_rect()
        self.rect.left=(SCREEN_WIDTH-self.rect.width)/2
        self.rect.top=(SCREEN_HEIGHT-self.rect.height)

    def update(self):
        """ Update the bat location if required. """
        # Get a list of all keys currently pressed
        pressed = pygame.key.get_pressed()

        # move left or right if the left or right keys are pressed
        if pressed[pygame.K_LEFT]:
            self.rect=self.rect.move([-GUN_SPEED,0])
            
        if pressed[pygame.K_RIGHT]:
            self.rect=self.rect.move([GUN_SPEED,0])
            

        # Stop the gun going off the screen
        if (self.rect.left<0): self.rect.left=0
        if (self.rect.right>SCREEN_WIDTH): self.rect.right=SCREEN_WIDTH

#-------------------------------------------------------
# class:  Frog
#-------------------------------------------------------
class Frog(pygame.sprite.Sprite):
    """ The frog """
    jump_size=36
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_FROG)
        self.rect=self.image.get_rect()
        self.rect.left=(SCREEN_WIDTH-self.rect.width)/2
        self.rect.top=(SCREEN_HEIGHT-self.rect.height)
        
    def jump(self,direction):
        if direction=='u':
            self.rect.top=self.rect.top-self.jump_size
        if direction=='d':
            self.rect.top=self.rect.top+self.jump_size
        if direction=='l':
            self.rect.left=self.rect.left-self.jump_size
        if direction=='r':
            self.rect.left=self.rect.left+self.jump_size
    def update(self):

        # Stop the frog going off the screen
        if (self.rect.left<0): self.rect.left=0
        if (self.rect.right>SCREEN_WIDTH): self.rect.right=SCREEN_WIDTH
        
#-------------------------------------------------------
# class: Ball
#-------------------------------------------------------
class Ball(pygame.sprite.Sprite):
    """ The ball """
    # called once when the sprite is created
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_BALL)
        self.rect=self.image.get_rect()
        self.rect.left=(SCREEN_WIDTH-self.rect.width)/2
        self.rect.top=(SCREEN_HEIGHT-self.rect.height)-50
        self.speed = BALL_SPEED

    # called once per frame to get the ball to move itself
    def update(self):
        """ Update the ball location. """
        self.rect=self.rect.move(self.speed)

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0: # we don't need to bounce at the bottom because the game will have ended
            self.speed[1] = -self.speed[1]

    # Reverses the y direction of the ball
    # This is called when the ball hits the bat
    def reverse_y(self):
        self.speed[1]=-self.speed[1]


#-------------------------------------------------------
# class: Bush
#-------------------------------------------------------
class Bush(pygame.sprite.Sprite):
    """ A square of bush """

    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_BUSH)
        self.rect=self.image.get_rect()
        self.rect.left=(SCREEN_WIDTH-self.rect.width)/2
        self.rect.top=(SCREEN_HEIGHT-self.rect.height)/2

#    def update(self):

    

    def SetPos(self,x,y):
        """ Position is from top left, starting at 1,1 """
        self.rect.left=self.rect.width*(x-1)
        self.rect.bottom=self.rect.height*y


#-------------------------------------------------------
# class: Home
#-------------------------------------------------------
class Home(pygame.sprite.Sprite):
    """ A square of bush """

    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_HOME)
        self.rect=self.image.get_rect()
        self.rect.left=(SCREEN_WIDTH-self.rect.width)/2
        self.rect.top=(SCREEN_HEIGHT-self.rect.height)/2

#    def update(self):

    

    def SetPos(self,x,y):
        """ Position is from top left, starting at 1,1 """
        self.rect.left=self.rect.width*(x-1)
        self.rect.bottom=self.rect.height*y


#-------------------------------------------------------
# class: Audio
#-------------------------------------------------------
class Audio:
 
    FROG_JUMP=1

    def __init__(self):
        self.sound_frog_jump=pygame.mixer.Sound('ring.wav')
    
    def play_sound(self,sound_id):
        if (sound_id==Audio.FROG_JUMP):
            self.sound_frog_jump.play()


#-------------------------------------------------------
# class: Game_State
#-------------------------------------------------------
class GameState:
    # Game states
    GAME_NOT_STARTED = 0
    GAME_RUNNING     = 1
    GAME_OVER        = 2

#-------------------------------------------------------
# class: Game
#-------------------------------------------------------
class Game(object):
    """ Represents the logic of the game """

    LEVEL_ROWS=9
    LEVEL_COLS=17

    levels=('                 '
            '                 '
            'BBBBBBBBBBBBBBBBB'
            'BBBBBBBYYYBBBBBBB'
            'BBBBBBYPYYBYBBBBB'
            'BBBBBBYYYYYYBBBBB'
            'BBBBBBYYYYBYBBBBB'
            'BBBBBBBYYBBBBBBBB'
            'BBBBBBBBBBBBBBBBB')

    def __init__(self):

        self.game_state=GameState.GAME_NOT_STARTED
        
        # Create a sound player
        self.audio=Audio()
        
        # All sprites in the game must be added to this list
        self.all_sprites = pygame.sprite.Group()
        self.all_invaders = pygame.sprite.Group()
        self.all_shelters = pygame.sprite.Group()

        
        #create Gun

        self.gun=Gun()

        self.all_sprites.add(self.gun)
        
    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():

            # Events handled in all states
            if event.type == pygame.QUIT:
                return True
            if event.type==pygame.KEYDOWN:
                if(event.key==pygame.K_ESCAPE):
                    return True
               
            # Events handled in GAME_RUNNING

            # None
                
            # Events handled in GAME_NOT_STARTED  
            if self.game_state==GameState.GAME_NOT_STARTED:
                if event.type==pygame.KEYDOWN:
                    self.game_state=GameState.GAME_RUNNING
                    
            # Events handled in GAME_NOT_STARTED  
            if self.game_state==GameState.GAME_OVER:
                if event.type==pygame.KEYDOWN:
                    self.__init__()
                             
        return False

 
    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if self.game_state==GameState.GAME_RUNNING:
            # Move all the sprites
            self.all_sprites.update()
           
                                                                               

            
                
 
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(BLACK)

        if self.game_state==GameState.GAME_NOT_STARTED:
            font = pygame.font.SysFont("comicsansms", 36,bold=True,italic=True)
            text = font.render("Press a key to start game", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if self.game_state==GameState.GAME_RUNNING:
            self.all_sprites.draw(screen)
 
        if self.game_state==GameState.GAME_OVER:
            font = pygame.font.SysFont("comicsansms", 36,bold=True,italic=True)
            text = font.render("Game Over, press a key", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
 
        # Flip makes all the stuff we have drawn actually appear on the screen
        pygame.display.flip()


# The main function - You should never need to change this.
def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
 
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption(TITLE)
#    pygame.mouse.set_visible(False)
 
    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()
 
    # Create an instance of the Game class
    game = Game()
 
    # Main game loop
    while not done:
 
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
 
        # Update object positions, check for collisions
        game.run_logic()
 
        # Draw the current frame
        game.display_frame(screen)
 
        # Pause for the next frame
        clock.tick(FPS)

    # Close window and exit
    pygame.quit()
    sys.exit()

#-------------------------------------------------------
# This is where the program actually starts
#-------------------------------------------------------

# Call the main function, start up the game
if __name__ == "__main__":
    main()
