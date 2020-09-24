import pygame
import os
import math
import time

class Functions():
    """Klasa przechowująca funkcje."""

    def __init__(self):

        self.screen_width = 800
        self.screen_height = 600
        self.screen_size = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.white = (255, 255, 255)

        pygame.init()

        #inicjalizacja fontów
        self.smallfont = pygame.font.SysFont("comicsansms", 25)
        self.mediumfont = pygame.font.SysFont("comicsansms", 38)
        self.bigfont = pygame.font.SysFont("comicsansms", 50)
        self.largefont = pygame.font.SysFont("comicsansms", 70)
        self.victoryfont = pygame.font.SysFont("comicsansms", 90)

    def score(self,killed_blocks, all_blocks):
        """Przedstawia aktualny wynik w lewym górnym rogu ekranu."""
        text = self.smallfont.render("Score: %s / %s"%(str(killed_blocks), str(all_blocks)), True, self.white )
        self.screen.blit(text, [0, 0])

    def lives(self,live):
        """Przedstawia aktualny wynik w lewym górnym rogu ekranu."""
        text = self.smallfont.render("Lives: %s / 3"%(str(live)), True, self.white)
        self.screen.blit(text, [665, 0])

    def text_object(self, text, color, size):
        """Tworzy tekst na obiekcie w zależności od jego wielkości."""

        if size == "small":
            textSurface = self.smallfont.render(text, True, color)
        elif size == "medium":
            textSurface = self.mediumfont.render(text, True, color)
        elif size == "big":
            textSurface = self.bigfont.render(text, True, color)
        elif size == "large":
            textSurface = self.largefont.render(text, True, color)
        elif size == "victory":
            textSurface = self.victoryfont.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def text_to_button(self, msg, color, buttonx, buttony, width, height, size="small"):
        """Przypisuje teskt do konkretnego przycisku."""
        textSurf, textRect = Functions.text_object(self,msg, color, size)
        textRect.center = ((buttonx+(width/2)), buttony+(height/2)) #wyśrodkowanie tekstu
        self.screen.blit(textSurf, textRect)

    def message(self, msg, color, y_displace=0, size="small"):
        """Wyświetla tekst na ekranie."""
        textSurf, textRect = Functions.text_object(self,msg,color,size)
        textRect.center = (self.screen_width/2), (self.screen_height/2) + y_displace
        self.screen.blit(textSurf, textRect)

    def reset_ball(self):
        """Resetuje predkości piłki."""
        self.ball.x_velocity = 0
        self.ball.y_velocity = 0

    def calculate_velocity(self, velocity, expected_x):
        """Liczy potrzebne wartości w celu zachowania tej samej prędkości."""
        return math.sqrt(velocity - expected_x**2)

    def loadSound(self, name):
        """Laduje dźwięk."""
        fullname = os.path.join("data", name)
        sound = pygame.mixer.Sound(fullname)
        return sound

    def invite(self):
        """Ekran wyświetlający sie przy wyjściu z gry, zapraszający do ponownej gry."""

        self.screen.fill(self.grey)
        Functions.message(self, "Come again!",
                          self.white,
                          size="big")
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        quit()






