import pygame
 
#paddle class definition

class Padle:

	def __init__(self,x,y,moveupkey, movedownkey):
		self.x = x
		self.y = y
		self.moveupkey = moveupkey
		self.movedownkey = movedownkey

	def goup (self):
		self.y  -= 3

	def godown (self):
		self.y  += 3

	def movement(self):
		if pygame.key.get_pressed()[self.moveupkey]: self.goup()
		if pygame.key.get_pressed()[self.movedownkey]: self.godown()


class Ball:
	def __init__(self, x, y):
		self.x = x
		self.y = y

#Parameter Inialization

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False
Padleleft = Padle(20,135, pygame.K_UP, pygame.K_DOWN)
Padleright = Padle(380,135, pygame.K_LEFT, pygame.K_RIGHT)
Ball = Ball(200,150)


clock = pygame.time.Clock()

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
                        done = True

	Padleleft.movement()
	Padleright.movement()

	screen.fill((0, 0, 0))
	pygame.draw.rect(screen, (255,255,255), pygame.Rect(Padleleft.x, Padleleft.y, 10, 30))                    
	pygame.draw.rect(screen, (255,255,255), pygame.Rect(Padleright.x, Padleright.y, 10, 30))                    
	pygame.draw.circle(screen, (255,255,255), (Ball.x, Ball.y), 5)
	pygame.display.flip()
	clock.tick(60)