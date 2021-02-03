import pygame
from pygame.locals import *
import random

pygame.init()
class Ball:
    def __init__(self, WIDTH, HEIGHT, r = 20):
        self.x = WIDTH // 2# random.randint(0 + r * 3, WIDTH - r)
        self.y = HEIGHT // 2# random.randint(0 + r, HEIGHT - r)
        self.vel_x = -0.3 # random.randint(-1, 1) 
        self.vel_y = 0.3 # random.randint(1)
        self.r = r
        self.recently_collided = False

    def show(self, screen):
         pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)

    def move(self, screen): 
        self.x += self.vel_x
        self.y += self.vel_y
        
        if (self.y + self.r) >= screen.get_height() or (self.y - self.r) <= 0:
            self.vel_y *= -1

    def change_direction(self):
        self.vel_x *= -1

    def stop(self):
        self.vel_x = 0
        self.vel_y = 0

class Paddle:
    def __init__(self, WIDTH, HEIGHT, x, type):
        self.width = 20
        self.height = 70
        self.x = x
        self.y = HEIGHT // 2
        self.vel = 1
        self.KEYUP = False
        self.direction = 0
        self.type = type # 1 - player, 0 - bot

    def show(self, screen):
        pygame.draw.rect(screen,(0, 255, 0),(self.x, self.y, self.width, self.height))

    def move(self, screen):
        if self.y >= 0 and self.direction == -1:
            self.y += self.vel * self.direction
        
        elif((self.y + self.height) <= screen.get_height() and self.direction == 1):
            self.y += self.vel * self.direction
            
    def collision(self, b, screen):   
        if b.recently_collided:
            b.recently_collided = False
            return

        if self.type: 
            if(b.x - b.r <= self.x + self.width): 
                if b.y - b.r // 2 >= self.y and b.y + b.r // 2 <= self.y + self.height: 
                    b.recently_collided = True
                    b.change_direction() 
                else:
                    b.stop()
            
        else:   
            if b.x + b.r >= self.x:
                if b.y - b.r // 2 >= self.y and b.y + b.r // 2 <= self.y + self.height:
                    b.recently_collided = True
                    b.change_direction()
                else:
                    b.stop()


WIDTH = 640
HEIGHT = 480
OFFSET = 20
paddle1 = Paddle(WIDTH, HEIGHT, OFFSET, 1) # player
paddle2 = Paddle(WIDTH, HEIGHT, WIDTH - 40, 0) # bot

screen = pygame.display.set_mode((WIDTH, HEIGHT))

b = Ball(WIDTH, HEIGHT)

running = True

while running:
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
    paddle2.move(screen)
    paddle2.show(screen)
 
    pygame.display.flip()
    
pygame.quit()

  
