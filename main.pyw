import pygame
import sys

from player import Player
from world import World
from light import Light

WIDTH, HEIGHT = 1920, 1080
FPS = 60

def main():
  print("Welcome to Shadeshaper! Use A and D to move, SPACE to jump, and right click to place the light source")

  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Shadeshaper')

  with open("levels/title.lvl", "r") as file:
    tile_map = file.readlines()

  world = World(WIDTH, HEIGHT, 30, tile_map)
  player = Player(world.player_position)
  light = None
  clock = pygame.time.Clock()

  while True:
    # events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit("\nThank you for playing!")
      elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_position = pygame.mouse.get_pos()
        if event.button == 3: # rmb
          light = Light(mouse_position, world.calculate_light(mouse_position), "white")

    # inputs
    keys_pressed = pygame.key.get_pressed()
    player.check_inputs(keys_pressed)

    # movement
    player.move(world)
    player.animate()

    if player.goal:
      pass

    # update frame
    screen.fill("grey")
    world.draw(screen)
    if light is not None:
      light.draw(screen)
    player.draw(screen)
    pygame.display.update()

    # update clock
    clock.tick(60)

if __name__ == "__main__": main()
