import pygame
import sys
import os

from player import Player
from world import World
from light import Light

WIDTH, HEIGHT = 1920, 1080
FPS = 60

X = 0
Y = 1

def main():
  print("""Welcome to the Shadeshaper editor! Use A and D to move, and SPACE to jump.
You can also toggle tiles by left clicking, toggle goal tiles by middle clicking, and place a light source by right clicking.
You can also save the current map by pressing M, and a prompt will come up in the console asking for the level name.""")

  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Shadeshaper editor')
  
  with open("levels/title.lvl", "r") as file:
    tile_map = file.readlines()

  world = World(WIDTH, HEIGHT, 30, tile_map)
  player = Player(world.player_position)
  light = Light(exists=False)
  clock = pygame.time.Clock()

  while True:
    # events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_position = pygame.mouse.get_pos()
        if event.button == 1: # lmb
          light = Light(exists=False)
          world.toggle_cell(mouse_position)
        elif event.button == 2: # mmb
          light = Light(exists=False)
          world.toggle_cell(mouse_position, goal=True)
        elif event.button == 3: # rmb
          light = Light(world, mouse_position)

    # inputs
    keys_pressed = pygame.key.get_pressed()
    player.check_inputs(keys_pressed)
    if keys_pressed[pygame.K_m]:
      print("\nIf file exists, it will be overwritten.")
      level_name = input("Level name: ")
      with open(os.path.join("levels", f"{level_name}.lvl"), "w") as file:            
        for cell in world.cells:
          if cell.goal:
            file.write("G")
          elif cell.exists:
            file.write("#")
          else:
            file.write("-")

          if cell.body.width + cell.position[X] == WIDTH:
            file.write("\n")
      print("Level saved.")

    # movement
    player.move(world, Light(exists=False))
    player.animate()

    # update frame
    screen.fill("grey")
    light.draw(screen)
    world.draw(screen)
    player.draw(screen)
    pygame.display.update()

    # update clock
    clock.tick(FPS)

if __name__ == "__main__": main()
