import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, settings, graphics_provider, sound_provider, bullets, all_sprites):
        pygame.sprite.Sprite.__init__(self)

        self.settings = settings
        self.bullets = bullets
        self.all_sprites = all_sprites
        self.graphics_provider = graphics_provider
        self.sound_provider = sound_provider

        self.image = pygame.transform.scale(self.graphics_provider.player_img, (50, 38))
        self.image.set_colorkey(settings.colors.black)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = settings.WIDTH / 2
        self.rect.bottom = settings.HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > self.settings.power_up_time:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = self.settings.WIDTH / 2
            self.rect.bottom = self.settings.HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > self.settings.WIDTH:
            self.rect.right = self.settings.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
                
            if self.power == 1:
                bullet = Bullet(
                    self.rect.centerx, 
                    self.rect.top, 
                    self.graphics_provider.bullet_img, 
                    self.settings)

                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
                self.sound_provider.shoot_sound.play()

            if self.power >= 2:
                bullet1 = Bullet(
                    self.rect.left, 
                    self.rect.centery, 
                    self.graphics_provider.bullet_img, 
                    self.settings)
                bullet2 = Bullet(
                    self.rect.right, 
                    self.rect.centery, 
                    self.graphics_provider.bullet_img, 
                    self.settings)

                self.all_sprites.add(bullet1)
                self.all_sprites.add(bullet2)
                self.bullets.add(bullet1)
                self.bullets.add(bullet2)
                self.sound_provider.shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (self.settings.WIDTH / 2, self.settings.HEIGHT + 200)
