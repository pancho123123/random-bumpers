import pygame
from random import randint
from pathlib import Path


WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
#GREEN = (0, 255, 0)
#RED = (255,0,0)
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
		self.speedx = randint(-1,1)
		self.speedy = randint(-1,1)

class Bumper1(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 300
		self.rect.y = 300
		
	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.left < 0 or self.rect.right > WIDTH:
			self.speedx = -self.speedx
		if self.rect.top < 0 or self.rect.bottom > 500:
			self.speedy = -self.speedy

class Bumper2(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 500
		self.rect.y = 300
		
	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.left < 0 or self.rect.right > WIDTH:
			self.speedx = -self.speedx
		if self.rect.top < 0 or self.rect.bottom > 500:
			self.speedy = -self.speedy

		
class Bumper3(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 400
		self.rect.y = 200

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.left < 0 or self.rect.right > WIDTH:
			self.speedx = -self.speedx
		if self.rect.top < 0 or self.rect.bottom > 500:
			self.speedy = -self.speedy


class Bumper4(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 200
		self.rect.y = 200

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.left < 0 or self.rect.right > WIDTH:
			self.speedx = -self.speedx
		if self.rect.top < 0 or self.rect.bottom > 500:
			self.speedy = -self.speedy


class Bumper5(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 500
		self.rect.y = 200

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.left < 0 or self.rect.right > WIDTH:
			self.speedx = -self.speedx
		if self.rect.top < 0 or self.rect.bottom > 500:
			self.speedy = -self.speedy

class Bumper6(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 300
		self.rect.y = 200

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.left < 0 or self.rect.right > WIDTH:
			self.speedx = -self.speedx
		if self.rect.top < 0 or self.rect.bottom > 500:
			self.speedy = -self.speedy


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

	# termino del juego por borde inferior
	if ball.rect.top > 610:
		game_over = True

	
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
	# checar colisiones - ball - player
	if pygame.sprite.collide_rect(ball, player):
		ball.rect.bottom = player.rect.top
		ball.speedy = -ball.speedy

		
	
	all_sprites.draw(screen)

	#Marcador
	
	draw_text1(screen, str(score), 25, WIDTH // 2, 10)
	
	pygame.display.flip()
pygame.quit()