import pygame
from pygame.locals import *
import random
from colors import colors

pygame.init()
class Ball:
    def __init__(self, WIDTH, HEIGHT, r = 20, color = 'red'):
        self.x = WIDTH // 2# random.randint(0 + r * 3, WIDTH - r)
        self.y = HEIGHT // 2# random.randint(0 + r, HEIGHT - r)
        self.vel_x = -2 # random.randint(-1, 1) 
        self.vel_y = 2 # random.randint(1)
        self.r = r
        self.color = colors.get(color)
        

    def show(self, screen):
         pygame.draw.circle(screen, self.color
         , (self.x, self.y), self.r)

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

    def show(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, screen):
        if self.y >= 0 and self.direction == -1:
            self.y += self.vel * self.direction
        
        elif self.y + self.height <= screen.get_height() and self.direction == 1:
            self.y += self.vel * self.direction
            
    def collision(self, b, screen):  
        if b.vel_x > 0:
            return

        if b.x - b.r <= self.x + self.width: 
            if b.y + b.r >= self.y and b.y - b.r <= self.y + self.height: 
                b.change_direction() 
            else:
                print(b.vel_x, b.y, self.y + self.height)
                b.reset(screen)
class PaddleEnemy(PaddlePlayer):
    def __init__(self, WIDTH, HEIGHT, x):
        super().__init__(WIDTH, HEIGHT, x)

    def move(self, screen, ball):
        if ball.x < screen.get_width() // 2 or ball.vel_x < 0:
            return
        center_y = self.y + self.height // 2 # center of the paddle
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
                ball.recently_collided = True
                ball.change_direction()
            else:
                ball.reset(screen)

class Game:
    WIDTH = 640
    HEIGHT = 480
    OFFSET = 20
    clock = pygame.time.Clock()
    FPS = 30
    def __init__(self):
        self.paddle1 = PaddlePlayer(self.WIDTH, self.HEIGHT, self.OFFSET) # player
        self.paddle2 = PaddleEnemy(self.WIDTH, self.HEIGHT, self.WIDTH - 40) # bot
        self.b = Ball(self.WIDTH, self.HEIGHT)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True

    def run(self):
        self.clock.tick(self.FPS)
        if not self.running:
            return

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = 0
            elif event.type == pygame.KEYDOWN:
                print(event.key)
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

        self.show()
                
    def show(self):
        self.screen.fill((120, 120, 120))

        self.b.show(self.screen)
        self.b.move(self.screen)

        self.paddle1.collision(self.b,self. screen)
        self.paddle1.show(self.screen)
        self.paddle1.move(self.screen)
        
        self.paddle2.collision(self.b, self.screen)
        self.paddle2.move(self.screen, self.b)
        self.paddle2.show(self.screen)
    
        pygame.display.flip()
    
game = Game()
while game.running:
    game.run()

pygame.quit()

  