import pygame
import numpy as np
import random

# Inicializando o pygame
pygame.init()

# Configurações do jogo
largura_janela = 400
altura_janela = 500  # Ajustado para incluir espaço para pontuação
tamanho_bloco = largura_janela // 4
fonte = pygame.font.Font(None, 50)
fonte_pontuacao = pygame.font.Font(None, 30)
fonte_game_over = pygame.font.Font(None, 70)
fps = 30

# Cores
cores = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

preto = (119, 110, 101)
branco = (255, 255, 255)
cinza_fundo = (187, 173, 160)

# Inicializando a tela
tela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("2048")

# Funções principais do jogo
def iniciar_jogo():
    tabuleiro = np.zeros((4, 4), dtype=int)
    adicionar_novo_numero(tabuleiro)
    adicionar_novo_numero(tabuleiro)
    return tabuleiro

def adicionar_novo_numero(tabuleiro):
    if 0 in tabuleiro:
        linha, coluna = random.choice([(i, j) for i in range(4) for j in range(4) if tabuleiro[i, j] == 0])
        tabuleiro[linha, coluna] = random.choices([2, 4], weights=[90, 10], k=1)[0]

def mover_esquerda(tabuleiro, pontuacao):
    novo_tabuleiro = np.zeros_like(tabuleiro)
    mudou = False  # Verifica se houve mudança no tabuleiro

    for i in range(4):
        linha = tabuleiro[i, :]
        linha = linha[linha != 0]
        nova_linha = []
        pular = False

        for j in range(len(linha)):
            if pular:
                pular = False
                continue
            if j < len(linha) - 1 and linha[j] == linha[j + 1]:
                nova_linha.append(linha[j] * 2)
                pontuacao += linha[j] * 2
                pular = True
                mudou = True  # Houve fusão, então houve mudança
            else:
                nova_linha.append(linha[j])

        novo_tabuleiro[i, :len(nova_linha)] = nova_linha

        # Se a linha antes e depois forem diferentes, houve mudança
        if not np.array_equal(tabuleiro[i, :], novo_tabuleiro[i, :]):
            mudou = True

    return novo_tabuleiro, pontuacao, mudou

def rotacionar_90_graus(tabuleiro):
    return np.rot90(tabuleiro)

def movimentar(tabuleiro, direcao, pontuacao):
    mudou = False

    if direcao == 'esquerda':
        tabuleiro, pontuacao, mudou = mover_esquerda(tabuleiro, pontuacao)
    elif direcao == 'direita':
        tabuleiro = rotacionar_90_graus(rotacionar_90_graus(tabuleiro))
        tabuleiro, pontuacao, mudou = mover_esquerda(tabuleiro, pontuacao)
        tabuleiro = rotacionar_90_graus(rotacionar_90_graus(tabuleiro))
    elif direcao == 'cima':
        tabuleiro = rotacionar_90_graus(tabuleiro)
        tabuleiro, pontuacao, mudou = mover_esquerda(tabuleiro, pontuacao)
        tabuleiro = rotacionar_90_graus(rotacionar_90_graus(rotacionar_90_graus(tabuleiro)))
    elif direcao == 'baixo':
        tabuleiro = rotacionar_90_graus(rotacionar_90_graus(rotacionar_90_graus(tabuleiro)))
        tabuleiro, pontuacao, mudou = mover_esquerda(tabuleiro, pontuacao)
        tabuleiro = rotacionar_90_graus(tabuleiro)

    return tabuleiro, pontuacao, mudou

def verificar_derrota(tabuleiro):
    if 0 in tabuleiro:
        return False
    for direcao in ['esquerda', 'direita', 'cima', 'baixo']:
        if not np.array_equal(tabuleiro, movimentar(tabuleiro, direcao, 0)[0]):
            return False
    return True

def desenhar_tabuleiro(tabuleiro, pontuacao):
    tela.fill(cinza_fundo)
    for i in range(4):
        for j in range(4):
            valor = tabuleiro[i, j]
            cor = cores.get(valor, branco)
            pygame.draw.rect(tela, cor, (j * tamanho_bloco, i * tamanho_bloco + 100, tamanho_bloco, tamanho_bloco))
            if valor != 0:
                texto = fonte.render(str(valor), True, preto if valor < 128 else branco)
                texto_rect = texto.get_rect(center=(j * tamanho_bloco + tamanho_bloco // 2, i * tamanho_bloco + 100 + tamanho_bloco // 2))
                tela.blit(texto, texto_rect)
    
    # Desenhar a pontuação
    texto_pontuacao = fonte_pontuacao.render(f"Pontuação: {pontuacao}", True, preto)
    tela.blit(texto_pontuacao, (10, 10))

def mostrar_menu():
    tela.fill(cinza_fundo)
    mensagem = fonte_game_over.render("Fim de Jogo!", True, preto)
    reiniciar = fonte.render("Pressione R para Reiniciar", True, preto)
    tela.blit(mensagem, (largura_janela // 2 - mensagem.get_width() // 2, altura_janela // 3))
    tela.blit(reiniciar, (largura_janela // 2 - reiniciar.get_width() // 2, altura_janela // 2))
    pygame.display.update()

# Loop principal do jogo
def jogo_2048():
    tabuleiro = iniciar_jogo()
    pontuacao = 0
    clock = pygame.time.Clock()
    rodando = True

    while rodando:
        movimento_realizado = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    tabuleiro, pontuacao, movimento_realizado = movimentar(tabuleiro, 'esquerda', pontuacao)
                elif evento.key == pygame.K_RIGHT:
                    tabuleiro, pontuacao, movimento_realizado = movimentar(tabuleiro, 'direita', pontuacao)
                elif evento.key == pygame.K_UP:
                    tabuleiro, pontuacao, movimento_realizado = movimentar(tabuleiro, 'cima', pontuacao)
                elif evento.key == pygame.K_DOWN:
                    tabuleiro, pontuacao, movimento_realizado = movimentar(tabuleiro, 'baixo', pontuacao)
                
                # Só adiciona um novo número se houve um movimento válido
                if movimento_realizado:
                    adicionar_novo_numero(tabuleiro)

        if verificar_derrota(tabuleiro):
            mostrar_menu()
            esperando = True
            while esperando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        esperando = False
                        rodando = False
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                        tabuleiro = iniciar_jogo()
                        pontuacao = 0
                        esperando = False

        desenhar_tabuleiro(tabuleiro, pontuacao)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

jogo_2048()
