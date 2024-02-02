import pygame, random, math
from random import randint
from pathlib import Path
from abc import ABC, abstractmethod


WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
#GREEN = (0, 255, 0)
RED = (255,0,0)
#BLUE = (0,0,255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Bumpers")
clock = pygame.time.Clock()
current_path = Path.cwd()
file_path = current_path / 'highscore.txt'

def draw_text1(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_text2(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, BLACK)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def direction(a,b):
	#x,y vector from a to b
	if hasattr(a,'rect'):
		xa = a.rect.centerx
		ya = a.rect.centery
	else:
		xa, ya = a
	if hasattr(b,'rect'):
		xb = b.rect.centerx
		yb = b.rect.centery
	else:
		xb, yb = b
	dx = xb -xa
	dy = yb - ya
	return dx, dy

def distance(a,b):
	#pitagoras distance between a and b
	dx, dy = direction(a,b)
	return (dx**2 + dy**2)**(1/2)

def reflection(normal, i_vector, impulse = 1):
	'i_vector reflection with normal vector.'
	if complex(*normal) != 0 and complex(*i_vector) != 0:
		alpha = complex(*normal) / abs(complex(*normal))
		incidence =complex(*i_vector) / abs(complex(*i_vector))
		rotated = -complex(*i_vector) * (alpha/incidence)**2
		rotated *= impulse
		reflected = rotated.real, rotated.imag
	else:
		reflected = i_vector
	return reflected

# Wall abstract base class, not intended tu instantiate.
# use the specific wall classes below
# CircunWall,
class Wall(ABC):

	@abstractmethod
	def draw(self, surface):
		pass

	@abstractmethod
	def collide(self, o):
		pass

	@abstractmethod
	def bounce(self, o):
		pass

	def move_to_safe(self, o):
		while self.collide(o):
			o.rect.x += o.speedx
			o.rect.y += o.speedy

class CircunWall(Wall):
	def __init__(self, center, radio, color):
		self.center = center
		self.radio = radio
		self.color = color

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.center, self.radio)

	def collide(self, o):
		centers_distance = distance(o.rect.center, self.center)
		distance_to_circunf = self.radio - centers_distance
		return -o.radio < distance_to_circunf < o.radio

	def bounce(self, o, impulse=None):
		normal = direction(self.center, o.rect.center)
		i_vector = o.speedx , o.speedy
		if impulse:
			o.speedx, o.speedy = reflection(normal, i_vector, impulse)
		else:
			o.speedx, o.speedy = reflection(normal, i_vector)

class ArcWall(Wall):
	def __init__(self, center, radio, start, stop, color):
		self.center = center
		self.radio = radio
		diam = 2*radio
		self.rect = pygame.Rect(center, (diam, diam)).move(-radio, -radio)
		self.start = start
		self.stop = stop
		if self.stop < self.start:
			self.stop += math.tau
		self.color = color

	def draw(self, surface):
		pygame.draw.arc(surface, self.color, self.rect, -self.stop, -self.start )

	def collide(self, o):
		colliding = False
		o_rel_x, o_rel_y = direction(self.center, o)
		o_angle = math.atan2(o_rel_y, o_rel_x)
		if o_angle < 0:
			o_angle += math.tau
		if self.start <= o_angle <= self.stop:
			centers_distance = distance(o.rect.center, self.center)
			distance_to_circunf = self.radio - centers_distance
			colliding = -o.radio < distance_to_circunf < o.radio
		return colliding

	def bounce(self, o, impulse=None):
		normal = direction(self.center, o.rect.center)
		i_vector = o.speedx, o.speedy
		if impulse:
			o.speedx, o.speedy = reflection(normal, i_vector, impulse)
		else:
			o.speedx, o.speedy = reflection(normal, i_vector)

class LineWall(Wall):
	def __init__(self, start, stop, color):
		self.start = start
		self.stop = stop
		self.color = color

	def draw(self, surface):
		pygame.draw.line(surface, self.color, self.start, self.stop)

	def collide(self, o):
		p = complex(*direction(self.start, o.rect.center))
		ba = complex(*direction(self.start, self.stop))
		pba = p/ba
		if 0 <= pba.real <= 1:
			line_distance = abs(pba.imag*ba)
		else:
			line_distance = min(
				distance(self.start, o.rect.center), 
				distance(self.stop, o.rect.center))
		return line_distance < o.radio

	def bounce(self, o, impulse=None):
		normal = direction(self.start, self.stop)
		i_vector = -o.speedx, -o.speedy
		if impulse:
			o.speedx, o.speedy = reflection(normal, i_vector, impulse)
		else:
			o.speedx, o.speedy = reflection(normal, i_vector)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/borde.png").convert(),(150,25))
		#self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH//2
		self.rect.y = 550
		self.speedx = 0
		self.score = 0
		
	def update(self):
		self.speedx = 0
		#self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			self.speedx = -7
		if keystate[pygame.K_d]:
			self.speedx = 7
		self.rect.x += self.speedx
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		
class Ball(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/Ball1.png").convert_alpha()
		#self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH // 2
		self.rect.y = HEIGHT // 2
		self.radio = self.rect.w/2
		self.speedy = 4
		self.speedx = 4
		
	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		
		if self.rect.left < 0 or self.rect.right > WIDTH:
			self.speedx = -self.speedx
		if self.rect.top < 0:
			self.speedy = -self.speedy
		if self.speedx > 5:
			self.speedx -= 0.1
		if self.speedx < -5:
			self.speedx += 0.1
		if self.speedy > 5:
			self.speedy -= 0.1
		if self.speedy < -5:
			self.speedy += 0.1

class Bumper(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame .transform.scale(pygame.image.load("img/bumper2.png"),(50,50)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		a_list = [-2,-1,1,2]
		self.speedx = 0
		self.speedy = 0

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.left < 0 or self.rect.right > WIDTH:
			self.speedx = -self.speedx
		if self.rect.top < 0 or self.rect.bottom > 500:
			self.speedy = -self.speedy

class Bumper1(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 300
		self.rect.y = 300
		
class Bumper2(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 500
		self.rect.y = 300
		
class Bumper3(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 400
		self.rect.y = 200

class Bumper4(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 200
		self.rect.y = 200

class Bumper5(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 500
		self.rect.y = 200

class Bumper6(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 300
		self.rect.y = 200

def show_go_screen():
	
	screen.fill(BLACK)
	draw_text1(screen, "Pinball", 65, WIDTH // 2, HEIGHT // 4)
	draw_text1(screen, "-", 20, WIDTH // 2, HEIGHT // 2)
	draw_text1(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 3/4)
	draw_text1(screen, "Created by: Francisco Carvajal", 10,  60, 625)

	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

def get_high_score():
	with open(file_path,'r') as file:
		return file.read()

def show_game_over_screen():
	screen.fill(BLACK)
	if highest_score <= score:
		draw_text1(screen, "¡high score!", 60, WIDTH  // 2, HEIGHT * 1/4)
		draw_text1(screen, "score: "+str(score), 30, WIDTH // 2, HEIGHT // 2)
		draw_text1(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 4/5)
	else:
		draw_text1(screen, "score: "+str(score), 60, WIDTH // 2, HEIGHT * 1/3)
		draw_text1(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 2/3)

	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

### high score

try:
	highest_score = int(get_high_score())
except:
	highest_score = 0

circle1 = CircunWall((325,325), 23, RED)
circle2 = CircunWall((525,325), 23, RED)
circle3 = CircunWall((425,225), 23, RED)
circle4 = CircunWall((225,225), 23, RED)
circle5 = CircunWall((525,225), 23, RED)
circle6 = CircunWall((325,225), 23, RED)
walls = [circle1, circle2, circle3, circle4, circle5, circle6]
game_over = False
running = True
start = True
while running:
	screen.fill(BLACK)
	if game_over:

		show_game_over_screen()

		game_over = False
		screen.fill(BLACK)
		all_sprites = pygame.sprite.Group()
		

		ball = Ball()
		player = Player()
		all_sprites.add(player, ball)
	
		bumper1 = Bumper1()
		bumper2 = Bumper2()
		bumper3 = Bumper3()
		bumper4 = Bumper4()
		bumper5 = Bumper5()
		bumper6 = Bumper6()	
		all_sprites.add(bumper1, bumper2, bumper3, bumper4, bumper5, bumper6)
		
	
		score = 0

	if start:

		show_go_screen()

		start = False
		screen.fill(BLACK)
		all_sprites = pygame.sprite.Group()
		

		ball = Ball()
		player = Player()
		all_sprites.add(player, ball)
		
		bumper1 = Bumper1()
		bumper2 = Bumper2()
		bumper3 = Bumper3()
		bumper4 = Bumper4()
		bumper5 = Bumper5()
		bumper6 = Bumper6()		
		all_sprites.add(bumper1, bumper2, bumper3, bumper4, bumper5, bumper6)
		
		score = 0
		
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	all_sprites.update()
	for w in walls:
		if w.collide(ball):
			w.bounce(ball, impulse = 1.4)
			score += 25
			w.move_to_safe(ball)

	# termino del juego por borde inferior
	if ball.rect.top > 610:
		game_over = True

	
	
	# checar colisiones - ball - player
	if pygame.sprite.collide_rect(ball, player):
		if ball.speedy > 0:
			ball.rect.bottom = player.rect.top
			ball.speedy = -ball.speedy

	for w in walls:
		w.draw(screen)
	
	all_sprites.draw(screen)

	#Marcador
	
	draw_text1(screen, str(score), 25, WIDTH // 2, 10)
	
	pygame.display.flip()
pygame.quit()

"""
# Checar colisiones - ball - bumper1
	if pygame.sprite.collide_rect(ball, bumper1):
		score += 300
		ball.speedx = -ball.speedx + randint(-1,1)
		ball.speedy = -ball.speedy + randint(-1,1)
		
	# Checar colisiones - ball - bumper2
	if pygame.sprite.collide_rect(ball, bumper2):
		score += 25
		ball.speedx = -ball.speedx + randint(-1,1)
		ball.speedy = -ball.speedy + randint(-1,1)

	# Checar colisiones - ball - bumper3
	if pygame.sprite.collide_rect(ball, bumper3):
		score += 25
		ball.speedx = -ball.speedx + randint(-1,1)
		ball.speedy = -ball.speedy + randint(-1,1)
	# Checar colisiones - ball - bumper4
	if pygame.sprite.collide_rect(ball, bumper4):
		score += 25
		ball.speedx = -ball.speedx + randint(-1,1)
		ball.speedy = -ball.speedy + randint(-1,1)
	# Checar colisiones - ball - bumper5
	if pygame.sprite.collide_rect(ball, bumper5):
		score += 25
		ball.speedx = -ball.speedx + randint(-1,1)
		ball.speedy = -ball.speedy + randint(-1,1)
	# Checar colisiones - ball - bumper6
	if pygame.sprite.collide_rect(ball, bumper6):
		score += 25
		ball.speedx = -ball.speedx + randint(-1,1)
		ball.speedy = -ball.speedy + randint(-1,1)

"""