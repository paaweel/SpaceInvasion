import sys
from time import sleep

import pygame
import random

from settings import Settings
from graphics_provider import GraphicsProvider
from sound_provider import SoundProvider
from mob import Mob
from player import Player
from bullet import Bullet
from explosion import Explosion
from powerup import Powerup
from enemy import Enemy


class Game:
    """Overall class to manage the game."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        
        self.settings = Settings()
        self.setup_pygame()
        
        self.graphics_provider = GraphicsProvider(self.settings)
        self.sound_provider = SoundProvider()

    def setup_pygame(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
        pygame.display.set_caption(self.settings.application_name)
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font('arial')

    def draw_text(self, surf, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.settings.colors.white)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def new_mob(self):
        mob = Mob(self.settings, self.graphics_provider)
        self.all_sprites.add(mob)
        self.mobs.add(mob)

    def new_enemy(self):
        enemy = Enemy(self.settings, self.graphics_provider)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def draw_shield_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0

        fill = (pct / 100) * self.settings.BAR_LENGTH
        outline_rect = pygame.Rect(x, y, self.settings.BAR_LENGTH, self.settings.BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, self.settings.BAR_HEIGHT)
        pygame.draw.rect(surf, self.settings.colors.green, fill_rect)
        pygame.draw.rect(surf, self.settings.colors.white, outline_rect, 2)

    def draw_lives(self, surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            surf.blit(img, img_rect)

    def show_go_screen(self):
        self.screen.blit(self.graphics_provider.background, self.graphics_provider.background_rect)
        self.draw_text(self.screen, self.settings.application_name, 64, self.settings.WIDTH / 2, self.settings.HEIGHT / 4)
        self.draw_text(self.screen, "Use Arrow keys move, Space to fire", 22, self.settings.WIDTH / 2, self.settings.HEIGHT / 2)
        self.draw_text(self.screen, "Press any key to begin", 18, self.settings.WIDTH / 2, self.settings.HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        
        while waiting:
            self.clock.tick(self.settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def run_game(self):
        game_over = True
        running = True

        while running:
            if game_over:
                self.show_go_screen()
                game_over = False
                self.all_sprites = pygame.sprite.Group()
                self.mobs = pygame.sprite.Group()
                self.enemies = pygame.sprite.Group()
                self.bullets = pygame.sprite.Group()
                self.powerups = pygame.sprite.Group()

                self.player = Player(
                    self.settings, 
                    self.graphics_provider, 
                    self.sound_provider, 
                    self.bullets, 
                    self.all_sprites)

                self.all_sprites.add(self.player)
                for i in range(8):
                    self.new_mob()

                for i in range(3):
                    self.new_enemy()
                
                score = 0

            # keep loop running at the right speed
            self.clock.tick(self.settings.FPS)
            # Process input (events)
            for event in pygame.event.get():
            # check for closing window
                if event.type == pygame.QUIT:
                    running = False

            # Update
            self.all_sprites.update()

            # check to see if a bullet hit a mob
            hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
            for hit in hits:
                score += 50 - hit.radius
                random.choice(self.sound_provider.expl_sounds).play()
                expl = Explosion(hit.rect.center, 'large', self.graphics_provider)
                self.all_sprites.add(expl)
                if random.random() > 0.9:
                    powerup = Powerup(hit.rect.center, self.settings, self.graphics_provider)
                    self.all_sprites.add(powerup)
                    self.powerups.add(powerup)
                self.new_mob()

            # check to see if a bullet hit an enemy
            hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
            for hit in hits:
                score += 50 - hit.radius
                random.choice(self.sound_provider.expl_sounds).play()
                expl = Explosion(hit.rect.center, 'large', self.graphics_provider)
                self.all_sprites.add(expl)
                if random.random() > 0.9:
                    powerup = Powerup(hit.rect.center, self.settings, self.graphics_provider)
                    self.all_sprites.add(powerup)
                    self.powerups.add(powerup)
                self.new_enemy()

            # check to see if a mob hit the player  
            hits = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_circle)
            for hit in hits:
                self.player.shield -= hit.radius * 2
                expl = Explosion(hit.rect.center, 'small', self.graphics_provider)
                self.all_sprites.add(expl)
                self.new_mob()
                if self.player.shield <= 0:
                    self.sound_provider.player_die_sound.play()
                    death_explosion = Explosion(self.player.rect.center, 'player', self.graphics_provider)
                    self.all_sprites.add(death_explosion)
                    self.player.hide()
                    self.player.lives -= 1
                    self.player.shield = 100

            # check to see if player hit a powerup
            hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
            for hit in hits:
                if hit.type == 'shield':
                    self.player.shield += random.randrange(10, 30)
                    self.sound_provider.shield_sound.play()
                    if self.player.shield >= 100:
                        self.player.shield = 100
                if hit.type == 'gun':
                    self.player.powerup()
                    self.sound_provider.power_sound.play()

            # if the player died and the explosion has finished playing
            if self.player.lives == 0 and not death_explosion.alive():
                game_over = True

            # Draw / render
            self.screen.fill(self.settings.colors.black)
            self.screen.blit(self.graphics_provider.background, self.graphics_provider.background_rect)
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, str(score), 18, self.settings.WIDTH / 2, 10)
            self.draw_shield_bar(self.screen, 5, 5, self.player.shield)
            self.draw_lives(self.screen, self.settings.WIDTH - 100, 5, self.player.lives, self.graphics_provider.player_mini_img)
            # *after* drawing everything, flip the display
            pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = Game()
    ai.run_game()
