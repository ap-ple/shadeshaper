import pygame
import os
from tools import import_frames

class Player(pygame.sprite.Sprite):

  def __init__(self, pos):

    super().__init__()

    self.animations = {"idle": [], "run": [], "jump": [], "fall": []}
    self.frame = 0
    self.animation_speed = 0.1

    for animation in self.animations.keys():
      self.animations[animation] = import_frames("assets/character/" + animation)
    
    self.image = self.animations["idle"][self.frame]
    self.size = 64
    self.image_x_offset = 13
    self.body = pygame.Rect(*pos, self.size - (self.image_x_offset * 2), self.size)
    self.direction = 1

    self.move_keys = {pygame.K_a: -1, # left
                      pygame.K_d: 1,  # right
                      }
    self.run_speed = 0
    self.run_accel = 0.15
    self.run_decel = 0.75
    self.run_min_speed = 0.8
    self.run_max_speed = 23

    self.jump_key = pygame.K_SPACE
    self.jump_cooldown = 20
    self.jump_timer = 0
    self.jump_speed = 0
    self.jump_accel = 0.2
    self.jump_apex = 5
    self.jump_power = 125
    
    self.fall_start_speed = 3
    self.fall_speed = self.fall_start_speed * 1
    self.fall_accel = 1.15
    self.fall_max_speed = 22
    self.grounded = False
    self.falling = True

  def check_inputs(self, keys_pressed):

    # run inputs
    run_current_speed = self.run_speed * 1
    for key, direction in self.move_keys.items():
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
        self.jump_timer += self.jump_cooldown

  def horizontal_collide(self, terrain):

    for obstacle in terrain:
      if self.body.colliderect(obstacle.body):
        if self.run_speed < 0: # left
          self.body.left = obstacle.body.right
        elif self.run_speed > 0: # right
          self.body.right = obstacle.body.left

  def vertical_collide(self, terrain):

    for obstacle in terrain:
      if self.body.colliderect(obstacle.body):
        if self.grounded or self.falling:
          self.body.bottom = obstacle.body.top
          return "top"
        elif not self.grounded:
          self.body.top = obstacle.body.bottom
          return "bottom"

  def move(self, terrain):

    # running
    if abs(self.run_speed) > self.run_min_speed:
      self.body.x += self.run_speed
      self.horizontal_collide(terrain)  
    self.run_speed *= self.run_decel

    # fell off platform
    self.body.y += 1
    if self.grounded and self.vertical_collide(terrain) != "top":
      self.falling = True
      self.grounded = False
      self.fall_speed = self.fall_start_speed * 1

    # jumping
    if not self.falling and not self.grounded:
      self.body.y -= self.jump_speed * self.jump_accel
      self.jump_speed *= 1 - self.jump_accel
      
      if self.jump_speed < self.jump_apex or self.vertical_collide(terrain) == "bottom":
        self.falling = True
        self.fall_speed = self.fall_start_speed * 1

    # falling
    if self.falling:
      self.body.y += self.fall_speed
      self.fall_speed *= self.fall_accel
      if self.fall_speed > self.fall_max_speed:
        self.fall_speed = self.fall_max_speed * 1
      if self.vertical_collide(terrain) == "top":
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

    screen.blit(self.image, (self.body.x - self.image_x_offset, self.body.y))