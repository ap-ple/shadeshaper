import pygame

from level import Level

SCREEN_SIZE = (1920, 1080)

def main():
  print("Welcome to Shadeshaper! Use A and D to move, SPACE to jump, R to restart, and left click to move the light source")

  screen = pygame.display.set_mode(SCREEN_SIZE)
  pygame.display.set_caption('Shadeshaper')
  Level("title").play(screen, *SCREEN_SIZE)

if __name__ == "__main__": main()