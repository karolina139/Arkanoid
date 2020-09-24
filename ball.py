import pygame

class Ball(pygame.sprite.Sprite):
    """Klasa tworząca piłkę."""

    def __init__(self, width, height):

        #inicjalizuj klasę bazową
        pygame.sprite.Sprite.__init__(self)

        self.screen_width = 800
        self.scree_height = 600
        self.width = width
        self.height = height
        self.image = pygame.image.load("data/ball.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.centerx = 400
        self.rect.centery = 540
        self.x_velocity = 0
        self.y_velocity = 4

    def update(self):
        """Sprawdza czy piłka nie opuściła ekranu."""
        if self.rect.left < 0 or self.rect.right > self.screen_width:
            self.x_velocity = -self.x_velocity
#
        if self.rect.top < 5:
            self.y_velocity = -self.y_velocity

    def get_pos(self):
        """Zwraca wartość środka piłki."""
        return self.rect.centerx


