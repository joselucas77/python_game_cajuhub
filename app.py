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
        super().__init__(x, y, size, image)
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

        self.width = 1000
        self.height = 800

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Space")

        self.clock = pygame.time.Clock()
        self.state = "MENU"
        self.running = True
        self.spawn_timer = 0

        # Carregamento de imagens
        self.bg = pygame.image.load("background_galaxy.png").convert()
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

        self.player_img = pygame.image.load("player.png").convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (80, 80))
        self.player_img = pygame.transform.rotate(self.player_img, 90)

        self.enemy_img = pygame.image.load("enemy.png").convert_alpha()
        self.enemy_img = pygame.transform.scale(self.enemy_img, (80, 80))
        self.enemy_img = pygame.transform.rotate(self.enemy_img, -90)

        self.bullet_img = pygame.image.load("bullet.png").convert_alpha()
        self.bullet_img = pygame.transform.scale(self.bullet_img, (10, 20))
        self.bullet_img = pygame.transform.rotate(self.bullet_img, 90)

        self.player = Player(480, 700, 50, self.player_img)

        self.enemies = []
        self.bullets = []
        self.explosions = []

        # Áudios
        self.shot_sound = pygame.mixer.Sound("shoot.wav")
        self.explosion_sound = pygame.mixer.Sound("explosion.wav")

        try:
            pygame.mixer.music.load("music.wav")
            pygame.mixer.music.set_volume(0.2)
        except:
            print("Música não encontrada.")

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
                        new_bullet = Bullet(self.player.x + self.player.size//2 - 5, self.player.y, self.bullet_img)
                        self.bullets.append(new_bullet)
                        self.shot_sound.play()

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

        # Sistema de colisão Bala vs Inimigo
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if self.collide(bullet, enemy):
                    self.explosions.append(Explosion(enemy.x + enemy.size//2, enemy.y + enemy.size//2))
                    self.explosion_sound.play()
                    if bullet in self.bullets: self.bullets.remove(bullet)
                    if enemy in self.enemies: self.enemies.remove(enemy)
                    break

        # Sistema de colisão Inimigo vs Player
        for enemy in self.enemies[:]:
            if self.collide(enemy, self.player):
                self.enemies.remove(enemy)
                self.player.lives -= 1

        self.bullets = [b for b in self.bullets if b.y > -50]
        self.enemies = [e for e in self.enemies if e.y < self.height]

    def collide(self, a, b):
        return (
            a.x < b.x + b.size and
            a.x + a.size > b.x and
            a.y < b.y + b.size and
            a.y + a.size > b.y
        )
    
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        
        if self.state == "MENU":
            font = pygame.font.SysFont(None, 50)
            text = font.render("Pressione Enter para Iniciar", True, (255, 255, 255))
            self.screen.blit(text, (self.width//2 - 200, self.height//2))
        
        elif self.state == "PLAYING":
            self.player.draw(self.screen)

            for enemy in self.enemies:
                enemy.draw(self.screen)

            for bullet in self.bullets:
                bullet.draw(self.screen)

            for exp in self.explosions:
                exp.draw(self.screen)

            font = pygame.font.SysFont(None, 30)
            lives_text = font.render(f"Vidas: {self.player.lives}", True, (255, 255, 255))
            self.screen.blit(lives_text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            if self.player.lives <= 0:
                print("Game Over!")
                self.running = False
                
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()