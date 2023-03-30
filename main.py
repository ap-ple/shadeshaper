import pygame
import sys

from player import Player
from world import World

WIDTH, HEIGHT = 1920, 1080

def main():
  print("Welcome to Shadeshaper! Use A and D to move, and SPACE to jump")

  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Shadeshaper')

  player = Player((WIDTH / 2, HEIGHT / 2))
  world = World(WIDTH, HEIGHT, 30)
  clock = pygame.time.Clock()

  while True:
    # events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit("\nThank you for playing!")
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          world.toggle_cell(*pygame.mouse.get_pos())

    # inputs
    keys_pressed = pygame.key.get_pressed()
    player.check_inputs(keys_pressed)

    # movement
    player.move(world)
    player.animate()

    # update frame
    screen.fill("grey")
    if pygame.mouse.get_pressed()[2]:
      pygame.draw.polygon(screen, "white", world.calculate_light(pygame.mouse.get_pos()))
    world.draw(screen)
    player.draw(screen)
    pygame.display.update()

    # update clock
    clock.tick(60)

if __name__ == "__main__": main()