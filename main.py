import pygame
import random
from collections import deque

# Inicializa o Pygame
pygame.init()

# Define as dimensões da tela e cores
largura, altura = 500, 500
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Cobrinha")
branco = (255, 255, 255)
preto = (0, 0, 0)
verde = (0, 255, 0)
vermelho = (255, 0, 0)

# Tamanho do bloco da cobra e da comida
tamanho_bloco = 10

# Direções
ESQUERDA = "esquerda"
DIREITA = "direita"
CIMA = "cima"
BAIXO = "baixo"

# Função para desenhar a cobra na tela
def desenhar_cobra(cobra_corpo):
    for x in cobra_corpo:
        pygame.draw.rect(tela, verde, [x[0], x[1], tamanho_bloco, tamanho_bloco])

# Função para desenhar a comida na tela
def desenhar_comida(comida_pos):
    pygame.draw.rect(tela, vermelho, [comida_pos[0], comida_pos[1], tamanho_bloco, tamanho_bloco])

# Função para a mensagem de game over
def mensagem(msg, cor, pontuacao=0):
    fonte = pygame.font.SysFont(None, 30)
    texto = fonte.render(msg, True, cor)
    tela.blit(texto, [largura/3, altura/3])
    if pontuacao > 0:
        texto_ponto = fonte.render(f"Pontuação: {pontuacao}", True, cor)
        tela.blit(texto_ponto, [largura/3, altura/3 + 40])

# Função para desenhar a pontuação
def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont(None, 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", True, branco)
    tela.blit(texto, [0, 0])

# Inicializa a posição da comida FORA do corpo da cobra
def gerar_comida(cobra):
    while True:
        comida_x = round(random.randrange(0, largura - tamanho_bloco) / 10.0) * 10.0
        comida_y = round(random.randrange(0, altura - tamanho_bloco) / 10.0) * 10.0
        comida_pos = [comida_x, comida_y]
        if comida_pos not in cobra:
            return comida_pos

# Função para reiniciar o jogo
def reiniciar_jogo():
    global cobra, direcao, comida_pos, cobra_x, cobra_y, pontuacao, velocidade_jogo
    cobra_x = largura / 2
    cobra_y = altura / 2
    cobra = deque([[cobra_x, cobra_y]])
    direcao = DIREITA
    comida_pos = gerar_comida(cobra)
    pontuacao = 0
    velocidade_jogo = 15

# Inicializa a cobra e a comida
cobra_x = largura / 2
cobra_y = altura / 2
cobra = deque([[cobra_x, cobra_y]])
direcao = DIREITA
comida_pos = gerar_comida(cobra)
pontuacao = 0

# Loop principal do jogo
clock = pygame.time.Clock()
velocidade_jogo = 15

rodando = True
while rodando:

    clock.tick(velocidade_jogo)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT and direcao != DIREITA:
                direcao = ESQUERDA
            elif evento.key == pygame.K_RIGHT and direcao != ESQUERDA:
                direcao = DIREITA
            elif evento.key == pygame.K_UP and direcao != BAIXO:
                direcao = CIMA
            elif evento.key == pygame.K_DOWN and direcao != CIMA:
                direcao = BAIXO

    # Lógica do movimento da cobra
    if direcao == ESQUERDA:
        cobra_x -= tamanho_bloco
    if direcao == DIREITA:
        cobra_x += tamanho_bloco
    if direcao == CIMA:
        cobra_y -= tamanho_bloco
    if direcao == BAIXO:
        cobra_y += tamanho_bloco

    cobra_cabeça = [cobra_x, cobra_y]
    cobra.append(cobra_cabeça)

    # Verifica se a cobra comeu a comida
    if cobra_cabeça == comida_pos:
        comida_pos = gerar_comida(cobra)
        pontuacao += 10
        velocidade_jogo += 1
    else:
        cobra.popleft()

    # Verifica se a cobra colidiu com as bordas ou consigo mesma
    if (cobra_x >= largura or cobra_x < 0 or
        cobra_y >= altura or cobra_y < 0 or
        cobra_cabeça in list(cobra)[:-1]):
        rodando = False

    # Desenha na tela
    tela.fill(preto)
    desenhar_cobra(cobra)
    desenhar_comida(comida_pos)
    desenhar_pontuacao(pontuacao)
    pygame.display.update()

# Loop de encerramento para reiniciar ou sair
while True:
    tela.fill(preto)
    mensagem("Game Over! Pressione C para Jogar Novamente ou Q para Sair", vermelho, pontuacao)
    pygame.display.update()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_q:
                pygame.quit()
                quit()
            if evento.key == pygame.K_c:
                reiniciar_jogo()
                rodando = True
                break
    if rodando:
        break

    clock.tick(15)

pygame.quit()
quit()
