import pygame
import math

NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

X = 0
Y = 1

class Edge:

  def __init__(self):

    self.start = None
    self.end = None

class Cell:

  def __init__(self, size, position):

    self.exists = False
    self.edges = [False] * 4
    self.edge_id = [0] * 4
    self.goal = False

    self.body = pygame.Rect(*position, size, size)
    self.image = pygame.Surface((size, size))

    self.position = position

  def draw(self, screen):

    if self.goal:
      self.image.fill('chartreuse4')
    else:
      self.image.fill('black')
    screen.blit(self.image, self.position)

class World:

  def __init__(self, screen_width, screen_height, block_size, tile_map=()):

    # make sure both screen_width and screen_height are divisible by block_size
    self.width = screen_width // block_size
    self.height = screen_height // block_size
    self.block_size = block_size
    self.player_position = (screen_width // 2, screen_height // 2)

    self.cells = []

    for y in range(self.height):
      for x in range(self.width):
       self.cells.append(Cell(block_size, (x * block_size, y * block_size)))

    for x in range(self.width):
      self.cells[x].exists = True
      self.cells[self.width + x].exists = True
      self.cells[(self.height - 2) * self.width + x].exists = True
      self.cells[(self.height - 1) * self.width + x].exists = True
    for y in range(self.height):
      self.cells[y * self.width].exists = True
      self.cells[y * self.width + 1].exists = True
      self.cells[y * self.width + (self.width - 2)].exists = True
      self.cells[y * self.width + (self.width - 1)].exists = True

    for y, row in enumerate(tile_map):
      for x, tile in enumerate(row):
        if tile in "GP#":
          cell = self.cells[y * self.width + x]
          cell.exists = True
          if tile == "G":
            cell.goal = True
          elif tile == "P":
            self.player_position = (cell.position[X], cell.position[Y] - 50)

    self.set_edges()

  def set_edges(self):

    self.edges = []

    # reset edges
    for x in range(self.width):
      for y in range(self.height):
        for i in range(4):
          cell = y * self.width + x
          self.cells[cell].edges[i] = False
          self.cells[cell].edge_id[i] = 0

    for x in range(1, self.width - 1):
      for y in range(1, self.height - 1):
        cell = self.cells[y * self.width + x]
        north = self.cells[(y - 1) * self.width + x]
        south = self.cells[(y + 1) * self.width + x]
        west = self.cells[y * self.width + (x - 1)]
        east = self.cells[y * self.width + (x + 1)]

        if cell.exists:
          if not west.exists: # if no western cell, needs western edge
            if north.edges[WEST]: # northern cell has western edge, extend it
              self.edges[north.edge_id[WEST]].end[Y] += self.block_size
              cell.edge_id[WEST] = north.edge_id[WEST]
              cell.edges[WEST] = True

            else: # northern cell has no western edge, make one
              edge = Edge()
              edge.start = [x * self.block_size, y * self.block_size]
              edge.end = [edge.start[X], edge.start[Y] + self.block_size]

              edge_id = len(self.edges)
              self.edges.append(edge)

              cell.edges[WEST] = True
              cell.edge_id[WEST] = edge_id

          if not east.exists: # if no eastern cell, needs eastern edge
            if north.edges[EAST]: # northern cell has eastern edge, extend it
              self.edges[north.edge_id[EAST]].end[Y] += self.block_size
              cell.edge_id[EAST] = north.edge_id[EAST]
              cell.edges[EAST] = True

            else: # northern cell has no eastern edge, make one
              edge = Edge()
              edge.start = [x * self.block_size + self.block_size, y * self.block_size]
              edge.end = [edge.start[X], edge.start[Y] + self.block_size]

              edge_id = len(self.edges)
              self.edges.append(edge)

              cell.edges[EAST] = True
              cell.edge_id[EAST] = edge_id

          if not north.exists: # if no northern cell, needs northern edge
            if west.edges[NORTH]: # western cell has northern edge, extend it
              self.edges[west.edge_id[NORTH]].end[X] += self.block_size
              cell.edge_id[NORTH] = west.edge_id[NORTH]
              cell.edges[NORTH] = True

            else: # western cell has no northern edge, make one
              edge = Edge()
              edge.start = [x * self.block_size, y * self.block_size]
              edge.end = [edge.start[X] + self.block_size, edge.start[Y]]

              edge_id = len(self.edges)
              self.edges.append(edge)

              cell.edges[NORTH] = True
              cell.edge_id[NORTH] = edge_id

          if not south.exists: # if no southern cell, needs southern edge
            if west.edges[SOUTH]: # western cell has southern edge, extend it
              self.edges[west.edge_id[SOUTH]].end[X] += self.block_size
              cell.edge_id[SOUTH] = west.edge_id[SOUTH]
              cell.edges[SOUTH] = True

            else: # western cell has no southern edge, make one
              edge = Edge()
              edge.start = [x * self.block_size, y * self.block_size + self.block_size]
              edge.end = [edge.start[X] + self.block_size, edge.start[Y]]

              edge_id = len(self.edges)
              self.edges.append(edge)

              cell.edges[SOUTH] = True
              cell.edge_id[SOUTH] = edge_id

  def calculate_light(self, source):

    light = []

    for edge in self.edges:
      for i in range(2):
        ray = []
        ray.append((edge.start[X] if i == 0 else edge.end[X]) - source[X])
        ray.append((edge.start[Y] if i == 0 else edge.end[Y]) - source[Y])

        base_angle = math.atan2(ray[Y], ray[X])
        offset = 0.0001

        for r in range(3):
          if r == 0: angle = base_angle - offset
          if r == 1: angle = base_angle
          if r == 2: angle = base_angle + offset

          ray[X] = math.cos(angle)
          ray[Y] = math.sin(angle)

          min_t1 = float('inf')
          min_point = [0, 0]
          min_angle = 0
          valid = False

          for e in self.edges:
            segment = []
            segment.append(e.end[X] - e.start[X])
            segment.append(e.end[Y] - e.start[Y])

            if abs(segment[X] - ray[X]) > 0 and abs(segment[Y] - ray[Y]) > 0:
              t2 = (ray[X] * (e.start[Y] - source[Y]) + (ray[Y] * (source[X] - e.start[X]))) / (segment[X] * ray[Y] - segment[Y] * ray[X])
              t1 = (e.start[X] + segment[X] * t2 - source[X]) / ray[X]

              if t1 > 0 and t2 >= 0 and t2 <= 1:
                if t1 < min_t1:
                  min_t1 = t1
                  min_point[X] = source[X] + ray[X] * t1
                  min_point[Y] = source[Y] + ray[Y] * t1
                  min_angle = math.atan2(min_point[Y] - source[Y], min_point[X] - source[X])
                  valid = True

          min_point = (round(min_point[X], 1), round(min_point[Y], 1))
          if valid and min_point not in (point for point, _ in light):
            light.append((min_point, min_angle))

    light.sort(key=lambda x: x[1])
    return tuple(point for point, _ in light)

  def toggle_cell(self, position, goal=False):

    cell = self.cells[(position[Y] // self.block_size) * self.width + (position[X] // self.block_size)]
    if goal:
      if cell.exists and cell.goal:
        cell.exists = False
        cell.goal = False
      elif cell.exists:
        cell.goal = True
      else:
        cell.exists = True
        cell.goal = True
    else:
      cell.exists = not cell.exists
      cell.goal = False
      
    self.set_edges()

  def draw(self, screen):

    for cell in self.cells:
      if cell.exists:
        cell.draw(screen)
