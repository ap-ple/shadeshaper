import pygame
import math
  
X = 0
Y = 1

class Light:

  def __init__(self, world, position=None, exists=True):
    
    self.exists = exists
    self.position = position
    if self.position is None:
      self.position = (world.width * world.block_size + 32, world.height * world.block_size + 32)

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
        self.image = pygame.image.load("assets/light/light_on.png")
    if not self.exists:
      self.image = pygame.image.load("assets/light/light_off.png")
      self.points = ()

  def draw(self, screen):

    if self.exists:
      pygame.draw.polygon(screen, "white", self.points)
    
    screen.blit(self.image, (self.position[X] - 32, self.position[Y] - 32))
