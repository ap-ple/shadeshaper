import pygame
import math
  
X = 0
Y = 1

class Light:

  def __init__(self, world=None, position=None, exists=True):
    
    self.exists = exists
    
    if self.exists:
      for cell in world.cells:
        if cell.exists:
          c = cell.body
          for point in (c.topleft, c.topright, c.bottomleft, c.bottomright):
            if math.sqrt((point[X] - position[X]) ** 2 + (point[Y] - position[Y]) ** 2) < 60:
              self.exists = False
              break
      else:
        self.points = world.calculate_light(position)
        self.position = position
        self.image = pygame.image.load("assets/light/light.png")
    if not self.exists:
      self.points = ()    

  def draw(self, screen):

    if self.exists:
      pygame.draw.polygon(screen, "white", self.points)
      screen.blit(self.image, (self.position[X] - 32, self.position[Y] - 32))
