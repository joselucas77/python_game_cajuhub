import pygame
import random
import math
import sys

pygame.init()
pygame.mixer.init()

# Tamanho ajustado para o formato padrão do campo horizontal
width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hockey Game")

clock = pygame.time.Clock()

# Cores em RGB
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 140, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
gray = (100, 100, 100)

# Fontes
font = pygame.font.SysFont("trebuchetms", 32, bold=True)
big_font = pygame.font.SysFont("impact", 64, bold=False)

# Carregamento de Imagens
try:
    background = pygame.image.load("mesa.png")
    background = pygame.transform.scale(background, (width, height))
except:
    background = None

try:
    disco_img = pygame.image.load("disco.png")
    disco_img = pygame.transform.scale(disco_img, (68, 68))
except:
    disco_img = None

try:
    player_blue = pygame.image.load("player_blue.png")
    player_blue = pygame.transform.scale(player_blue, (80, 80))
except:
    player_blue = None

try:
    player_red = pygame.image.load("player_red.png")
    player_red = pygame.transform.scale(player_red, (80, 80))
except:
    player_red = None

# --- CORREÇÃO DA MÚSICA ---
try:
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1) # Faltava esta linha para a música tocar em loop infinito!
except: 
    pass


class Player:
    def __init__(self, x, is_jose_lucas=False):
        self.x = x
        self.width = 80
        self.height = 80
        self.y = height // 2 - (self.height // 2)
        self.speed = 12 if is_jose_lucas else 8
        self.vidas = 3  
        self.pontos = 0 

    def draw(self):
        if self.x < width // 2:
            if player_blue:
                img = pygame.transform.scale(player_blue, (self.width, self.height))
                screen.blit(img, (self.x, self.y))
            else:
                pygame.draw.rect(screen, blue, (self.x, self.y, self.width, self.height))
        else:
            if player_red:
                img = pygame.transform.scale(player_red, (self.width, self.height))
                screen.blit(img, (self.x, self.y))
            else:
                pygame.draw.rect(screen, red, (self.x, self.y, self.width, self.height))


class Disco:
    def __init__(self, is_mike=False):
        self.is_mike = is_mike
        self.radius = 34
        self.reset()

    def reset(self):
        self.x = width // 2
        self.y = height // 2
        self.speed = 13 if self.is_mike else 8
        direction = random.choice([-1, 1])
        self.speed_x = self.speed * direction
        self.speed_y = random.uniform(-3, 3)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Colisão precisa com o teto e chão
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.speed_y *= -1
        if self.y + self.radius >= height:
            self.y = height - self.radius
            self.speed_y *= -1

    def draw(self):
        if disco_img:
            screen.blit(disco_img, (int(self.x - self.radius), int(self.y - self.radius)))
        else:
            pygame.draw.circle(screen, white, (int(self.x), int(self.y)), self.radius)


# Lista de personagens disponíveis
lista_jogadores = ["José Lucas", "Mike", "João"]
selected_player = 0

def draw_menu():
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(black)

    overlay = pygame.Surface((width, height))
    overlay.set_alpha(170)
    overlay.fill(black)
    screen.blit(overlay, (0, 0))

    title = big_font.render("Escolha o jogador", True, white)
    screen.blit(title, (width // 2 - 200, 70))

    for i, p_name in enumerate(lista_jogadores):
        color = yellow if i == selected_player else white
        text = font.render(p_name, True, color)
        screen.blit(text, (width // 2 - 100, 250 + i * 55))

    info = font.render("Enter = Escolher", True, orange)
    screen.blit(info, (width // 2 - 110, 500))


# Definindo a área vertical do gol azul (centralizado no meio da altura)
gol_altura = 160
gol_y_inicio = (height // 2) - (gol_altura // 2)
gol_y_fim = (height // 2) + (gol_altura // 2)

# --- LOOP GLOBAL DA APLICAÇÃO ---
main_loop = True

while main_loop:
    
    # --- LOOP DO MENU DE SELEÇÃO ---
    choosing = True
    while choosing:
        draw_menu()
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_player -= 1
                if event.key == pygame.K_DOWN:
                    selected_player += 1
                if event.key == pygame.K_RETURN:
                    choosing = False
                    
        if selected_player < 0:
            selected_player = len(lista_jogadores) - 1
        if selected_player >= len(lista_jogadores):
            selected_player = 0

    # --- CONFIGURAÇÃO DA PARTIDA PÓS-MENU ---
    player_name = lista_jogadores[selected_player]
    power_joao = player_name == "João"
    power_mike = player_name == "Mike"
    power_joselucas = player_name == "José Lucas"

    # Jogadores e Disco inicializados com os poderes corretos
    left_disco = Player(75, is_jose_lucas=power_joselucas)
    right_disco = Player(width - 155, is_jose_lucas=False) 
    disco = Disco(is_mike=power_mike)

    raspando = False
    rasp_time = 0
    
    # --- CORREÇÃO: Variável de saque para pausar o jogo antes de lançar ---
    esperando_saque = True

    # --- LOOP PRINCIPAL DA PARTIDA EM ANDAMENTO ---
    running = True
    game_over = False

    while running:
        clock.tick(60)

        # Controles do Jogador da Esquerda (Permitido mover mesmo aguardando o saque)
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                left_disco.y -= left_disco.speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                left_disco.y += left_disco.speed

            left_disco.y = max(0, min(height - left_disco.height, left_disco.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Retorno ao menu
                if game_over and (event.key == pygame.K_r or event.key == pygame.K_RETURN):
                    running = False 
                
                # Botão de Lançar/Saque
                if esperando_saque and event.key == pygame.K_SPACE and not game_over:
                    esperando_saque = False
                    if power_joao:
                        raspando = True
                        rasp_time = 0

        if not game_over:
            
            if esperando_saque:
                # Mantém o disco congelado no meio enquanto aguarda o jogador apertar ESPAÇO
                disco.x = width // 2
                disco.y = height // 2
                
                # IA tenta se centralizar enquanto espera
                ai_center = right_disco.y + right_disco.height / 2
                if ai_center < height // 2 - 10:
                    right_disco.y += 3
                elif ai_center > height // 2 + 10:
                    right_disco.y -= 3
            else:
                # IA ativa seguindo o disco
                ai_center = right_disco.y + right_disco.height / 2
                if ai_center < disco.y:
                    right_disco.y += 6
                else:
                    right_disco.y -= 6
                right_disco.y = max(0, min(height - right_disco.height, right_disco.y))

                # Habilidade do João (Raspando)
                if raspando:
                    disco.x = left_disco.x + left_disco.width + disco.radius
                    disco.y = (height // 2) + int(math.sin(rasp_time) * 170)
                    rasp_time += 0.06
                    if rasp_time >= math.pi * 4:
                        raspando = False
                        disco.speed_x = disco.speed
                        disco.speed_y = random.uniform(-3, 3)
                else:
                    disco.move()
                
                # --- COLISÕES COM OS JOGADORES ---
                # Batida no Player da Esquerda
                if (disco.speed_x < 0 and 
                    disco.x - disco.radius <= left_disco.x + left_disco.width and 
                    disco.x + disco.radius >= left_disco.x and
                    left_disco.y <= disco.y <= left_disco.y + left_disco.height):
                    
                    disco.x = left_disco.x + left_disco.width + disco.radius
                    hit_pos = (disco.y - left_disco.y) / left_disco.height
                    offset = (hit_pos - 0.5) * 2
                    disco.speed_x *= -1
                    disco.speed_y = offset * 7

                # Batida no Player da Direita
                if (disco.speed_x > 0 and 
                    disco.x + disco.radius >= right_disco.x and 
                    disco.x - disco.radius <= right_disco.x + right_disco.width and
                    right_disco.y <= disco.y <= right_disco.y + right_disco.height):
                    
                    disco.x = right_disco.x - disco.radius
                    hit_pos = (disco.y - right_disco.y) / right_disco.height
                    offset = (hit_pos - 0.5) * 2
                    disco.speed_x *= -1
                    disco.speed_y = offset * 7
                    disco.speed_x *= 1.03

                # --- PAREDES LATERAIS DA ARENA VS SISTEMA DE GOL ---
                
                # Limite Esquerdo do Campo
                if disco.x - disco.radius <= 20:
                    if gol_y_inicio <= disco.y <= gol_y_fim:
                        right_disco.pontos += 1
                        left_disco.vidas -= 1
                        disco.reset()
                        esperando_saque = True # Pede o saque novamente
                    else:
                        disco.x = 20 + disco.radius
                        disco.speed_x *= -1

                # Limite Direito do Campo
                if disco.x + disco.radius >= width - 20:
                    if gol_y_inicio <= disco.y <= gol_y_fim:
                        left_disco.pontos += 1
                        right_disco.vidas -= 1
                        disco.reset()
                        esperando_saque = True # Pede o saque novamente
                    else:
                        disco.x = width - 20 - disco.radius
                        disco.speed_x *= -1

                # Monitoramento de Fim de Vidas
                if left_disco.vidas <= 0 or right_disco.vidas <= 0:
                    game_over = True
                    esperando_saque = False

        # --- DESENHO DOS ELEMENTOS NA TELA ---
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(black)
            pygame.draw.line(screen, white, (width // 2, 0), (width // 2, height), 2)
            
            # Paredes delimitadoras cinzas
            pygame.draw.rect(screen, gray, (0, 0, 20, gol_y_inicio))
            pygame.draw.rect(screen, gray, (0, gol_y_fim, 20, height - gol_y_fim))
            pygame.draw.rect(screen, gray, (width - 20, 0, 20, gol_y_inicio))
            pygame.draw.rect(screen, gray, (width - 20, gol_y_fim, 20, height - gol_y_fim))
            
            # Gols Azuis
            pygame.draw.rect(screen, blue, (0, gol_y_inicio, 20, gol_altura))
            pygame.draw.rect(screen, blue, (width - 20, gol_y_inicio, 20, gol_altura))

        left_disco.draw()
        right_disco.draw()
        disco.draw()

        texto_p1 = font.render(f"P1 Vidas: {left_disco.vidas} | Gols: {left_disco.pontos}", True, yellow)
        texto_p2 = font.render(f"Gols: {right_disco.pontos} | IA Vidas: {right_disco.vidas}", True, yellow)
        screen.blit(texto_p1, (40, 20))
        screen.blit(texto_p2, (width - 340, 20))

        if esperando_saque and not game_over:
            texto_saque = font.render("Aperte ESPAÇO para Lançar!", True, orange)
            screen.blit(texto_saque, (width // 2 - 190, height // 2 + 50))

        if game_over:
            overlay = pygame.Surface((width, height))
            overlay.set_alpha(200)
            overlay.fill(black)
            screen.blit(overlay, (0, 0))
            
            vencedor = "VOCÊ VENCEU!" if right_disco.vidas == 0 else "A IA VENCEU!"
            texto_fim = big_font.render(vencedor, True, red)
            texto_reiniciar = font.render("Pressione ENTER para voltar ao Menu", True, white)
            
            screen.blit(texto_fim, (width // 2 - 180, height // 2 - 50))
            screen.blit(texto_reiniciar, (width // 2 - 250, height // 2 + 50))

        pygame.display.update()

pygame.quit()