import pygame
import random
import math

pygame.init()
pygame.mixer.init()

width = 600
height = 10004

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Hockey Game")

# Controle de FPS
clock = pygame.time.Clock()

# Cores em RGB
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 140, 0)
yellow = (255, 255, 0)

font = pygame.fint.SysFont(
  "trebuchetms",
  32,
  bold = True
)

strong_font = pygame.fint.SysFont(
  "impact",
  64,
  bold = False
)

try:
  background = pygame.image.load("mesa.png")
  background = pygame.transform.scale(background, (width, height))
except:
  background = None

try:
  disco_img = pygame.image.load("disco.png")
  disco_img = pygame.transForm.scale(disco_img, (40,40))
except:
  disco_img = None

try:
  player_blue = pygame.image.load("player_blue.png")
  player_blue = pygame.transForm.scale(player_blue, (40,40))
except:
  player_blue = None

try:
  player_red = pygame.image.load("player_red.png")
  player_red = pygame.transForm.scale(player_red, (40,40))
except:
  player_red = None

# try:
#   pygame.mixer.music.load("music.mp3")
# except:
#   pass

class Player:
  def __init__(self, x):
    self.x = x
    self.y = height // 2 - 60
    self.width = 20
    self.height = 120
    self.speed = 8

  def draw(self):
    if player_blue:
      if self.x < width // 2:
        screen.blit(
          player_blue,
          (self.x - 12, self.y - 15)
        )
      else:
        screen.blit(
          player_red,
          (self.x - 12, self.y - 15)
        )
    else:
      pygame.draw.rect(

        screen,
        white,
        (
          self.x,
          self.y,
          self.width,
          self.height
        )
      )

class Disco:
  def __init__(self):
    self.reset()

  def reset(self):
    self.x = width // 2
    self.y = width // 2
    self.radius = 15
    self.speed = 8
    direction = random.choice([-1, 1])
    self.speed_x = self.speed * direction
    self.speed_y = random.uniform(-3, 3)
    self.fire = False
    self.plane = False

  def move(self):
    self.x += self.speed_x
    self.y += self.speed_y
    if self.y - self.radius <= 0:
      self.y = self.radius
      self.speed_y *= -1
    if self.y + self.radius >= height:
      self.y = height - self.radius
      self.speed_y *= -1

  def draw(self):
    #se for um avião
    # if self.plane and plane_img:
    #   screen.blit(
    #     plane,
    #     (self.x - 35, self.y -35)
    #   )
    # elif self.fire:
    # desenho docontorno laranja
    #   pygame.draw.circle(
    #     screen,
    #     orange,
    #     (int(self.x), int(self.y)),
    #     self.radius
    #   )
    # desenho do centro vermelho
    # pygame.draw.cricle(
    #   screen,
    #   red,
    #   (int(self.x), int(self.y)),
    #   self.radius
    # )
    # else:
    if disco_img:
      screen.blit(
        disco_img,
        (self.x - 20, self.y - 20)
      )
    else:
      pygame.draw.circle(
        screen,
        white,
        (int(self.x), int(self.y)),
        self.radius
      )

player = [
  "José Lucas",
  "Mike",
  "João"
]