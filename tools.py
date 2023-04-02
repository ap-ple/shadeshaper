import os
import pygame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

X = 0
Y = 1

def import_frames(path):
  frames = []

  for _, _, files in os.walk(path):
    for frame in files:
      frames.append(pygame.image.load(os.path.join(path, frame)).convert_alpha())

  return frames

def rect_inside_polygon(rect, points):
  polygon = Polygon(points)
  for point in (rect.topleft, rect.topright, rect.bottomleft, rect.bottomright):
    if polygon.contains(Point(*point)):
      return True

  return False