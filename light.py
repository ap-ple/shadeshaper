import pygame

class Light:

  def __init__(self, position, points, color):

    self.position = position
    self.points = points
    self.color = color

  def draw(self, screen):

    pygame.draw.polygon(screen, self.color, self.points)
