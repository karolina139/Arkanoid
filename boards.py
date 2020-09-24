import pygame



class Pages():
    """Klasa przechowująca poszczególne strony gry."""

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen_size = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.white = (255, 255, 255)
        self.grey = (128, 128, 128)
        self.light_grey = (179, 179, 179)

        pygame.init()

        self.smallfont = pygame.font.SysFont("comicsansms", 25)
        self.mediumfont = pygame.font.SysFont("comicsansms", 38)
        self.bigfont = pygame.font.SysFont("comicsansms", 50)
        self.largefont = pygame.font.SysFont("comicsansms", 70)
        self.victoryfont = pygame.font.SysFont("comicsansms", 90)
