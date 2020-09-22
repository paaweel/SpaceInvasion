import pygame 
from os import path

class SoundProvider():
    def __init__(self):
        super().__init__()
        self.snd_dir = path.join(path.dirname(__file__), 'snd')
        self.load_sounds()

    def load_sounds(self):
        self.shoot_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'pew.wav'))
        self.shield_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'pow4.wav'))
        self.power_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'pow5.wav'))
        
        self.expl_sounds = []
        for snd in ['expl3.wav', 'expl6.wav']:
            self.expl_sounds.append(pygame.mixer.Sound(path.join(self.snd_dir, snd)))
        self.player_die_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'rumble1.ogg'))
        
        pygame.mixer.music.load(path.join(self.snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)