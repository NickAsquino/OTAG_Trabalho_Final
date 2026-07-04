import pygame
from constants import *

# =============================================================================
# LAYOUT DA AMARELINHA (Posições das casas)
# =============================================================================
def calcular_posicoes_amarelinha():
    """
    Calcula as posições (Rect) de cada casa da amarelinha no formato clássico.
    Retorna um dicionário {numero_casa: pygame.Rect}.

    Layout (de baixo para cima):
        Fileira 1 (base):  casas 1 e 2 (lado a lado)
        Fileira 2:         casa 3 (centralizada)
        Fileira 3:         casas 4 e 5 (lado a lado)
        Fileira 4:         casa 6 (centralizada)
        Fileira 5:         casas 7 e 8 (lado a lado)
        Fileira 6 (topo):  casa 9 (centralizada - "Céu")

    NOTA PARA INTEGRAÇÃO FUTURA COM CÂMERA:
        Estas coordenadas de tela poderão ser mapeadas para regiões do mundo real
        detectadas pela visão computacional. Basta substituir a verificação de
        "clique do mouse dentro do Rect" por "posição do jogador na região".
    """
    posicoes = {}
    cx = GRID_OFFSET_X  # Centro horizontal

    # Calculamos de cima para baixo (topo → base)
    # Fileira 6 (topo) - Casa 9 ("Céu")
    y = GRID_OFFSET_Y
    posicoes[9] = pygame.Rect(
        cx - CASA_LARGURA // 2, y,
        CASA_LARGURA, CASA_ALTURA
    )

    # Fileira 5 - Casas 7 e 8 (lado a lado)
    y += CASA_ALTURA + CASA_ESPACO
    posicoes[7] = pygame.Rect(
        cx - CASA_LARGURA - CASA_ESPACO // 2, y,
        CASA_LARGURA, CASA_ALTURA
    )
    posicoes[8] = pygame.Rect(
        cx + CASA_ESPACO // 2, y,
        CASA_LARGURA, CASA_ALTURA
    )

    # Fileira 4 - Casa 6 (centralizada)
    y += CASA_ALTURA + CASA_ESPACO
    posicoes[6] = pygame.Rect(
        cx - CASA_LARGURA // 2, y,
        CASA_LARGURA, CASA_ALTURA
    )

    # Fileira 3 - Casas 4 e 5 (lado a lado)
    y += CASA_ALTURA + CASA_ESPACO
    posicoes[4] = pygame.Rect(
        cx - CASA_LARGURA - CASA_ESPACO // 2, y,
        CASA_LARGURA, CASA_ALTURA
    )
    posicoes[5] = pygame.Rect(
        cx + CASA_ESPACO // 2, y,
        CASA_LARGURA, CASA_ALTURA
    )

    # Fileira 2 - Casa 3 (centralizada)
    y += CASA_ALTURA + CASA_ESPACO
    posicoes[3] = pygame.Rect(
        cx - CASA_LARGURA // 2, y,
        CASA_LARGURA, CASA_ALTURA
    )

    # Fileira 1 (base) - Casas 1 e 2 (lado a lado)
    y += CASA_ALTURA + CASA_ESPACO
    posicoes[1] = pygame.Rect(
        cx - CASA_LARGURA - CASA_ESPACO // 2, y,
        CASA_LARGURA, CASA_ALTURA
    )
    posicoes[2] = pygame.Rect(
        cx + CASA_ESPACO // 2, y,
        CASA_LARGURA, CASA_ALTURA
    )

    return posicoes


