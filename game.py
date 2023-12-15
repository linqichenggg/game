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
# rock_img = pygame.image.load(os.path.join("img","c0.jpg")).convert()
rock_imgs = []
for i in range(3):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"c{i}.jpg")).convert())

#score display
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

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
        self.image_ori = pygame.transform.scale(random.choice(rock_imgs),(30,40))
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.9 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randrange(0,WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-100, -40)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        # rotate
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)


    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        #center
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
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
score = 0

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
    #every hit is the cigarette that collide with dingzhen
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        score += hit.radius
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)

    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    #display
    screen.fill(BLACK)
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    pygame.display.update()
pygame.quit()