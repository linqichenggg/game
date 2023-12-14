import pygame
import random
import os

FPS = 60
WIDTH = 1000
HEIGHT = 800

WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

#initial
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("lqc")
clock = pygame.time.Clock()

#img
background_img = pygame.image.load(os.path.join("img","litang.jpg")).convert()
player_img = pygame.image.load(os.path.join("img","dingzhen.jpg")).convert()
rock_img = pygame.image.load(os.path.join("img","chuan.jpg")).convert()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (47,51))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 5
        self.speedx = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(rock_img,(23,35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width*0.9 / 2
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randrange(0,WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-100, -40)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        self.rot_degree = 5


    # def rotate(self):
    #     self.image = pygame.transform.rotate(self.image, self.rot_degree)

    def update(self):
        # self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top >HEIGHT or self.rect.left > WIDTH or self.rect.right < 0 :
            self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
            self.rect.bottom = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

#loop
running = True
while running:
    clock.tick(FPS)
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #update
    all_sprites.update()
    hits =  pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        r= Rock()
        all_sprites.add(r)
        rocks.add(r)

    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    #display
    screen.fill(BLACK)
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    pygame.display.update()
pygame.quit()