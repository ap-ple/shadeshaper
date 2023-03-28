import os
import pygame

def import_frames(path):
  frames = []

  for _, _, files in os.walk(path):
    for frame in files:
      frames.append(pygame.image.load(os.path.join(path, frame)))

  return frames