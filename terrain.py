import pygame

class Terrain:

  def __init__(self, x, y, width, height):

    self.body = pygame.Rect(x, y, width, height)
    self.image = pygame.Surface((width, height))
    self.image.fill((0, 0, 0))
    
  def draw(self, screen):

    screen.blit(self.image, (self.body.x, self.body.y))