import pygame
import sys

from player import Player
from terrain import Terrain

WIDTH, HEIGHT = 1920, 1080

def main():
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Shadeshaper')

  player = Player((1000, 500))
  terrain = [
            # borders
            Terrain(0,     0,      WIDTH, 1),
            Terrain(0,     HEIGHT, WIDTH, 1),
            Terrain(0,     0,      1,     HEIGHT),
            Terrain(WIDTH, 0,      1,     HEIGHT),
            # test platforms
            Terrain(100, 1010, 200, 20),
            Terrain(300, 950, 200, 20),
            Terrain(500, 890, 200, 20),
            Terrain(100, 890, 200, 20),
            Terrain(700, 830, 200, 20),
            Terrain(900, 770, 200, 20),
            Terrain(1100, 710, 200, 20),
            Terrain(1300, 650, 200, 20),
            Terrain(1500, 590, 200, 20),
            Terrain(1700, 530, 200, 20),
            Terrain(400, 1030, 300, 50),
            ]
  clock = pygame.time.Clock()

  while True:
    # events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    # inputs
    keys_pressed = pygame.key.get_pressed()
    player.check_inputs(keys_pressed)

    # movement
    player.move(terrain)
    player.animate()

    # update frame
    screen.fill("white")
    player.draw(screen)
    for obstacle in terrain:
      obstacle.draw(screen)
    pygame.display.update()

    # update clock at 60 frames per second
    clock.tick(60)

if __name__ == "__main__":
  print("Welcome to Shadeshaper")
  main()