# Version 16

import sys, pygame, time, random

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
HEADER_HEIGHT=32
GAME_TOP=HEADER_HEIGHT
SCORE_TOP=0
SCORE_LEFT=0
SCORE_WIDTH=SCREEN_WIDTH/2
SCORE_HEIGHT=HEADER_HEIGHT
LIVES_TOP=0
LIVES_LEFT=SCREEN_WIDTH/2
LIVES_WIDTH=SCREEN_WIDTH/2
LIVES_HEIGHT=HEADER_HEIGHT

# Game behaviour
MAX_LIVES=3

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
GRAPHIC_MISSILE_CROSS= 'Graphics\Missile_Cross.png'
GRAPHIC_MISSILE_STRAIGHT= 'Graphics\Missile_Straight.png'
GRAPHIC_MISSILE_ZIGZAG= 'Graphics\Missile_Zigzag.png'
GRAPHIC_MISSILE_SPACESHIP= 'Graphics\Missile_Spaceship.png'

# Delays
BULLET_DELAY=0.5
ANIMATION_DELAY=0.5
SPACESHIP_DELAY=25

# Raw speeds (pixels per second)
RAW_GUN_SPEED=180
RAW_BULLET_SPEED=240
RAW_MISSILE_SPEED=120
RAW_SPACESHIP_SPEED=60 # to do, normal speed is 120

# Speeds (pixels per frame)
GUN_SPEED=RAW_GUN_SPEED/FPS
BULLET_SPEED=RAW_BULLET_SPEED/FPS
MISSILE_SPEED=RAW_MISSILE_SPEED/FPS
SPACESHIP_SPEED=RAW_BULLET_SPEED/FPS


# Alien movements
ALIEN_JUMP_FRAME_COUNT=FPS/10 # usually 5... ish
ALIEN_JUMP_SIZE=10

# Placement
ALIEN_COLUMNS=12
ALIEN_ROWS=5
ALIEN_SPACING_X=60
ALIEN_SPACING_Y=50
ALIEN_TOP_OFFSET=50

# Other
MISSILE_CHANCE_PER_SECOND=3/2500

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
    row=0
    direction='R'
    all_sprites=None
    
    def __init__(self):
        super().__init__()
        self.alien_below=None

    def update (self):
        if self.alien_below is None:
            if random.random()< MISSILE_CHANCE_PER_SECOND:
                missile=MissileCross()
                missile.set_position(self.rect.x,self.rect.y)
                Alien.all_sprites.add(missile)

    def set_row(self,row):
        self.row=row
 
    def set_position(self,x,y):
        self.rect.centerx=x
        self.rect.centery=y

    def move_if_in_row(self,row):
        if self.row==row:
            if self.direction=='L':
                self.rect.left=self.rect.left-ALIEN_JUMP_SIZE
            if self.direction=='R':
                self.rect.left=self.rect.left+ALIEN_JUMP_SIZE
            if self.direction=='D':
                self.rect.bottom=self.rect.bottom+ALIEN_SPACING_Y

            self.change_image()

    def change_direction(self,direction):
        self.direction=direction
            
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
    current_row=5
    frame_count=0
    moving_down=False
    
    def _init_(self):
        self.direction='R'
        self.current_row=5
        self.all_invaders = pygame.sprite.Group()
        self.frame_count=0
        self.moving_down=False

    def update(self):
        self.frame_count+=1
        
        # Check if it is time to move the aliens
        
        if self.frame_count==ALIEN_JUMP_FRAME_COUNT:
            for alien in self.all_invaders:
                alien.move_if_in_row(self.current_row)
            self.current_row=self.current_row-1
            if self.current_row==0:
                self.current_row=5
                self.check_for_screen_edge()
            self.frame_count=0
        

    # Check for screen edge
    
    def check_for_screen_edge(self):
      
        change_direction=False
                
        for alien in self.all_invaders:
            if alien.rect.left<0:
                change_direction=True
            if alien.rect.right>SCREEN_WIDTH:
                change_direction=True

        if change_direction==True:
            if self.moving_down:
                if self.direction=='L':
                    self.direction='R'
                else:
                    self.direction='L'
                    
                for alien in self.all_invaders:
                    alien.change_direction(self.direction)
                    self.moving_down=False
            else:        
                for alien in self.all_invaders:
                    alien.change_direction('D')
                    self.moving_down=True

    def add(self,alien):
        self.all_invaders.add(alien)

    # Check for collisions
            
    def check_for_collisions(self,bullet):
        result=0
        #pygame.sprite.groupcollide
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

    #new_direction=''

    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_SPACESHIP)
        self.rect=self.image.get_rect()
        self.rect.left=SCREEN_WIDTH
        self.rect.top=GAME_TOP
        self.score=100

    def set_direction(self,new_direction):
        self.direction=new_direction
        
        if new_direction=='R':
            self.rect.right=0
        else:
            self.rect.left=SCREEN_WIDTH
        

    def update(self):
        if self.direction=='L':
            self.rect.left=self.rect.left-SPACESHIP_SPEED
        else:
             self.rect.left=self.rect.left+SPACESHIP_SPEED
             
        if self.rect.right<1:
            self.kill()
        if self.rect.left>SCREEN_WIDTH:
            self.kill()

    def get_score(self):
        return self.score



#-------------------------------------------------------
# class: Missile
#-------------------------------------------------------
class Missile(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()

    def set_position(self,x,y):
        self.rect.left=x
        self.rect.top=y
        
    def update(self):
        self.rect.top=self.rect.top+MISSILE_SPEED
        if self.rect.top>SCREEN_HEIGHT:
            self.kill()
    
#-------------------------------------------------------
# class: MissileCross
#-------------------------------------------------------
class MissileCross(Missile):
    
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_MISSILE_CROSS)
        self.rect=self.image.get_rect()

#-------------------------------------------------------
# class: MissileStraight
#-------------------------------------------------------
class MissileStraight(Missile):
    
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_MISSILE_STRAIGHT)
        self.rect=self.image.get_rect()


#-------------------------------------------------------
# class: MissileZigzag
#-------------------------------------------------------
class MissileZigzag(Missile):
    
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_MISSILE_ZIGZAG)
        self.rect=self.image.get_rect()


#-------------------------------------------------------
# class: MissileSpaceship
#-------------------------------------------------------
class MissileSpaceship(Missile):
    
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(GRAPHIC_MISSILE_SPACESHIP)
        self.rect=self.image.get_rect()



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
# class: Lives
#-------------------------------------------------------
class Lives(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect=pygame.Rect(LIVES_LEFT,LIVES_TOP,LIVES_WIDTH,LIVES_HEIGHT)
        self.lives=MAX_LIVES
        self.Draw_lives()

    def lose_life(self):
        self.lives=self.lives-1

    def Draw_lives(self):
        font = pygame.font.SysFont("comicsansms", 16,bold=True,italic=True)
        text='LIVES {:01d}'.format(self.lives)
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
    

    last_spaceship_time=time.time()

    next_spaceship_direction='L'

    def __init__(self):

        self.game_state=GameState.GAME_NOT_STARTED
        
        # Create a sound player
        # Self.audio=Audio()
        
        # All sprites in the game must be added to this list
        self.all_sprites = pygame.sprite.Group()
        self.all_shelters = pygame.sprite.Group()
        Alien.all_sprites=self.all_sprites

        # Create Score
        self.score=Score()
        self.all_sprites.add(self.score)

        # Create Lives
        self.lives=Lives()
        self.all_sprites.add(self.lives)

        # Create Gun
        self.gun=Gun()
        self.all_sprites.add(self.gun)


        # Create Bullet
        self.bullet=Bullet()


        # Create Alien_swarm
        self.alien_swarm=Alien_swarm()

        # temporary for testing
        self.missilecross=MissileCross()
        self.all_sprites.add(self.missilecross)
        self.missilecross.set_position(SCREEN_WIDTH/2,0)

        # Create Spaceship
        self.spaceship=Spaceship()


        # Create Aliens
        for col in range(1,ALIEN_COLUMNS+1):
            previous_alien=None
            for row in range(5,0,-1):
                if row in range (1,2):
                    alien=Alien3()
                if row in range (2,4):
                    alien=Alien2()
                if row in range (4,6):
                    alien=Alien1()
            
                self.all_sprites.add(alien)
                self.alien_swarm.add(alien)
                alien.set_position(col*ALIEN_SPACING_X,row*ALIEN_SPACING_Y+ALIEN_TOP_OFFSET)
                alien.set_row(row)
                if previous_alien is not None:
                    alien.alien_below=previous_alien
                previous_alien=alien           
        
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

            # Alien spaceship time also creating a spaceship
            if time.time()>self.last_spaceship_time+SPACESHIP_DELAY:
                self.spaceship=Spaceship()

                print('1) Its spaceship time, self.next_spaceship_direction=',self.next_spaceship_direction)

                self.spaceship.set_direction(self.next_spaceship_direction)
                if self.next_spaceship_direction=='R':
                    self.next_spaceship_direction='L'
                else:
                    self.next_spaceship_direction='R'

                print('2) direction should have chnaged, self.next_spaceship_direction=',self.next_spaceship_direction)
                
                self.all_sprites.add(self.spaceship)
                self.last_spaceship_time=time.time()
                
            
            # Move all the sprites
            self.all_sprites.update()
                
            # Check for collisions in alien swarm
            if self.bullet.alive():
                x=self.alien_swarm.check_for_collisions(self.bullet)      
                self.score.Add(x)

            # Check for collisions with spaceship
            if self.bullet.alive() and self.spaceship.alive():
                hits=pygame.sprite.spritecollide(self.bullet,pygame.sprite.GroupSingle(self.spaceship),False)
                for hit in hits:
                    hit.kill()
                    self.bullet.kill()
                    self.score.Add(hit.get_score())


 
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

    # Create Bullet function
    def create_bullet(self):
        if not self.bullet.alive():
            self.bullet.set_position(self.gun.rect.centerx-self.bullet.rect.width/2,self.gun.rect.top)
            self.all_sprites.add(self.bullet)
    
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
