import pygame
import operator


# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)


class Padle(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, color, width, height, movementUpKey, movementDownKey):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
 
        # Call the parent class (Sprite) constructor
        super(Padle,self).__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        self.movementDownKey = movementDownKey
        self.movementUpKey = movementUpKey

    def movement(self):

        if pygame.key.get_pressed()[self.movementDownKey]:self.rect.y += 3
        if pygame.key.get_pressed()[self.movementUpKey]:self.rect.y -= 3

class Ball(pygame.sprite.Sprite):
    
    def __init__(self,color):
        super(Ball,self).__init__()
 
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, color, (5, 5), 5, 0)
        self.rect = self.image.get_rect()
        self.direction = 'right'
    
    def change_direction(self):
        
        if self.direction == 'right':
            self.direction = 'left'
        elif self.direction == 'left':
            self.direction = 'right'  
        

    def movement(self):
        if self.direction == 'right' : new_place = tuple(map(operator.add, self.rect.center , ( 1, 0)))
        if self.direction == 'left' : new_place = tuple(map(operator.add, self.rect.center , ( -1, 0)))    
        self.rect.center = new_place
        

# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode([screen_width, screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
padle_list = pygame.sprite.Group()
 
# This is a list of every sprite. 
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# Creating the objects

padleleft = Padle(WHITE, 10, 30,pygame.K_UP, pygame.K_DOWN)

# Setting the object's position

padleleft.rect.x = 20
padleleft.rect.y = 135

# Add the block to the list of objects
padle_list.add(padleleft)
all_sprites_list.add(padleleft)

padleright = Padle(WHITE, 10, 30,pygame.K_LEFT, pygame.K_RIGHT)

# Setting the object's position

padleright.rect.x = 380
padleright.rect.y = 135

# Add the block to the list of objects
padle_list.add(padleright)
all_sprites_list.add(padleright)

ball_list = pygame.sprite.Group()

ball = Ball(WHITE)

ball.rect.x = 240
ball.rect.y = 150

all_sprites_list.add(ball)
ball_list.add(ball)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True

    hit_list = pygame.sprite.spritecollide(ball, padle_list, False)
    if hit_list: 
        ball.change_direction()
        print ball.direction
        print "yes"
    # Clear the screen
    screen.fill(BLACK)

    padleleft.movement()
    padleright.movement()
    ball.movement()
  

    # Draw all the spites
    all_sprites_list.draw(screen)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()