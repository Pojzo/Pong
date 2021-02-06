import pygame
from pygame.locals import *
import random
from colors import colors
from objects import PaddlePlayer, PaddleEnemy, Ball



class Game:
    WIDTH = 640
    HEIGHT = 480
    OFFSET = 20
    clock = pygame.time.Clock()
    FPS = 200

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.paddle1 = PaddlePlayer(
            self.WIDTH, self.HEIGHT, self.OFFSET)  # player
        self.paddle2 = PaddleEnemy(
            self.WIDTH, self.HEIGHT, self.WIDTH - 40)  # bot
        self.b = Ball(self.WIDTH, self.HEIGHT)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True
        self.font = pygame.font.SysFont('Arial', 30)
        self.local = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.paddle1.KEYUP = True
                    self.paddle1.direction = -1

                elif event.key == pygame.K_DOWN:
                    self.paddle1.KEYUP = True
                    self.paddle1.direction = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.paddle1.KEYUP = False
                    self.paddle1.direction = 0

    def move_objects(self):
        self.b.move(self.screen)

        self.paddle1.move(self.screen, self.b, autonomy=True)
        self.paddle1.collision(self.b, self. screen)

        if self.local:
            self.paddle2.move(self.screen, self.b)
        self.paddle2.collision(self.b, self.screen)

    def run(self):
        if not self.running:
            return

        self.clock.tick(self.FPS)
        self.handle_events()
        self.move_objects()
        self.show()

    def show_background(self, width=10, height=20, gap=10):

        self.screen.fill(colors.get('gray'))
        lines = self.screen.get_height() // height
        color = colors.get('white')
        y = gap // 2
        for i in range(lines):
            pygame.draw.rect(
                self.screen, color, (self.screen.get_width()//2 - width, y, width, height))
            y += height + gap

    def show_objects(self):
        self.b.show(self.screen)
        self.paddle1.show(self.screen)
        self.paddle2.show(self.screen)

    def draw_score(self):
        score1 = self.paddle2.score
        score2 = self.paddle1.score
        surface1 = self.font.render(str(score1), False, (0, 0, 0))
        surface2 = self.font.render(str(score2), False, (0, 0, 0))
        self.screen.blit(surface1, (self.screen.get_width() // 4, 0))
        self.screen.blit(surface2, (self.screen.get_width() // 4 * 3 - 30, 0))

    def show(self):
        self.show_background()
        self.show_objects()
        self.draw_score()
        pygame.display.flip()

    def receive_message(self, msg):
        value = 0
        self.paddle2.move_by_value(value, self.screen)



