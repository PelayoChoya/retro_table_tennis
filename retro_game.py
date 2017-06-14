import pygame
import operator
import random
import neuralnetwork


# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

random_height = ('UP','DOWN','NONE')

class Border(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
 
        # Call the parent class (Sprite) constructor
        super(Border,self).__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()


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
    
    def neuralnet_movement ( self , dir):

        if dir == -1 and (self.rect.y < 269): self.rect.y += 3
        elif dir == 1 and (self.rect.y > 1):self.rect.y -= 3
        elif dir == 0: self.rect.y += 0

class Ball(pygame.sprite.Sprite):

    def __init__(self,color):
        super(Ball,self).__init__()
 
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, color, (5, 5), 5, 0)
        self.rect = self.image.get_rect()
        self.direction = 'right'
        self.height = 'NONE'
    
    def change_direction(self, height):
        
        if self.direction == 'right':
            self.direction = 'left'
            self.height = height
        elif self.direction == 'left':
            self.direction = 'right'
            self.height = height  
        

    def  border_collision(self):

        if self.height == 'UP': self.height = 'DOWN'
        elif self.height == 'DOWN': self.height = 'UP'

    def movement(self):

        if self.direction == 'right' and self.height == 'NONE' : new_place = tuple(map(operator.add, self.rect.center , ( 2, 0)))
        if self.direction == 'left'  and self.height == 'NONE' : new_place = tuple(map(operator.add, self.rect.center , ( -2, 0)))
        if self.direction == 'right' and self.height == 'DOWN' : new_place = tuple(map(operator.add, self.rect.center , ( 2, 2)))
        if self.direction == 'left'  and self.height == 'DOWN' : new_place = tuple(map(operator.add, self.rect.center , ( -2, 2)))  
        if self.direction == 'right' and self.height == 'UP' : new_place = tuple(map(operator.add, self.rect.center , ( 2, -2)))
        if self.direction == 'left'  and self.height == 'UP' : new_place = tuple(map(operator.add, self.rect.center , ( -2, -2)))      
        self.rect.center = new_place
    
    
        

def collision_place(ballY, PadleY):
    
    return random.choice(random_height)

def velocity_valueX(ball):
    if ball.direction == 'right':
        return 2
    elif ball.direction == 'left':
        return -2 

def velocity_valueY(ball):
    if ball.height == 'NONE':
        return 0
    elif ball.height == 'UP':
        return -2 
    elif ball.height == 'DOWN':
        return 2


# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode([screen_width, screen_height])


border_list = pygame.sprite.Group()
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

upBorder = Border(WHITE, 400, 10)

# Setting the object's position

upBorder.rect.x = 0
upBorder.rect.y = 0

# Add the block to the list of objects
border_list.add(upBorder)
all_sprites_list.add(upBorder)

downBorder = Border(WHITE, 400, 10)

# Setting the object's position

downBorder.rect.x = 0
downBorder.rect.y = 290

# Add the block to the list of objects
border_list.add(downBorder)
all_sprites_list.add(downBorder)

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

pop=[neuralnetwork.Network([5,3]) for i in range(20)]
brain=neuralnetwork.createandtrain(pop,100)

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True

    padle_hit_list = pygame.sprite.spritecollide(ball, padle_list, False)

    if padle_hit_list: 
        ball.change_direction(collision_place(ball.rect.center[0], padleleft.rect.y))
    border_hit_list = pygame.sprite.spritecollide(ball, border_list, False)
    if border_hit_list:
        ball.border_collision()

    # Clear the screen
    screen.fill(BLACK)
    neural_result = brain.output([float(ball.rect.center[0])/400,(1-float(ball.rect.center[1])/300),float(velocity_valueX(ball))*60/300,-float(velocity_valueY(ball))*60/300,(1-float(padleleft.rect.y +15)/300)])
    padleleft.neuralnet_movement(neural_result)
    padleright.movement()
    ball.movement()
    #print padleleft.rect.y

    # Draw all the spites
    all_sprites_list.draw(screen)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    print [float(ball.rect.center[0])/400,(1-float(ball.rect.center[1])/300),float(velocity_valueX(ball))*60/300,-float(velocity_valueY(ball))*60/300,(1-float(padleleft.rect.y +15)/300)]
    print neural_result
    # Limit to 60 frames per second
    clock.tick(60)
    
pygame.quit()