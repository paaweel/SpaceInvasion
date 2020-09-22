import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, settings, graphics_provider):
        pygame.sprite.Sprite.__init__(self)

        self.settings = settings
        self.graphics_provider = graphics_provider
        
        self.image = pygame.transform.scale(self.graphics_provider.enemy_img, (50, 50))
        self.image.set_colorkey(settings.colors.black)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(self.settings.WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > self.settings.HEIGHT + 10 or self.rect.left < -100 or self.rect.right > self.settings.WIDTH + 100:
            self.rect.x = random.randrange(self.settings.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

            
