import pygame
from colors import colors


class Ball:
    def __init__(self, WIDTH, HEIGHT, r=10, color='red'):
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

    def map_range(self, value, start1, stop1, start2, stop2):
        return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2

    def collide(self, paddle_start, paddle_height):
        self.vel_x *= -1

    def reset(self, screen):
        self.x = screen.get_width() // 2


class PaddlePlayer:
    def __init__(self, WIDTH, HEIGHT, x, color='black'):
        self.width = 20
        self.height = 70
        self.x = x
        self.y = HEIGHT // 2
        self.vel = 3
        self.KEYUP = False
        self.direction = 0
        self.color = colors.get(color)
        self.score = 0

    def show(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))

    def move(self, screen, ball, autonomy=False):
        if autonomy:
            if ball.x > screen.get_width() // 2 or ball.vel_x > 0:
                return
            center_y = self.y + self.height // 2  # center of the paddle
            if center_y > ball.y:
                if not self.y < 0:
                    self.y -= self.vel
            else:
                if not self.y + self.height > screen.get_height():
                    self.y += self.vel
            return
        if self.y >= 0 and self.direction == -1:
            self.y += self.vel * self.direction

        elif self.y + self.height <= screen.get_height() and self.direction == 1:
            self.y += self.vel * self.direction

    def move_by_value(self, value, screen):
        if not self.y < 0 and not self.y + self.height > screen.get_height():
            self.y += value

    def add_score(self):
        self.score += 1

    def collision(self, b, screen):
        if b.vel_x > 0:
            return

        if b.x - b.r <= self.x + self.width:
            if b.y + b.r >= self.y and b.y - b.r <= self.y + self.height:
                b.collide(self.y, self.height)
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
                ball.collide(self.y, self.height)  # pass center of the paddle
            else:
                self.add_score()
                ball.reset(screen)
