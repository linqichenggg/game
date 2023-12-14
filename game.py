import pygame

FPS = 60
WIDTH = 500
HEIGHT = 600

WHITE = (255,255,255)
GREEN = (0,255,0)

#initial
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("dingzhen")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

#loop
running = True
while running:
    clock.tick(FPS)
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update
    all_sprites.update()

    #display
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()