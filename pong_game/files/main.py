import pygame
from pygame.locals import *

pygame.init()
  
screen = pygame.display.set_mode((640, 480))

running = 1

while running:
  for event in pygame.event.get():
    if event.type == QUIT:
        running = 0
    else:
        pass

  screen.fill((120, 120, 120))
  pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(100, 100, 200, 200))
  pygame.display.flip()


pygame.quit()
