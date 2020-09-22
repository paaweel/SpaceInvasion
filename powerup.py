import pygame
import random

class Powerup(pygame.sprite.Sprite):
    def __init__(self, center, settings, graphics_provider):
        pygame.sprite.Sprite.__init__(self)

        self.settings = settings
        self.graphics_provider = graphics_provider
        
        self.type = random.choice(['shield', 'gun'])
        self.image = self.graphics_provider.powerup_images[self.type]
        self.image.set_colorkey(self.settings.colors.black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > self.settings.HEIGHT:
            self.kill()