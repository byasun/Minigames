import pygame
import time
import random

pygame.init()

# Definindo cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)

# Largura e altura da tela
largura = 600
altura = 400

# Criando a tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo Snake')

# Controle de tempo
relogio = pygame.time.Clock()

# Definindo o tamanho do bloco e a velocidade do jogo
tamanho_bloco = 10
velocidade_jogo = 15

# Fonte para o texto
font_style = pygame.font.SysFont("bahnschrift", 25)
font_pontos = pygame.font.SysFont("comicsansms", 35)

# Função para mostrar a pontuação
def mostrar_pontos(pontos):
    valor = font_pontos.render("Pontuação: " + str(pontos), True, preto)
    tela.blit(valor, [0, 0])

# Função para desenhar a cobra
def desenhar_cobra(tamanho_bloco, lista_corpo_cobra):
    for x in lista_corpo_cobra:
        pygame.draw.rect(tela, verde, [x[0], x[1], tamanho_bloco, tamanho_bloco])

# Função para mostrar mensagens na tela
def mensagem(msg, cor):
    mensagem_1 = font_style.render(msg, True, cor)
    tela.blit(mensagem_1, [largura / 6, altura / 3])

# Função principal do jogo
def jogo():
    game_over = False
    game_close = False

    # Posições iniciais da cobra
    x1 = largura / 2
    y1 = altura / 2

    # Direções iniciais
    x1_mover = 0
    y1_mover = 0

    # Corpo da cobra
    lista_corpo_cobra = []
    comprimento_cobra = 1

    # Posição da comida
    comida_x = round(random.randrange(0, largura - tamanho_bloco) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura - tamanho_bloco) / 10.0) * 10.0

    while not game_over:

        while game_close:
            tela.fill(azul)
            mensagem("Você perdeu! Pressione C para jogar novamente ou Q para sair", vermelho)
            mostrar_pontos(comprimento_cobra - 1)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if evento.key == pygame.K_c:
                        jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x1_mover = -tamanho_bloco
                    y1_mover = 0
                elif evento.key == pygame.K_RIGHT:
                    x1_mover = tamanho_bloco
                    y1_mover = 0
                elif evento.key == pygame.K_UP:
                    y1_mover = -tamanho_bloco
                    x1_mover = 0
                elif evento.key == pygame.K_DOWN:
                    y1_mover = tamanho_bloco
                    x1_mover = 0

        # Verificando se a cobra bateu nas bordas
        if x1 >= largura or x1 < 0 or y1 >= altura or y1 < 0:
            game_close = True
        x1 += x1_mover
        y1 += y1_mover
        tela.fill(azul)
        pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])
        lista_corpo_cobra.append([x1, y1])
        if len(lista_corpo_cobra) > comprimento_cobra:
            del lista_corpo_cobra[0]

        # Verificando se a cobra colidiu com ela mesma
        for x in lista_corpo_cobra[:-1]:
            if x == [x1, y1]:
                game_close = True

        desenhar_cobra(tamanho_bloco, lista_corpo_cobra)
        mostrar_pontos(comprimento_cobra - 1)

        pygame.display.update()

        # Verificando se a cobra comeu a comida
        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, largura - tamanho_bloco) / 10.0) * 10.0
            comida_y = round(random.randrange(0, altura - tamanho_bloco) / 10.0) * 10.0
            comprimento_cobra += 1

        relogio.tick(velocidade_jogo)

    pygame.quit()
    quit()

# Iniciando o jogo
jogo()
