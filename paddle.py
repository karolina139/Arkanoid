import pygame
from pygame import *

class Paddle(pygame.sprite.Sprite):
    """Klasa tworząca deskę."""

    def __init__(self, x,y,sizex,sizey,color):

        # Inicjalizuj klasę bazową Sprite
        pygame.sprite.Sprite.__init__(self)

        self.screen_width = 800
        self.image = pygame.Surface((sizex, sizey), SRCALPHA,32)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.image.fill(color)
        self.speed = 5


    def update(self):
        """Sprawdza czy deska nie opuściła ekranu."""
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def get_pos(self):
        """Zwraca wartość środka deski."""
        return self.rect.centerx

