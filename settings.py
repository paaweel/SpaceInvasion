class Settings():
    """A class to store all settings for the game."""
    
    def __init__(self):
        super().__init__()

        # General settings
        self.application_name = "SpaceInvaderv2"
        self.font = "arial"

        # Screen dimensions
        self.HEIGHT = 600
        self.WIDTH = 600
        
        # Colors data structure
        self.colors = Colors()
        
        self.FPS = 60
        self.power_up_time = 5000

        self.BAR_LENGTH = 100
        self.BAR_HEIGHT = 10



class Colors():
    """A class to store all colors for the game."""
    
    def __init__(self):
        super().__init__()

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
