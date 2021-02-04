import pygame
from pygame.locals import *
import random
from colors import colors

pygame.init()
class Ball:
    def __init__(self, WIDTH, HEIGHT, r = 20, color = 'red'):
        self.x = WIDTH // 2# random.randint(0 + r * 3, WIDTH - r)
        self.y = HEIGHT // 2# random.randint(0 + r, HEIGHT - r)
        self.vel_x = -0.3 # random.randint(-1, 1) 
        self.vel_y = 0.3 # random.randint(1)
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
        self.vel = 1
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
        if center_y > b.y:
            if not self.y < 0:
                self.y -= self.vel
        else:
            if not self.y + self.height > screen.get_height():
                self.y += self.vel
            
    def collision(self, b, screen):
        if b.vel_x < 0:
            return
        if b.x + b.r >= self.x:
            if b.y >= self.y and b.y <= self.y + self.height:
                b.recently_collided = True
                b.change_direction()
            else:
                b.reset(screen)


WIDTH = 640
HEIGHT = 480
OFFSET = 20
paddle1 = PaddlePlayer(WIDTH, HEIGHT, OFFSET) # player
paddle2 = PaddleEnemy(WIDTH, HEIGHT, WIDTH - 40) # bot

screen = pygame.display.set_mode((WIDTH, HEIGHT))

b = Ball(WIDTH, HEIGHT)

running = True

while running:
    if b.vel_x == 0:
        continue
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        elif event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == pygame.K_UP:
                paddle1.KEYUP = True
                paddle1.direction = -1

            elif event.key == pygame.K_DOWN:
                paddle1.KEYUP = True
                paddle1.direction = 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                paddle1.KEYUP = False
                paddle1.direction = 0
            

    screen.fill((120, 120, 120))

    b.show(screen)
    b.move(screen)

    paddle1.collision(b, screen)
    paddle1.show(screen)
    paddle1.move(screen)
    

    paddle2.collision(b, screen)
    paddle2.move(screen, b)
    paddle2.show(screen)
 
    pygame.display.flip()
    
pygame.quit()

  
