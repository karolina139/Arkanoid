import pygame
from functions import Functions


class Pages():
    """Klasa tworząca deskę."""

    def __init__(self):

        self.screen_width = 800
        self.screen_height = 600
        self.screen_size = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.white = (255, 255, 255)
        self.grey = (128, 128, 128)
        self.light_grey = (179, 179, 179)

        pygame.init()
        
        #czcionki
        self.smallfont = pygame.font.SysFont("comicsansms", 25)
        self.mediumfont = pygame.font.SysFont("comicsansms", 38)
        self.bigfont = pygame.font.SysFont("comicsansms", 50)
        self.largefont = pygame.font.SysFont("comicsansms", 70)
        self.victoryfont = pygame.font.SysFont("comicsansms", 90)

    def victory(self):
        """Tworzy stronę pojawiającą się w przpadku zwycięstwa."""
        author = True
        while author:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            self.screen.fill(self.grey)

            Functions.message(self, "V i c t o r y!",
                              self.white,
                              y_displace=-50,
                              size="victory")

            self.button("play again", 72.5, 500, 170, 40, self.grey, self.light_grey, action="play",text_color = self.white)
            self.button("back to menu", 315, 500, 170, 40, self.grey, self.light_grey, action="back to menu", text_color=self.white)
            self.button("quit", 557.5, 500, 170, 40, self.grey, self.light_grey, action="quit", text_color=self.white)

            pygame.display.update()

    def start(self):
        """Tworzy stronę pojawiającą się w na starcie."""

        intro = True
        while intro:
            self.sound_start.play()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            self.screen.blit(self.background, [0, 0])

            self.button("Welcome to Arkanoid", 0, 100, 800, 150, self.white, self.white, size="large")
            self.button("play", 275, 310, 250, 65, self.light_grey, self.grey, action="play", size="medium")
            self.button("options", 125, 460, 170, 40, self.light_grey, self.grey, action="options")
            self.button("about author", 315, 460, 170, 40, self.light_grey, self.grey, action="about author")
            self.button("quit", 505, 460, 170, 40, self.light_grey, self.grey, action="quit")
            pygame.display.flip()
            pygame.display.update()


    def second_options(self):
        """Tworzy drugą stronę z opcjami."""

        opt1 = True
        while opt1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            self.screen.fill(self.grey)

            Functions.message(self, "Choose length of paddle:",
                              self.white,
                              y_displace=-200,
                              size="small")

            self.button("short", 120, 150, 160, 35, self.light_grey, self.dark_grey, action="short_paddle")
            self.button("medium", 320, 150, 160, 35, self.light_grey, self.dark_grey, action="medium_paddle")
            self.button("long", 520, 150, 160, 35, self.light_grey, self.dark_grey, action="long_paddle")

            Functions.message(self, "Choose size of ball:",
                              self.white,
                              y_displace=0,
                              size="small")

            self.button("small", 120, 350, 160, 35, self.light_grey, self.dark_grey, action="small_ball")
            self.button("medium", 320, 350, 160, 35, self.light_grey, self.dark_grey, action="medium_ball")
            self.button("big", 520, 350, 160, 35, self.light_grey, self.dark_grey, action="big_ball")

            self.button("back", 330, 500, 140, 60, self.light_grey, self.dark_grey, action="back to options")

            pygame.display.update()

    def about_author(self):
        """Tworzy stronę z informacjami o autorze"""

        author = True
        while author:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            self.screen.fill(self.grey)

            Functions.message(self, "Author:",
                              self.white,
                              y_displace=-100,
                              size="small")
            Functions.message(self, "Rakus Karolina",
                              self.white,
                              y_displace= 0 ,
                              size="big")
            self.button("back", 330, 500, 140, 60, self.light_grey, self.dark_grey, action="back to menu")

            pygame.display.update()



