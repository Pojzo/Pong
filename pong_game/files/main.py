import pygame
from pygame.locals import *
import random
from colors import colors

pygame.init()
pygame.font.init()


class Ball:
    def __init__(self, WIDTH, HEIGHT, r=20, color='red'):
        self.x = WIDTH // 2  # random.randint(0 + r * 3, WIDTH - r)
        self.y = HEIGHT // 2  # random.randint(0 + r, HEIGHT - r)
        self.vel_x = -2  # random.randint(-1, 1)
        self.vel_y = 2  # random.randint(1)
        self.r = r
        self.color = colors.get(color)

    def show(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def move(self, screen):
        self.x += self.vel_x
        self.y += self.vel_y

        if (self.y + self.r) >= screen.get_height() or (self.y - self.r) <= 0:
            self.vel_y *= -1

    def change_direction(self):
        self.vel_x *= -1

    def reset(self, screen):
        self.x = screen.get_width() // 2


class PaddlePlayer:
    def __init__(self, WIDTH, HEIGHT, x):
        self.width = 20
        self.height = 70
        self.x = x
        self.y = HEIGHT // 2
        self.vel = 3
        self.KEYUP = False
        self.direction = 0
        self.color = colors.get('green')
        self.score = 0

    def show(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))

    def move(self, screen):
        if self.y >= 0 and self.direction == -1:
            self.y += self.vel * self.direction

        elif self.y + self.height <= screen.get_height() and self.direction == 1:
            self.y += self.vel * self.direction

    def add_score(self):
        self.score += 1

    def collision(self, b, screen):
        if b.vel_x > 0:
            return

        if b.x - b.r <= self.x + self.width:
            if b.y + b.r >= self.y and b.y - b.r <= self.y + self.height:
                b.change_direction()
            else:
                self.add_score()
                b.reset(screen)


class PaddleEnemy(PaddlePlayer):
    def __init__(self, WIDTH, HEIGHT, x):
        super().__init__(WIDTH, HEIGHT, x)

    def move(self, screen, ball):
        if ball.x < screen.get_width() // 2 or ball.vel_x < 0:
            return
        center_y = self.y + self.height // 2  # center of the paddle
        if center_y > ball.y:
            if not self.y < 0:
                self.y -= self.vel
        else:
            if not self.y + self.height > screen.get_height():
                self.y += self.vel

    def collision(self, ball, screen):
        if ball.vel_x < 0:
            return
        if ball.x + ball.r >= self.x:
            if ball.y >= self.y and ball.y <= self.y + self.height:
                ball.change_direction()
            else:
                self.add_score()
                ball.reset(screen)


class Game:
    WIDTH = 640
    HEIGHT = 480
    OFFSET = 20
    clock = pygame.time.Clock()
    FPS = 200

    def __init__(self):
        self.paddle1 = PaddlePlayer(
            self.WIDTH, self.HEIGHT, self.OFFSET)  # player
        self.paddle2 = PaddleEnemy(
            self.WIDTH, self.HEIGHT, self.WIDTH - 40)  # bot
        self.b = Ball(self.WIDTH, self.HEIGHT)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True
        self.font = pygame.font.SysFont('Arial', 30)

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

        self.paddle1.move(self.screen)
        self.paddle1.collision(self.b, self. screen)

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


game = Game()
while game.running:
    game.run()

pygame.quit()
