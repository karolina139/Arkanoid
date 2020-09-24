import pygame

class Extensions(pygame.sprite.Sprite):
    """Klasa tworząca rozszerzenia."""

    def __init__(self, posx, posy, extension):

        # Inicjalizuj klasę bazową Sprite
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(extension)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy
        self.speed = 5

