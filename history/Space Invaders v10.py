# Version 10

import sys, pygame, time

# Globals
TITLE="Space Invaders"
SCREEN_HEIGHT=540
SCREEN_WIDTH=960
FPS=60

TILE_HEIGHT=64
TILE_WIDTH=64

#Colours
BLACK=(0,0,0)
WHITE=(255,255,255)

# Sounds
SOUND_FROG_JUMP='ring.wav'

# Layout
SCORE_HEIGHT=32
GAME_TOP=SCORE_HEIGHT
SCORE_TOP=0
SCORE_LEFT=0
SCORE_WIDTH=SCREEN_WIDTH
SCORE_HEIGHT=30


# Graphics
GRAPHIC_GUN= 'Graphics\Gun.png'
GRAPHIC_BULLET= 'Graphics\Bullet.png'
GRAPHIC_ALIEN1= 'Graphics\Alien1 First position.png'
GRAPHIC_ALIEN1_SECOND= 'Graphics\Alien1 Second position.png'
GRAPHIC_ALIEN2= 'Graphics\Alien2 First position.png'
GRAPHIC_ALIEN2_SECOND='Graphics\Alien2 Second position.png'
GRAPHIC_ALIEN3= 'Graphics\Alien3 First position.png'
GRAPHIC_ALIEN3_SECOND= 'Graphics\Alien3 Second position.png'
GRAPHIC_SPACESHIP= 'Graphics\Alien Spaceship.png'

# Speeds
GUN_SPEED=3
BULLET_SPEED=3
BULLET_DELAY=0.5
ANIMATION_DELAY=0.5
SPACESHIP_DELAY=10
SPACESHIP_SPEED=2

# Placement
ALIEN_COLUMNS=12
ALIEN_ROWS=5
ALIEN_SPACING_X=60
ALIEN_SPACING_Y=50
ALIEN_TOP_OFFSET=50

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
# class:  Bullet
#-------------------------------------------------------   
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_BULLET)
        self.rect=self.image.get_rect()
        self.rect.left=(SCREEN_WIDTH-self.rect.width)/2
        self.rect.top=(SCREEN_HEIGHT-self.rect.height)
        
    def set_position(self,x,y):
        self.rect.left=x
        self.rect.top=y
        
    def update(self):
        self.rect.top=self.rect.top-BULLET_SPEED
        if self.rect.top<GAME_TOP:
            self.kill()



#-------------------------------------------------------
# class:  Alien
#-------------------------------------------------------
class Alien(pygame.sprite.Sprite):

    direction='R'
    
    def __init__(self):
        super().__init__()
        
    def set_position(self,x,y):
        self.rect.centerx=x
        self.rect.centery=y

    def update(self):
        if self.direction=='L':
            self.rect.left=self.rect.left-1
        if self.direction=='R':
            self.rect.left=self.rect.left+1

    def change_direction(self):
        if self.direction=='R':
            self.direction='L'
        else:
            self.direction='R'
            
    def change_image(self):
        if self.image==self.image1:
            self.image=self.image2
        else:
            self.image=self.image1

    def get_score(self):
        return self.score


#-------------------------------------------------------
# class:  Alien1
#-------------------------------------------------------
class Alien1(Alien):

    score=10
    
    def __init__(self):
        super().__init__()
        self.image1=pygame.image.load(GRAPHIC_ALIEN1)
        self.image2=pygame.image.load(GRAPHIC_ALIEN1_SECOND)
        self.image=self.image1
        self.rect=self.image.get_rect()





#-------------------------------------------------------
# class:  Alien2
#-------------------------------------------------------
class Alien2(Alien):

    score=20
    
    def __init__(self):
        super().__init__()
        self.image1=pygame.image.load(GRAPHIC_ALIEN2)
        self.image2=pygame.image.load(GRAPHIC_ALIEN2_SECOND)
        self.image=self.image1       
        self.rect=self.image.get_rect()

                



#-------------------------------------------------------
# class:  Alien3
#-------------------------------------------------------
class Alien3(Alien):

    score=30

    def __init__(self):
        super().__init__()
        self.image1=pygame.image.load(GRAPHIC_ALIEN3)
        self.image2=pygame.image.load(GRAPHIC_ALIEN3_SECOND)
        self.image=self.image1
        self.rect=self.image.get_rect()


#------------------------------------------------------
# class: Alien_swarm
#------------------------------------------------------
class Alien_swarm():
    
    last_animation_time=time.time()-1 # Putting this in the past means we can create a new bullet imediately

    all_invaders=pygame.sprite.Group()
    direction='R'
    
    def _init_(self):
        self.direction='R'
        self.all_invaders = pygame.sprite.Group()

    def update(self):
        self.check_for_screen_edge()
        self.check_for_animation_time()
        

    # Check for screen edge
    
    def check_for_screen_edge(self):

            
        change_direction=False
                
        for alien in self.all_invaders:
            if alien.rect.left<0:
                change_direction=True
            if alien.rect.right>SCREEN_WIDTH:
                change_direction=True

        if change_direction==True:
            for alien in self.all_invaders:
                alien.change_direction()

    def add(self,alien):
        self.all_invaders.add(alien)

    def check_for_animation_time(self):
        if time.time()>self.last_animation_time+ANIMATION_DELAY:
            for alien in self.all_invaders:
                alien.change_image()

            self.last_animation_time=time.time()
            
    def check_for_collisions(self,bullets):
        result=0
        pygame.sprite.groupcollide
        for bullet in bullets:
            hits=pygame.sprite.spritecollide(bullet,self.all_invaders,False)
            for hit in hits:
                hit.kill()
                bullet.kill()
                result+=hit.get_score()
    
        return result    
            


#-------------------------------------------------------
# class: Spaceship
#-------------------------------------------------------
class Spaceship(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_SPACESHIP)
        self.rect=self.image.get_rect()
        self.rect.left=SCREEN_WIDTH
        self.rect.top=GAME_TOP

    def update(self):
        self.rect.left=self.rect.left-SPACESHIP_SPEED
        if self.rect.right<1:
            self.kill()
        if self.rect.left>SCREEN_WIDTH:
            self.kill()

#-------------------------------------------------------
# class: Score
#-------------------------------------------------------
class Score(pygame.sprite.Sprite):
    

    def __init__(self):
        super().__init__()
        self.rect=pygame.Rect(SCORE_LEFT,SCORE_TOP,SCORE_WIDTH,SCORE_HEIGHT)
        self.score=0
        self.Draw_score()

    def Add(self,delta):
        self.score=self.score+delta
        self.Draw_score()
        

    def Draw_score(self):
        font = pygame.font.SysFont("comicsansms", 16,bold=True,italic=True)
        text='SCORE {:06d}'.format(self.score)
        self.image = font.render(text, True, WHITE)

    





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
    
    last_bullet_time=time.time()-1 # Putting this in the past means we can create a new bullet imediately

    last_spaceship_time=time.time()

    def __init__(self):

        self.game_state=GameState.GAME_NOT_STARTED
        
        # Create a sound player
        self.audio=Audio()
        
        # All sprites in the game must be added to this list
        self.all_sprites = pygame.sprite.Group()
        self.all_shelters = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()

        # Create Score
        self.score=Score()
        self.all_sprites.add(self.score)

 
        # Create Gun
        self.gun=Gun()
        self.all_sprites.add(self.gun)


        # Create Alien_swarm
        self.alien_swarm=Alien_swarm()

        
        for row in range(4,6):
            for col in range(1,ALIEN_COLUMNS+1):
                alien1=Alien1()
                self.all_sprites.add(alien1)
                self.alien_swarm.add(alien1)
                alien1.set_position(col*ALIEN_SPACING_X,row*ALIEN_SPACING_Y+ALIEN_TOP_OFFSET)

        for row in range(2,4):
            for col in range(1,ALIEN_COLUMNS+1):
                alien2=Alien2()
                self.all_sprites.add(alien2)
                self.alien_swarm.add(alien2)
                alien2.set_position(col*ALIEN_SPACING_X,row*ALIEN_SPACING_Y+ALIEN_TOP_OFFSET)

        for row in range(1,2):
            for col in range(1,ALIEN_COLUMNS+1):
                alien3=Alien3()
                self.all_sprites.add(alien3)
                self.alien_swarm.add(alien3)
                alien3.set_position(col*ALIEN_SPACING_X,row*ALIEN_SPACING_Y+ALIEN_TOP_OFFSET)
        
            
        
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
                if(event.key==pygame.K_SPACE):
                    self.create_bullet()
               
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
            self.alien_swarm.update()

            # Alien spaceship time
            if time.time()>self.last_spaceship_time+SPACESHIP_DELAY:
                self.spaceship=Spaceship()
                self.all_sprites.add(self.spaceship)
                self.last_spaceship_time=time.time()
            
            # Move all the sprites
            self.all_sprites.update()
                
            # Check for collisions
            x=self.alien_swarm.check_for_collisions(self.all_bullets)      
            self.score.Add(x)
 
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

    # Create Bullet
    def create_bullet(self):
        if self.last_bullet_time<time.time()-BULLET_DELAY:
            bullet=Bullet()
            bullet.set_position(self.gun.rect.centerx-bullet.rect.width/2,self.gun.rect.top)
            self.all_sprites.add(bullet)
            self.all_bullets.add(bullet)
            self.last_bullet_time=time.time()
    


    
# The main function - You should never need to change this.
def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
 
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption(TITLE)
#   pygame.mouse.set_visible(False)
 
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
