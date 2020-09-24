import pygame

class DoubleBlocks(pygame.sprite.Sprite):
    """Klasa tworząca klocki do planszy"""

    def __init__(self, posx, posy, texture):

        # Inicjalizuj klasę bazową Sprite
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("data/gray_brick")
        self.image = pygame.transform.scale(self.image, (80, 25))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy