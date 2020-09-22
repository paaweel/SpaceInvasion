from os import path
import pygame

class GraphicsProvider():
    def __init__(self, settings):
        super().__init__()
        self.settings = settings

        self.img_dir = path.join(path.dirname(__file__), 'img')

        self.load_graphics()
        self.load_animations()

    def load_graphics(self):
        self.background = pygame.image.load(path.join(self.img_dir, "starfield.png")).convert()
        self.background_rect = self.background.get_rect()
        self.player_img = pygame.image.load(path.join(self.img_dir, "playerShip.png")).convert()
        self.enemy_img = pygame.image.load(path.join(self.img_dir, "enemyShip.png")).convert()
        self.player_mini_img = pygame.transform.scale(self.player_img, (25, 19))
        self.player_mini_img.set_colorkey(self.settings.colors.black)
        self.bullet_img = pygame.image.load(path.join(self.img_dir, "laserRed16.png")).convert()
        self.meteor_images = []
        meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png']
        for img in meteor_list:
             self.meteor_images.append(pygame.image.load(path.join(self.img_dir, img)).convert())

    def load_animations(self):
        self.explosion_anim = {}
        self.explosion_anim['large'] = []
        self.explosion_anim['small'] = []
        self.explosion_anim['player'] = []

        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join(self.img_dir, filename)).convert()
            img.set_colorkey(self.settings.colors.black)
            img_lg = pygame.transform.scale(img, (75, 75))
            self.explosion_anim['large'].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            self.explosion_anim['small'].append(img_sm)
            filename = 'sonicExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join(self.img_dir, filename)).convert()
            img.set_colorkey(self.settings.colors.black)
            self.explosion_anim['player'].append(img)

        self.powerup_images = {}
        self.powerup_images['shield'] = pygame.image.load(path.join(self.img_dir, 'shield_gold.png')).convert()
        self.powerup_images['gun'] = pygame.image.load(path.join(self.img_dir, 'bolt_gold.png')).convert()

