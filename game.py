import pygame
import random

class Entity:
  def __init__(self, x, y, size, image):
    self.x = x
    self.y = y
    self.size = size
    self.image = image

  def draw(self, screen):
    screen.blit(self.image, (self.x, self.y))

class Player(Entity):
  def __init__(self, x, y, size, image):
    super().__init__(x, y, 50, image)
    self.speed = 6
    self.lives = 3

  def move(self, keys, width, height):
    if keys[pygame.K_LEFT]:
      self.x -= self.speed
    if keys[pygame.K_RIGHT]:
      self.x += self.speed
    if keys[pygame.K_UP]:
      self.y -= self.speed
    if keys[pygame.K_DOWN]:
      self.y += self.speed

    self.x = max(0, min(width - self.size, self.x))
    self.y = max(0, min(height - self.size, self.y))

class Enemy(Entity):
  def __init__(self, image):
    x = random.randint(0, 750)
    y = random.randint(-100, -40)
    super().__init__(x, y, 40, image)
    self.speed = random.randint(2, 5)
  def update(self):
    self.y += self.speed
