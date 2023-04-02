import pygame

from level import Level

def main():
  print("Welcome to Shadeshaper! Use A and D to move, SPACE to jump, R to restart, and left click to move the light source")

  screen = pygame.display.set_mode()
  pygame.display.set_caption('Shadeshaper')
  Level("title").play(screen, *screen.get_size())

if __name__ == "__main__": main()