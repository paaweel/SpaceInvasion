import pygame
import random

class Mob(pygame.sprite.Sprite):
    def __init__(self, settings, graphics_provider):
        pygame.sprite.Sprite.__init__(self)

        self.settings = settings
        self.graphics_provider = graphics_provider
        
        self.image_orig = random.choice(self.graphics_provider.meteor_images)
        self.image_orig.set_colorkey(self.settings.colors.black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(self.settings.WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > self.settings.HEIGHT + 10 or self.rect.left < -100 or self.rect.right > self.settings.WIDTH + 100:
            self.rect.x = random.randrange(self.settings.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
