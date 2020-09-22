import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, graphics_provider):
        self.graphics_provider = graphics_provider
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = self.graphics_provider.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.graphics_provider.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.graphics_provider.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center