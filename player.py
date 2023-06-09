import pygame
import os
from tools import import_frames, rect_inside_polygon

class Player(pygame.sprite.Sprite):

  def __init__(self, position):

    super().__init__()

    self.animations = {"idle": [], "fading":[], "running": [], "jumping": [], "falling": []}
    self.frame = 0
    self.animation_speed = 0.1

    self.goal_reached = False
    self.fading = False
    self.failed = False
    self.moved = False

    for animation in self.animations.keys():
      self.animations[animation] = import_frames("assets/character/" + animation)
    
    self.animation = self.animations["idle"]
    self.image = self.animation[self.frame]
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

    if not self.fading:
      # run inputs
      if keys_pressed[pygame.K_r]:
        self.failed = True
      run_current_speed = self.run_speed
      for key, direction in self.run_keys.items():
        if keys_pressed[key]:
          self.moved = True
          self.direction = direction
          self.run_speed += (self.run_max_speed - abs(run_current_speed)) * self.run_accel * self.direction
      # jump input
      if self.jump_timer > 0:
        self.jump_timer -= 1
      elif self.grounded:
        if keys_pressed[self.jump_key]:
          self.moved = True
          self.grounded = False
          self.jump_speed = self.jump_power

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
              self.goal_reached = True
            return "top"
          elif not self.grounded:
            self.body.top = cell.body.bottom
            self.jump_timer = 20
            return "bottom"

  def move(self, world, light):

    if not self.fading:
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
        self.fall_speed = self.fall_start_speed

      # jumping
      if not self.falling and not self.grounded:
        self.body.y -= self.jump_speed * self.jump_accel
        self.jump_speed *= 1 - self.jump_accel
        
        if self.jump_speed < self.jump_apex or self.vertical_collide(world) == "bottom":
          self.falling = True
          self.fall_speed = self.fall_start_speed

      # falling
      if self.falling:
        self.body.y += self.fall_speed
        self.fall_speed *= self.fall_accel
        if self.fall_speed > self.fall_max_speed:
          self.fall_speed = self.fall_max_speed
        if self.vertical_collide(world) == "top":
          self.falling = False
          self.grounded = True

      if rect_inside_polygon(self.body, light.points):
        self.fading = True

  def animate(self):
    if self.fading:
      if self.animation != self.animations["fading"]:
        self.animation = self.animations["fading"]
        self.animation_speed = 0.2
        self.frame = 0
    elif abs(self.run_speed) < self.run_min_speed:
      if self.animation != self.animations["idle"]:
        self.animation = self.animations["idle"]
        self.animation_speed = 0.1
        self.frame = 0

    self.frame += self.animation_speed
    if self.frame >= len(self.animation):
      if self.fading:
        self.failed = True
        self.frame -= self.animation_speed
      else:
        self.frame = 0

    image = self.animation[int(self.frame)]

    if self.direction < 0:
      image = pygame.transform.flip(image, True, False)
    
    self.image = image

  def draw(self, screen):

    screen.blit(self.image, (self.body.x - self.image_x_offset, self.body.y - self.image_y_offset))