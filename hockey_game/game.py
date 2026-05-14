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