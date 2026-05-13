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

class Bullet(Entity):
  def __init__(self, x, y, image):
    super().__init__(x, y, 10, image)
    self.speed = 10
  def update(self):
    self.y -= self.speed

class Explosion:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.radius = 5
    self.max_radius = 30
    self.alive = True
  def update(self):
    self.radius += 2
    if self.radius > self.max_radius:
      self.alive = False
  def draw(self, screen):
    pygame.draw.circle(screen, (255, 200, 0), (self.x, self.y), self.radius)

class Game:
  def __init__(self):
    pygame.init()
    pygame.mixer.init()

    self.width = 800
    self.height = 600

    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption("Space")

    self.clock = pygame.time.Clock()

    self.state = "MENU"

    self.bg = pygame.image.load("background.png").convert()
    self.bg = pygame.transform.scale(self.bg,(self.width, self.height))

    self.bg = pygame.image.load("player.png").convert_alpha()
    self.bg = pygame.transform.scale(self.player_img, (100, 100))

    self.bg = pygame.image.load("enemy.png").convert_alpha()
    self.bg = pygame.transform.scale(self.player_img, (100, 200))

    self.bg = pygame.image.load("bullet.png").convert_alpha()
    self.bg = pygame.transform.scale(self.player_img, (50, 40))

    self.player = Player(375, 500, self.player_img)

    self.enemies = []
    self.bullets = []
    self.explosions = []

    # para audios .wav
    self.shot_sound = pygame.Sound("shoot.wav")
    self.explosion_sound = pygame.mixer.Sound("explosion.wav")

    # Para audio .mp3
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.5)

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if self.state == "MENU":
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            self.state = "PLAYING"

            pygame.mixer.music.play(-1)

      elif self.state == "PLAYING":
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            Bullet(self.player.x + 20, self.player.y, self.bullet_img)

  def update(self):
    if self.state != "PLAYING":
      return
    
    keys = pygame.key.get_pressed()
    self.player.move(keys, self.width, self.height)

    self.spawn_timer += 1
    if self.spawn_timer > 50:
      self.enemies.append(Enemy(self.enemy_img))
      self.spawn_timer = 0

    for enemy in self.enemies:
      enemy.update()

    for bullet in self.bullets:
      bullet.update()

    for exp in self.explosions:
      exp.update()
    
    self.explosions = [e for e in self.explosions if e.alive]

    for bullet in self.bullets[:]:
      if enemy in self.enemies[:]:
        if self.collide(bullet, enemy):
          self.explosion.append(Explosion(enemy.x, enemy.y))
          self.explosion_sound.play()
          self.bullet.remove(bullet)
          self.enemies.remove(enemy)
          break

    for enemy in self.enemies[:]:
      if self.collide(enemy, self.player):
        self.enemies.remove(enemy)
        self.player.lives -= 1

    self.bullets = [b for b in self.bullets if b.y > 0]
    self.enemies = [e for e in self.enemies if e.y < self.height]

  def collide(self, a, b):
    return (
      a.x < b.x + b.size and
      a.x + a.size > b.x and
      a.y < b.y + b.size and
      a.y + a.size > b.y
    )
  
  def draw(self):
    if self.state == "MENU":
      self.screen.blit(self.bg, (0,0))
      font = pygame.font.SysFont(None, 50)
      text = font.render("Pressione Enter para defender a galaxia", True, {255, 255, 255})
      self.screen.blit(text, (80, 250))
      pygame.display.flip()
      return
    
    self.screen.blit(self.bg, (0,0))
    self.player.draw(self.screen)

    for enemy in self.enemies:
      enemy.draw(self.screen)

    for bullet in self.bullets:
      bullet.draw(self.screen)

    for exp in self.explosions:
      exp.draw(self.screen)

    font = pygame.font.SysFOnt(None, 30)
    lives = font.render(f"Vidas: {self.player.liver}", True, (255, 255, 255))
    self.screen.blit(lives, (10, 10))

    pygame.display.flip()

  def run(self):
    while self.running and self.player.lives > 0:
      self.hanfle_events()
      self.update()
      self.draw()
      self.clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
  game = Game()
  game.run()


