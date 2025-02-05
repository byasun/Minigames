import pygame
import numpy as np

pygame.init()

# Cores do tabuleiro
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza_fundo = (187, 173, 160)
vermelho = (255, 0, 0)  # Cor de fundo das letras
preto_texto = (0, 0, 0)
branco_texto = (255, 255, 255)

# Fonte para desenhar as letras das peças
fonte = pygame.font.Font(None, 40)

# Configuração da janela (com espaço para as peças capturadas)
largura_janela = 480  # Aumentado para espaço extra
altura_janela = 480  # Aumentado para espaço extra
tela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Xadrez")

# Definir o tamanho das casas do tabuleiro
tamanho_casa = 400 // 8

# Lista para armazenar peças capturadas
pecas_capturadas = {"branco": [], "preto": []}

def desenhar_tabuleiro():
    tela.fill(cinza_fundo)
    for linha in range(8):
        for coluna in range(8):
            cor = branco if (linha + coluna) % 2 == 0 else preto
            pygame.draw.rect(tela, cor, (coluna * tamanho_casa, linha * tamanho_casa, tamanho_casa, tamanho_casa))

def desenhar_pecas():
    for peca in pecas:
        peca.desenhar()

def desenhar_pecas_capturadas():
    # Desenha as peças capturadas fora do tabuleiro
    for i, peca in enumerate(pecas_capturadas["branco"]):
        peca.desenhar_no_lugar_capturado(i, "branco")
    for i, peca in enumerate(pecas_capturadas["preto"]):
        peca.desenhar_no_lugar_capturado(i, "preto")

class Peca:
    def __init__(self, nome, posicao, cor):
        self.nome = nome
        self.posicao = posicao  # (linha, coluna)
        self.cor = cor  # "branco" ou "preto"

    def mover(self, nova_posicao):
        self.posicao = nova_posicao
        print(f"{self.nome} ({self.cor}) movido para {nova_posicao}")

    def desenhar(self):
        x, y = self.posicao[1] * tamanho_casa, self.posicao[0] * tamanho_casa
        letra = self.nome[0].upper()

        # Ajustando a cor do texto da peça conforme a cor da peça
        texto_cor = branco_texto if self.cor == "preto" else preto_texto
        texto = fonte.render(letra, True, texto_cor)

        # Tamanho da caixa vermelha
        largura_caixa = tamanho_casa // 2
        altura_caixa = tamanho_casa // 2

        # Desenha o fundo vermelho (ajustando o tamanho e a posição)
        pygame.draw.rect(tela, vermelho, (x + (tamanho_casa - largura_caixa) // 2, y + (tamanho_casa - altura_caixa) // 2, largura_caixa, altura_caixa))
        
        # Desenha o texto centralizado dentro da caixa vermelha
        texto_x = x + (tamanho_casa - largura_caixa) // 2 + (largura_caixa - texto.get_width()) // 2
        texto_y = y + (tamanho_casa - altura_caixa) // 2 + (altura_caixa - texto.get_height()) // 2
        tela.blit(texto, (texto_x, texto_y))

    def desenhar_no_lugar_capturado(self, indice, cor):
        espaco_capturado = 420  # A partir do eixo x = 420
        tamanho_peca = 40
        y_offset = 50 + indice * 50  # Para empilhar as peças capturadas
        if cor == "branco":
            x_offset = espaco_capturado
            texto = fonte.render(self.nome[0].upper(), True, branco_texto)
        else:
            x_offset = espaco_capturado + 40
            texto = fonte.render(self.nome[0].upper(), True, preto_texto)

        pygame.draw.rect(tela, vermelho, (x_offset, y_offset, tamanho_peca, tamanho_peca))
        tela.blit(texto, (x_offset + 8, y_offset + 8))

class Peao(Peca):
    def movimento_valido(self, destino):
        direcao = -1 if self.cor == "branco" else 1
        linha_atual, coluna_atual = self.posicao
        linha_destino, coluna_destino = destino

        if coluna_atual == coluna_destino and linha_destino == linha_atual + direcao:
            return True
        if coluna_atual == coluna_destino and linha_atual in (1, 6) and linha_destino == linha_atual + 2 * direcao:
            return True
        if abs(coluna_destino - coluna_atual) == 1 and linha_destino == linha_atual + direcao:
            return True
        return False

class Torre(Peca):
    def movimento_valido(self, destino):
        return self.posicao[0] == destino[0] or self.posicao[1] == destino[1]

class Cavalo(Peca):
    def movimento_valido(self, destino):
        dx = abs(destino[0] - self.posicao[0])
        dy = abs(destino[1] - self.posicao[1])
        return (dx, dy) in [(2, 1), (1, 2)]

class Bispo(Peca):
    def movimento_valido(self, destino):
        return abs(destino[0] - self.posicao[0]) == abs(destino[1] - self.posicao[1])

class Rainha(Peca):
    def movimento_valido(self, destino):
        return Torre.movimento_valido(self, destino) or Bispo.movimento_valido(self, destino)

class Rei(Peca):
    def movimento_valido(self, destino):
        return abs(destino[0] - self.posicao[0]) <= 1 and abs(destino[1] - self.posicao[1]) <= 1

# Criando as peças no tabuleiro
pecas = [
    Peao("Peao", (6, i), "branco") for i in range(8)
] + [
    Peao("Peao", (1, i), "preto") for i in range(8)
] + [
    Torre("Torre", (0, 0), "preto"), 
    Torre("Torre", (0, 7), "preto"),
    Torre("Torre", (7, 0), "branco"), 
    Torre("Torre", (7, 7), "branco"),
    Cavalo("Cavalo", (0, 1), "preto"), 
    Cavalo("Cavalo", (0, 6), "preto"),
    Cavalo("Cavalo", (7, 1), "branco"), 
    Cavalo("Cavalo", (7, 6), "branco"),
    Bispo("Bispo", (0, 2), "preto"), 
    Bispo("Bispo", (0, 5), "preto"),
    Bispo("Bispo", (7, 2), "branco"), 
    Bispo("Bispo", (7, 5), "branco"),
    Rainha("Rainha", (0, 3), "preto"), 
    Rainha("Rainha", (7, 3), "branco"),
    Rei("Rei", (0, 4), "preto"), 
    Rei("Rei", (7, 4), "branco")
]

def desenhar_pecas():
    for peca in pecas:
        peca.desenhar()

def desenhar_pecas_capturadas():
    # Desenha as peças capturadas fora do tabuleiro
    for i, peca in enumerate(pecas_capturadas["branco"]):
        peca.desenhar_no_lugar_capturado(i, "branco")
    for i, peca in enumerate(pecas_capturadas["preto"]):
        peca.desenhar_no_lugar_capturado(i, "preto")

peca_selecionada = None
turno_atual = "branco"  # Começa com as peças brancas

def tratar_eventos():
    global peca_selecionada, turno_atual
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            coluna = x // tamanho_casa
            linha = y // tamanho_casa

            if peca_selecionada:
                # Verifica se é um movimento válido
                if peca_selecionada.movimento_valido((linha, coluna)) and peca_selecionada.cor == turno_atual:
                    peca_destino = None
                    for peca in pecas:
                        if peca.posicao == (linha, coluna):
                            peca_destino = peca
                            break

                    if peca_destino:
                        if peca_destino.cor != peca_selecionada.cor:
                            pecas.remove(peca_destino)  # Captura a peça adversária
                            pecas_capturadas[peca_destino.cor].append(peca_destino)
                            print(f"{peca_destino.nome} ({peca_destino.cor}) foi capturada!")
                        else:
                            print("Não pode capturar sua própria peça!")

                    peca_selecionada.mover((linha, coluna))
                    turno_atual = "preto" if turno_atual == "branco" else "branco"
                else:
                    print("Movimento inválido ou não é a sua vez!")
                
                peca_selecionada = None  # Deseleciona a peça após o movimento
            else:
                # Seleciona a peça se houver alguma na posição clicada
                for peca in pecas:
                    if peca.posicao == (linha, coluna) and peca.cor == turno_atual:
                        peca_selecionada = peca
                        print(f"Selecionado: {peca.nome} ({peca.cor})")
                        break
    return True

# Loop principal do jogo
rodando = True
while rodando:
    rodando = tratar_eventos()
    desenhar_tabuleiro()
    desenhar_pecas()
    desenhar_pecas_capturadas()  # Desenha as peças capturadas
    pygame.display.flip()

pygame.quit()
