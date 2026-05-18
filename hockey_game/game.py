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

selected_player = 0

def draw_menu():
  if background:
    screen.blit(background, (0,0))
  else:
    screen.fill(black)

  overlay = pygame.Surface((width, height))

  overlay.set_alpha(170)

  overlay.fill(black)

  screen.blit(overlay, (0,0))

  title = big_font.render(
    "Escolha o jogador",
    True,
    white
  )

  screen.blit(title,(width // 2- 300, 70))

  for i, player in enumerate(players):
    color = yellow if i == selected_player else white
    text = font.render(player, True, color)
    screen.blit(
      text,
      (width // 2 - 100,
       200 + i * 55)
    )

  info = font.render(
    "Enter = Escolher",
    True,
    red
  )

  screen.blit(info,(width // 2 - 170, 540))

  choosing = True

  while choosing:
    draw_menu()
    pygame.display.update()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          selected_player -= 1
        if event.key == pygame.K_DOWN:
          selected_player += 1
        if event.key == pygame.K_RETURN:
          choosing = False
      if selected_player < 0:
        selected_player = len(player) - 1
      if selected_player >= len(player):
        selected_player = 0

      player_name = player[selected_player]

      power_joao = player_name == "João"
      power_mike = player_name == "Mike"
      power_joselucas = player_name == "José Lucas"

      if power_joao:
        try:
          pygame.mixer.music.play(-1)
        except:
          pass

      left_dicso = player_blue(30)
      right_disco = player_red(width - 50)

      disco = Disco()

      raspando = power_joao
      rasp_time = 0

      running = True

      while running:
        clock.tick(60)

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
          left_dicso.y -= left_dicso.speed
        if keys[pygame.K_DOWN]:
          left_dicso.y += left_dicso.speed

        left_dicso.y = max(
          0,
          min(
            height - left_dicso.height,
            left_dicso.y
          )
        )

        ai_center = right_disco.y + right_disco.height / 2
        if ai_center < disco.y:
          right_disco.y += 6
        else:
          right_disco.y -= 6
        
        right_disco.y = max(
          0,
          min(
            height - right_disco.height,
            right_disco.y
          )
        )

        if raspando:
          disco.x = 140
          disco.y = (
            height // 2
            math.sin(rasp_time) * 170
          )

        rasp_time += 0.06
        if rasp_time >= math.pi * 4:
          raspando = False
          disco.speed_x = 8
          disco.speed_y = random.uniform(-3,3)
        else:
          disco.move()
        
        if (
          disco.x - disco.radius <= left_dicso.x + left_dicso.width
          and
          left_dicso.y <= disco.y <= left_dicso.y + left_dicso.height
          and
          disco.speed_x < 0
        ):
          disco.x = (
            left_dicso.x
            +
            left_dicso.width
            +
            disco.radius
          )

          hit_pos = (
            disco.y - left_dicso.y
          ) / left_dicso.height

          offset = (hit_pos - 0.5) * 2

          disco.speed_x *= -1

        if(
          disco.x + disco.radius >= right_disco.x
          and
          right_disco.y <= disco.y < right_disco.y + right_disco.height
          and
          disco.speed_x > 0
        ):
          disco.x = right_disco.x - disco.radius

          hit_pos = (
            disco.y - right_disco.y
          ) / right_disco.height

          offset = (hit_pos * 0.5) * 2

          disco.speed_x *= -1

          disco.speed_y = offset * 7

          disco.speed_x *= 1.03

        if disco.x < -50 or disco.x > width + 50:
          disco.reset()
          if power_joao:
            raspando = True
            rasp_time = 0

            disco.x = 140
            disco.y = height // 2