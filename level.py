import pygame
import sys

from player import Player
from world import World
from light import Light

class Level:

  def __init__(self, name):

    with open(f"levels/{name}.lvl", "r") as file:
      self.tile_map = file.readlines()

    self.name = name

  def play(self, screen, screen_width, screen_height):

    player = Player((0, 0))

    while not player.goal_reached:
      world = World(screen_width, screen_height, 30, self.tile_map)
      player = Player(world.player_position)
      light = Light(exists=False)
      clock = pygame.time.Clock()

      while not player.failed and not player.goal_reached:
        # events
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit("\nThank you for playing!")          

        # inputs + movement
        if light.exists:
          keys_pressed = pygame.key.get_pressed()
          player.check_inputs(keys_pressed)

        if not player.moved:
          mouse_pressed = pygame.mouse.get_pressed()
          if mouse_pressed[0]: #lmb
            mouse_position = pygame.mouse.get_pos()
            light = Light(world, mouse_position)
        else:
          player.move(world, light)
          player.animate()

        # update frame
        screen.fill("grey")
        light.draw(screen)
        world.draw(screen)
        player.draw(screen)
        pygame.display.update()

        # update clock
        clock.tick(60)

    if self.name == "title":
      if player.body.x < 700:
        goal = "level_1"
      elif player.body.x < 1600:
        goal = "level_3"
      else:
        goal = "level_2"
      Level(goal).play(screen, screen_width, screen_height)
    else:
      Level("title").play(screen, screen_width, screen_height)
