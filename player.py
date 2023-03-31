import pygame
import os
from tools import import_frames

class Player(pygame.sprite.Sprite):

  def __init__(self, position):

    super().__init__()

    self.animations = {"idle": [], "run": [], "jump": [], "fall": []}
    self.frame = 0
    self.animation_speed = 0.1

    self.goal = False

    for animation in self.animations.keys():
      self.animations[animation] = import_frames("assets/character/" + animation)
    
    self.image = self.animations["idle"][self.frame]
    self.size = 64
    self.image_x_offset = 13
    self.image_y_offset = 13
    self.body = pygame.Rect(*position, self.size - (self.image_x_offset * 2), self.size - self.image_y_offset)
    self.direction = 1

    self.run_keys = {pygame.K_a: -1, pygame.K_d: 1}
    self.run_speed = 0
    self.run_accel = 0.07
    self.run_decel = 0.8
    self.run_min_speed = 0.8
    self.run_max_speed = 28

    self.jump_key = pygame.K_SPACE
    self.jump_timer = 0
    self.jump_speed = 0
    self.jump_accel = 0.15
    self.jump_apex = 5
    self.jump_power = 150
    
    self.fall_start_speed = 3
    self.fall_speed = self.fall_start_speed * 1
    self.fall_accel = 1.13
    self.fall_max_speed = 20
    self.grounded = False
    self.falling = True

  def check_inputs(self, keys_pressed):

    # run inputs
    run_current_speed = self.run_speed * 1
    for key, direction in self.run_keys.items():
      if keys_pressed[key]:
        self.direction = direction
        self.run_speed += (self.run_max_speed - abs(run_current_speed)) * self.run_accel * self.direction
    # jump input
    if self.jump_timer > 0:
      self.jump_timer -= 1
    elif self.grounded:
      if keys_pressed[self.jump_key]:
        self.grounded = False
        self.jump_speed = self.jump_power * 1

  def horizontal_collide(self, world):

    for cell in world.cells:
      if cell.exists:
        if self.body.colliderect(cell.body):
          if self.run_speed < 0: # left
            self.body.left = cell.body.right
            self.run_speed = 0
          elif self.run_speed > 0: # right
            self.body.right = cell.body.left
            self.run_speed = 0

  def vertical_collide(self, world):

    for cell in world.cells:
      if cell.exists:
        if self.body.colliderect(cell.body):
          if self.grounded or self.falling:
            self.body.bottom = cell.body.top
            if cell.goal:
              self.goal = True
            return "top"
          elif not self.grounded:
            self.body.top = cell.body.bottom
            self.jump_timer = 20
            return "bottom"

  def move(self, world):

    # running
    if abs(self.run_speed) > self.run_min_speed:
      self.body.x += self.run_speed
      self.horizontal_collide(world)  
    self.run_speed *= self.run_decel

    # fell off platform
    self.body.y += 1
    if self.grounded and self.vertical_collide(world) != "top":
      self.falling = True
      self.grounded = False
      self.fall_speed = self.fall_start_speed * 1

    # jumping
    if not self.falling and not self.grounded:
      self.body.y -= self.jump_speed * self.jump_accel
      self.jump_speed *= 1 - self.jump_accel
      
      if self.jump_speed < self.jump_apex or self.vertical_collide(world) == "bottom":
        self.falling = True
        self.fall_speed = self.fall_start_speed * 1

    # falling
    if self.falling:
      self.body.y += self.fall_speed
      self.fall_speed *= self.fall_accel
      if self.fall_speed > self.fall_max_speed:
        self.fall_speed = self.fall_max_speed * 1
      if self.vertical_collide(world) == "top":
        self.falling = False
        self.grounded = True

  def animate(self):
    animation = self.animations["idle"]

    self.frame += self.animation_speed
    if self.frame >= len(animation):
      self.frame = 0

    image = animation[int(self.frame)]

    if self.direction < 0:
      image = pygame.transform.flip(image, True, False)
    
    self.image = image

  def draw(self, screen):

    screen.blit(self.image, (self.body.x - self.image_x_offset, self.body.y - self.image_y_offset))