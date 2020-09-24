#<a href='https://www.freepik.com/free-photos-vectors/background'>Background vector created by eightonesix - www.freepik.com</a>
#pozwolenie na użycie grafik

import pygame
from paddle import Paddle
from ball import Ball
from blocks import Blocks
import time
from functions import Functions
from pages import Pages
from extensions import Extensions
import random

class Game():
    def __init__(self):

        #Inicjalizacja PyGame
        self.screen_width = 800
        self.screen_height = 600
        self.screen_size = (self.screen_width, self.screen_height)

        #kolory
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.light_grey= (179, 179, 179)
        self.grey = (128, 128, 128)
        self.dark_grey = (115, 115, 115)

        #zmienne definiowane w celu utzryamania stałej prędkości piłki
        self.start_vel_x = 4
        self.start_vel_y = 4
        self.velocity = self.start_vel_x**2 + self.start_vel_y**2

        #zmienne potrzebne do zmiany parametrów
        self.board1 = False
        self.board2 = False
        self.board3 = False
        self.paddle_width = 0
        self.ball_width = 0
        self.check = 40

        #licznik żyć
        self.live_counter = 3

        #zdjęcia planszy
        self.board1_image = pygame.image.load("data/board1.png")
        self.board1_image = pygame.transform.scale(self.board1_image, (225,170))
        self.board2_image = pygame.image.load("data/board2.png")
        self.board2_image = pygame.transform.scale(self.board2_image, (225,170))
        self.board3_image = pygame.image.load("data/board3.png")
        self.board3_image = pygame.transform.scale(self.board3_image, (225, 170))

        self.background = pygame.image.load("data/background.jpg")

        pygame.init()

        #dźwięki w grze
        self.sound_killed_bricks = Functions.loadSound(self, "wood_knock.wav")
        self.sound_bounced_ball = Functions.loadSound(self, "paddle_bound.wav")
        self.sound_start = Functions.loadSound(self, "start.wav")
        self.sound_game = Functions.loadSound(self, "game.wav")
        self.sound_loose = Functions.loadSound(self, "loose_sound.wav")
        self.sound_victory = Functions.loadSound(self, "victory.wav")

        #czcionki
        self.smallfont = pygame.font.SysFont("comicsansms", 25)
        self.mediumfont = pygame.font.SysFont("comicsansms", 38)
        self.bigfont = pygame.font.SysFont("comicsansms", 50)
        self.largefont = pygame.font.SysFont("comicsansms", 70)
        self.victoryfont = pygame.font.SysFont("comicsansms", 90)

        #Inicializacja okna
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Arkanoid")

        #Inicjalizacja grupy dla planszy
        self.BlocksSprite = pygame.sprite.Group()
        
        #Inicjalizacja rozszerzeń
        self.AddSpeedSprite = pygame.sprite.Group()
        self.SubstractSpeedSprite = pygame.sprite.Group()

        #uruchomienie strony startowej
        Pages.start(self)
        Functions.reset_ball(self)

        self.gameLoop()

    def sprites(self, board=None, paddle_width=100, ball_width=30, ball_height=25):
        """
        Inicializuj grupy dla deski, piłki, rozszerzeń.
        :param board: numer planszy,
        :param paddle_width: szerokość deski,
        :param ball_width: szerekość piłki,
        :param ball_height: wysokość piłki.
        """

        self.PaddleSprite = pygame.sprite.Group()
        self.paddle = Paddle(int(self.screen_width/2 - paddle_width/2), int(self.screen_height-30), paddle_width, 10, self.white)
        self.PaddleSprite.add(self.paddle)
        self.paddle_width = paddle_width

        self.BallSprite = pygame.sprite.Group()
        self.ball = Ball(ball_width, ball_height)
        self.BallSprite.add(self.ball)
        self.ball_width = ball_width
        self.ball_height = ball_height

        #resetowanie zmiennej do wyświetlania wyniku
        self.killed_blocks = 0

        board

    def draw(self):
        """Rysuj grupy Sprite."""
        self.SubstractSpeedSprite.draw(self.screen)
        self.AddSpeedSprite.draw(self.screen)
        self.BallSprite.draw(self.screen)
        self.PaddleSprite.draw(self.screen)
        self.BlocksSprite.draw(self.screen)

    def update(self):
        """Aktualizuj grupy Sprite."""
        self.SubstractSpeedSprite.update()
        self.AddSpeedSprite.update()
        self.BallSprite.update()
        self.ball.rect.move_ip((self.ball.x_velocity, self.ball.y_velocity))
        self.PaddleSprite.update()
        self.BlocksSprite.update()

    def gameLoop(self):
        """Pętla gry właściwej."""
        self.sound_start.stop()
        self.sound_game.play()

        self.clock = pygame.time.Clock()
        self.delta = 0.0
        self.max_tps = 100.0

        self.exit = False
        self.gameover = False

        while not self.exit:

            #dzięlki temu zapewniam tą samą szybkość obiektów niezależnie od możliwości danego komputera
            self.delta += self.clock.tick() / 1000.0

            while self.delta > 1 / self.max_tps:
                self.delta -= 1 / self.max_tps

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.exit = True
                        if event.key == pygame.K_SPACE:
                            self.ball.y_velocity = -4
                            self.ball.x_velocity = 0

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.paddle.rect.x += -self.paddle.speed
                if keys[pygame.K_RIGHT]:
                    self.paddle.rect.x += self.paddle.speed
                elif keys[pygame.K_p]:
                    self.sound_game.stop()
                    self.pause()
                    self.clock = pygame.time.Clock()

                #przegrana
                if self.ball.rect.centery > self.screen_height-self.check:
                    Functions.reset_ball(self)
                    self.sound_game.stop()
                    if self.live_counter == 1:
                        self.sound_loose.play()
                        self.gameover = True
                    else:

                        self.ball.rect.top = self.screen_height - 100
                        self.ball.rect.centerx = self.screen_width / 2
                        self.paddle.rect.left = int(self.screen_width / 2 - self.paddle_width / 2)
                        self.paddle.rect.top = int(self.screen_height - 30)
                        self.sound_game.play()
                        time.sleep(1)

                    self.live_counter -= 1

                self.update()

                #zderzenie piłki i bloków
                for hit in pygame.sprite.groupcollide(self.BallSprite, self.BlocksSprite, 0, 1):
                    self.sound_killed_bricks.play()
                    self.ball.y_velocity = -self.ball.y_velocity
                self.killed_blocks = self.counter - len(self.BlocksSprite)

                #przspieszenie deski po zderzeniu pilki z rozszerzeniem
                for hit in pygame.sprite.groupcollide(self.BallSprite, self.AddSpeedSprite, 0, 1):
                    self.ball.y_velocity = -self.ball.y_velocity
                    self.paddle.speed = 10

                # przspieszenie deski po zderzeniu pilki z rozszerzeniem
                for hit in pygame.sprite.groupcollide(self.BallSprite, self.SubstractSpeedSprite, 0, 1):
                    self.ball.y_velocity = -self.ball.y_velocity
                    self.paddle.speed = 4

                #zwycięstwo
                if len(self.BlocksSprite) == 0:
                    self.sound_game.stop()
                    self.sound_victory.play()
                    self.live_counter =3
                    Pages.victory(self)

                # zderzenie piłki i deski
                for hit in pygame.sprite.groupcollide(self.PaddleSprite, self.BallSprite, 0, 0):

                    self.sound_bounced_ball.play()

                    # ustawienie różnych kątów odbicia piłki w zależności od miejsca jej odbicia na desce
                    if (self.paddle.get_pos() - self.paddle_width * 0.1) <= self.ball.get_pos() <= (self.paddle.get_pos() +self.paddle_width *0.1):
                        self.ball.x_velocity = 0
                        self.ball.y_velocity = - Functions.calculate_velocity(self,self.start_vel_y**2+ self.ball.x_velocity**2, 0)

                    elif self.paddle.get_pos() -self.paddle_width *0.5 -(self.ball_width/2) < self.ball.get_pos()  <self.paddle.get_pos() -self.paddle_width *0.3:
                        self.ball.x_velocity = -self.start_vel_x
                        self.ball.y_velocity = - self.ball.y_velocity

                    elif self.paddle.get_pos() + self.paddle_width * 0.3 <= self.ball.get_pos() < self.paddle.get_pos() + self.paddle_width * 0.5 + (self.ball_width/2):
                        self.ball.x_velocity = self.start_vel_x
                        self.ball.y_velocity = - self.ball.y_velocity

                    elif self.paddle.get_pos() - self.paddle_width * 0.3 <= self.ball.get_pos() < self.paddle.get_pos() - self.paddle_width * 0.1:
                        self.ball.x_velocity = -2
                        self.ball.y_velocity = Functions.calculate_velocity(self, self.velocity, -2)
                        self.ball.y_velocity = - self.ball.y_velocity

                    elif self.paddle.get_pos() + self.paddle_width * 0.1 < self.ball.get_pos() < self.paddle.get_pos() + self.paddle_width * 0.3:
                        self.ball.x_velocity = 2
                        self.ball.y_velocity = Functions.calculate_velocity(self, self.velocity, 2)
                        self.ball.y_velocity = - self.ball.y_velocity


                self.screen.fill(self.black)

                self.draw()

                #wysświetla wynik
                Functions.score(self, self.killed_blocks, self.counter)
                Functions.lives(self, self.live_counter)

                pygame.display.update()

                #pętla obsługująca przegraną
                while self.gameover == True:
                    self.sound_game.stop()

                    self.screen.fill(self.grey)
                    Functions.message(self, "Game over",
                                 self.white,
                                 y_displace=-50,
                                 size="large")
                    Functions.message(self, "Press M back to menu, or Q to quit",
                                 self.white,
                                 y_displace=50)
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                self.exit = True
                                self.gameover = False

                            if event.key == pygame.K_m:
                                Game()

                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                quit()

        Functions.invite(self)

    def options(self):
        """Tworzy pierwszą stronę z opcjami."""

        opt = True
        while opt:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            self.screen.fill(self.grey)
            self.screen.blit(self.board1_image, [47.5, 200])
            self.screen.blit(self.board2_image, [290, 200])
            self.screen.blit(self.board3_image, [537.5, 200])

            Functions.message(self, "To start the ball, press SPACE.",
                              self.white,
                              y_displace=-250,
                              size="small")

            Functions.message(self, "If you want to pause the game, press P.",
                              self.white,
                              y_displace=-200,
                              size="small")

            Functions.message(self, "Choose boards:",
                              self.white,
                              y_displace=-150,
                              size="small")

            self.button("back", 190, 500, 140, 60, self.light_grey, self.dark_grey, action="back to menu")
            self.button("next", 470, 500, 140, 60, self.light_grey, self.dark_grey, action="next")

            self.button("board 1", 80, 400, 160, 35, self.light_grey, self.dark_grey, action="board1")
            self.button("board 2", 320, 400, 160, 35, self.light_grey, self.dark_grey, action="board2")
            self.button("board 3", 560, 400, 160, 35, self.light_grey, self.dark_grey, action="board3")

            pygame.display.update()

    def pause(self):
        """Tworzy przezroczystą stronę dla pauzy."""

        paused = True

        Functions.message(self, "Paused",
                          self.white,
                          y_displace=-100,
                          size="large")
        Functions.message(self, "Press C to continue, M to back to menu, or Q to quit",
                          self.white,
                          y_displace=100)

        pygame.display.update()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.sound_game.play()
                        paused = False
                    elif event.key == pygame.K_m:
                        self.sound_game.stop()
                        Game()
                    elif event.key == pygame.K_q:
                        Functions.invite(self)
                    elif event.key == pygame.K_ESCAPE:
                        Functions.invite(self)


    def button(self, text, x, y, width, height, inactive_color, active_color, action=None, size="small", text_color=(0, 0, 0)):
        """
        Tworzy przyciski.
        :param text: tekst widniejący na przycisku,
        :param x: wartość z lewego górnego przycisku,
        :param y: wartość y lewego górnego roku przycisku,
        :param width: szerokość przycisku,
        :param height: wysokość przycisku,
        :param inactive_color: kolor nieaktywnego przycisku,
        :param active_color: kolor po najechaniu kursorem na przycisk,
        :param action: akcja jak ma się wykonać po naciśnięciu przycisku,
        :param size: rozmiar czcionki,
        :param text_color: kolor tekst.
        """

        #pozycja kursora
        cur = pygame.mouse.get_pos()

        #kliknięcie myszką
        click = pygame.mouse.get_pressed()

        if x + width > cur[0] > x and y + height > cur[1] > y:
            pygame.draw.rect(self.screen, active_color, (x, y, width, height))
            if click[0] == 1 and action != None:

                #opcje uruchomienia poszczególnych plansz
                if action == "board1":
                    self.board1 = True
                    self.board2 = False
                    self.board3 = False
                if action == "board2":
                    self.board2 = True
                    self.board1 = False
                    self.board3 = False
                if action == "board3":
                    self.board3 = True
                    self.board1 = False
                    self.board2 = False

                #parametry deski w zależności od wybranego rozmiaru
                if action == "short_paddle":
                    self.paddle_width = 70
                if action == "medium_paddle":
                    self.paddle_width = 100
                if action == "long_paddle":
                    self.paddle_width = 200

                #parametry piłki w zależności od wybranego rozmiaru
                if action == "small_ball":
                    self.ball_width = 18
                    self.ball_height = 15
                    self.check = 35
                if action == "medium_ball":
                    self.ball_width = 30
                    self.ball_height = 25
                    self.check = 40
                if action == "big_ball":
                    self.ball_width = 50
                    self.ball_height = 40
                    self.check = 45

                if action == "play":
                    #uruchomienie wybranych opcji z menu
                    if self.board1 == True and self.paddle_width == 0 and self.ball_width == 0:
                        self.sprites(self.plansza1())
                    elif self.board1 == True and self.paddle_width != 0 and self.ball_width == 0:
                        self.sprites(self.plansza1(), self.paddle_width)
                    elif self.board1 == True and self.paddle_width == 0 and self.ball_width != 0:
                        self.sprites(self.plansza1(), ball_width=self.ball_width, ball_height=self.ball_height)
                    elif self.board1 == True and self.paddle_width != 0 and self.ball_width != 0:
                        self.sprites(self.plansza1(), self.paddle_width, self.ball_width, self.ball_height)

                    elif self.board2 == True and self.paddle_width == 0 and self.ball_width == 0:
                        self.sprites(self.plansza2())
                    elif self.board2 == True and self.paddle_width != 0 and self.ball_width == 0:
                        self.sprites(self.plansza2(), self.paddle_width)
                    elif self.board2 == True and self.paddle_width == 0 and self.ball_width != 0:
                        self.sprites(self.plansza2(), ball_width=self.ball_width, ball_height=self.ball_height)
                    elif self.board2 == True and self.paddle_width != 0 and self.ball_width != 0:
                        self.sprites(self.plansza2(), self.paddle_width, self.ball_width, self.ball_height)

                    elif self.board3 == True and self.paddle_width == 0 and self.ball_width == 0:
                        self.sprites(self.plansza3())
                    elif self.board3 == True and self.paddle_width != 0 and self.ball_width == 0:
                        self.sprites(self.plansza3(), self.paddle_width)
                    elif self.board3 == True and self.paddle_width == 0 and self.ball_width != 0:
                        self.sprites(self.plansza3(), ball_width=self.ball_width, ball_height=self.ball_height)
                    elif self.board3 == True and self.paddle_width != 0 and self.ball_width != 0:
                        self.sprites(self.plansza3(), self.paddle_width, self.ball_width, self.ball_height)

                    elif self.board1 == False and self.board2 == False and self.board3 == False and self.paddle_width == 0 and self.ball_width == 0:
                        self.plansza1()
                        self.sprites()
                    elif self.board1 == False and self.board2 == False and self.board3 == False and self.paddle_width != 0 and self.ball_width == 0:
                        self.plansza1()
                        self.sprites(self.paddle_width)
                    elif self.board1 == False and self.board2 == False and self.board3 == False and self.paddle_width == 0 and self.ball_width != 0:
                        self.plansza1()
                        self.sprites(ball_width=self.ball_width, ball_height=self.ball_height)
                    elif self.board1 == False and self.board2 == False and self.board3 == False and self.paddle_width != 0 and self.ball_width != 0:
                        self.plansza1()
                        self.sprites(paddle_width=self.paddle_width, ball_width=self.ball_width, ball_height=self.ball_height)

                    Functions.reset_ball(self)
                    self.gameLoop()

                if action == "next":
                    Pages.second_options(self)

                if action == "about author":
                    Pages.about_author(self)

                if action == "quit":
                    Functions.invite(self)

                if action == "back to menu":
                    Pages.start(self)

                if action == "options":
                    self.options()

                if action == "back to options":
                    self.options()

        else:
            pygame.draw.rect(self.screen, inactive_color, (x, y, width, height))

        Functions.text_to_button(self,text, text_color, x, y, width, height, size)


    def plansza1(self):
        """Rysuje pierwszą planszę."""

        i = 5
        j = self.screen_height / 2 - 50

        while j > 0:

            block = Blocks(i, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            i = i + 33.75
            j = j - 30

        i = 90
        j = self.screen_height / 2 - 50
        while j > 70:

            block = Blocks(i, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            i = i + 33.75
            j = j - 30

        i = self.screen_width - 85
        j = self.screen_height / 2 - 50
        while j > 0:

            block = Blocks(i, j, 'data/wood_brick.png')
            self.BlocksSprite.add(block)
            i = i - 33.75
            j = j - 30

        i = self.screen_width - 2 * 85
        j = self.screen_height / 2 - 50
        while j > 70:

            block = Blocks(i, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            i = i - 33.75
            j = j - 30

        j = self.screen_height / 2 + 50
        while j > 0:

            block = Blocks(360, j, 'data/wood_brick.png')
            self.BlocksSprite.add(block)
            j = j - 30

        j = self.screen_height / 2 + 50
        while j > 150:

            block = Blocks(275, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            j = j - 30

        j = self.screen_height / 2 + 50

        while j > 150:

            block = Blocks(445, j, 'data/wood_brick.png')
            self.BlocksSprite.add(block)
            j = j - 30

        self.counter = len(self.BlocksSprite)

    def plansza2(self):
        """Rysuje drugą planszę."""

        j = self.screen_height / 2 - 50
        while j > 30:

            block = Blocks(10, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            j = j - 60

        j = self.screen_height / 2 - 25
        while j > 30:

            block = Blocks(90, j, 'data/wood_brick.png')
            self.BlocksSprite.add(block)
            j = j - 60

        j = self.screen_height / 2 - 50
        while j > 30:

            block = Blocks(170, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            j = j - 60

        ####

        j = self.screen_height / 2 - 50
        while j > 30:

            block = Blocks(self.screen_width-90, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            j = j - 60

        j = self.screen_height / 2 - 25
        while j > 30:

            block = Blocks(self.screen_width-170, j, 'data/wood_brick.png')
            self.BlocksSprite.add(block)
            j = j - 60

        j = self.screen_height / 2 - 50
        while j > 30:

            block = Blocks(self.screen_width-250, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            j = j - 60

        ###

        j = self.screen_height / 2 - 50
        for k in range(8):
            block = Blocks(270, j, 'data/light_wood_brick.png')
            self.BlocksSprite.add(block)
            j = j - 30

        j = self.screen_height / 2 - 50
        for k in range(8):
            block = Blocks(450, j, 'data/light_wood_brick.png')
            self.BlocksSprite.add(block)
            j = j - 30

        block = Blocks(360, 40, 'data/light_wood_brick.png')
        self.BlocksSprite.add(block)
        block = Blocks(360, 250, 'data/light_wood_brick.png')
        self.BlocksSprite.add(block)

        i = 10
        while i < self.screen_width:
            block = Blocks(i, self.screen_height/2+20, 'data/light_wood_brick.png')
            self.BlocksSprite.add(block)
            i = i + 175

        i = 100
        while i < self.screen_width:
            block = Blocks(i, self.screen_height/2+55, 'data/light_wood_brick.png')
            self.BlocksSprite.add(block)
            i = i + 175

        self.counter = len(self.BlocksSprite)

    def plansza3(self):
        """Rysuje trzecią planszę."""


        for i in range(2):
            self.add_speed = Extensions(random.randrange(30, self.screen_width-30),
                                        random.randrange(30, self.screen_height / 2), "data/add_speed.png")
            self.AddSpeedSprite.add(self.add_speed)

        for i in range(2):
            self.add_speed = Extensions(random.randrange(30, self.screen_width-30),
                                        random.randrange(30, self.screen_height / 2), "data/substract_speed.png")
            self.SubstractSpeedSprite.add(self.add_speed)


        i = 10
        j = 35
        while i < self.screen_width - 10:
            block = Blocks(i, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            i = i + 87.5

        i = 97.5
        j = 70
        while i < self.screen_width - 97.5:
            block = Blocks(i, j, 'data/wood_brick.png')
            self.BlocksSprite.add(block)
            i = i + 87.5

        i = 185
        j = 105
        while i < self.screen_width - 185:
            block = Blocks(i, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            i = i + 87.5

        i = 272.5
        j = 140
        while i < self.screen_width - 272.5:
            block = Blocks(i, j, 'data/wood_brick.png')
            self.BlocksSprite.add(block)
            i = i + 87.5

        ####

        block = Blocks(360, 175, 'data/gray_brick.png')
        self.BlocksSprite.add(block)

        ####

        i = 272.5
        j = 210
        while i < self.screen_width - 272.5:
            block = Blocks(i, j, 'data/wood_brick.png')
            self.BlocksSprite.add(block)
            i = i + 175

        i = 185
        j = 245
        while i < self.screen_width - 185:
            block = Blocks(i, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            i = i + 175

        i = 97.5
        j = 280
        while i < self.screen_width - 97.5:
            block = Blocks(i, j, 'data/wood_brick.png')
            self.BlocksSprite.add(block)
            i = i + 175

        i = 10
        j = 315
        while i < self.screen_width - 10:
            block = Blocks(i, j, 'data/gray_brick.png')
            self.BlocksSprite.add(block)
            i = i + 175

        ####

        i = 10
        for k in range(3):
            block = Blocks(i, 175, 'data/light_wood_brick.png')
            self.BlocksSprite.add(block)
            i = i + 87.5

        j = 140
        for k in range(2):
            block = Blocks(97.5, j, 'data/light_wood_brick.png')
            self.BlocksSprite.add(block)
            j = j + 70

        i = 535
        for k in range(3):
            block = Blocks(i, 175, 'data/light_wood_brick.png')
            self.BlocksSprite.add(block)
            i = i + 87.5

        j = 140
        for k in range(2):
            block = Blocks(622.5, j, 'data/light_wood_brick.png')
            self.BlocksSprite.add(block)
            j = j + 70

        self.counter = len(self.BlocksSprite)

