import pygame
import sys

pygame.init()

from player import Player
from world import World
from light import Light

font = pygame.font.Font("freesansbold.ttf", 24)

X = 0
Y = 1

class Level:

  def __init__(self, name):

    with open(f"levels/{name}.lvl", "r") as file:
      self.tile_map = file.readlines()

    self.name = name

  def play(self, screen, screen_width, screen_height, complete=False):

    player = Player((0, 0))

    while not player.goal_reached:
      game = pygame.Surface((1920, 1080))
      world = World(1920, 1080, 30, self.tile_map)
      player = Player(world.player_position)
      light = Light(position=(0, 0), exists=False)
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
            corrected_mouse_position = (int(1920 / screen_width * mouse_position[X]), int(1080 / screen_height * mouse_position[Y]))
            light = Light(world, corrected_mouse_position)
        else:
          player.move(world, light)
          player.animate()

        # update frame
        game.fill("grey")
        light.draw(game)
        world.draw(game)
        player.draw(game)

        if self.name == "title":
          if complete:
            message = "Thank you for playing!"
            message_x = 1550
          else:
            if not light.exists:
              tooltip = "Hold left click"
              tooltip_offset = 200
            else:
              tooltip = "A, D, and Space to move"
              tooltip_offset = 330

            tip = font.render(tooltip, True, "black")
            mouse_position = pygame.mouse.get_pos()
            game.blit(tip, (mouse_position[X] - tooltip_offset, mouse_position[Y] - 20))

            message = "Left click to place light, A and D to move, space to jump, and R to restart"
            message_x = 1000
            
          game.blit(font.render(message, True, "black"), (message_x, 90))

        frame = pygame.transform.scale(game, (screen_width, screen_height))
        screen.blit(frame, frame.get_rect())
        pygame.display.flip()
        pygame.display.update()

        # update clock
        clock.tick(60)

    levels = {"title": "level_1",
              "level_1": "level_2",
              "level_2": "level_3",
              "level_3": "title",}

    Level(levels[self.name]).play(screen, screen_width, screen_height, True)