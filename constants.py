"""
===============================================================================
EXERGAME: AMAR-É-LINDO (MVP)
===============================================================================
Descrição:
    MVP do exergame baseado na brincadeira de amarelinha.
    O jogador deve memorizar uma sequência de casas iluminadas e reproduzi-la
    clicando com o mouse na ordem correta.

Objetivo do MVP:
    Validar a lógica de programação, mecânica de jogo e feedbacks visuais.
    A interação atual é via mouse; futuramente será integrada com visão
    computacional (câmera + detecção de pose/movimento).

Estrutura de Pastas:
    AmarELindo/
    ├── main.py              (este arquivo)
    └── assets/
        ├── images/          (coloque imagens aqui: logo, backgrounds, etc.)
        ├── sounds/          (coloque sons aqui: acerto.wav, erro.wav, etc.)
        └── fonts/           (coloque fontes .ttf aqui, se desejar)

Fluxo do Jogo:
    1. TELA INICIAL   → Título animado com botão "Jogar"
    2. CATEGORIAS     → Seleção: Iniciante / Intermediário / Avançado
    3. CONTAGEM       → 3... 2... 1... Vai!
    4. MEMORIZAR      → Sequência de casas é iluminada
    5. REPRODUZIR     → Jogador clica nas casas na ordem correta
    6. Repete rodadas com dificuldade crescente dentro da categoria

Sequências:
    As sequências geradas seguem caminhos válidos na amarelinha,
    respeitando a adjacência das casas no layout clássico.

Autor: Desenvolvido como trabalho acadêmico - UDESC
Data: Julho/2026
===============================================================================
"""

import pygame
# =============================================================================
# CONSTANTES DE CONFIGURAÇÃO
# =============================================================================

# --- Dimensões da Tela ---
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

# --- Paleta de Cores (RGB) ---
BRANCO         = (255, 255, 255)
PRETO          = (0,   0,   0)
CINZA_CLARO    = (200, 200, 200)
CINZA_ESCURO   = (80,  80,  80)
CINZA_MEDIO    = (140, 140, 140)

# Cores do grid da amarelinha
COR_CASA_NORMAL    = (70,  100, 160)   # Azul escuro (casa padrão)
COR_CASA_BORDA     = (40,  60,  110)   # Borda das casas
COR_CASA_HOVER     = (100, 140, 200)   # Hover do mouse sobre a casa

# Cores de feedback
COR_ILUMINADA      = (255, 220, 50)    # Amarelo (sequência sendo mostrada)
COR_ACERTO         = (50,  200, 80)    # Verde (acerto)
COR_ERRO           = (220, 50,  50)    # Vermelho (erro)
COR_DICA           = (180, 120, 255)   # Roxo (dica/ajuda)
COR_CORRETA_FLASH  = (50,  255, 130)   # Verde claro (mostra casa correta no erro)

# Cores de UI
COR_FUNDO          = (25,  25,  40)    # Fundo da tela
COR_PAINEL         = (35,  35,  55)    # Painel de informações
COR_TEXTO_TITULO   = (255, 220, 50)    # Título
COR_TEXTO_INFO     = (200, 200, 220)   # Informações
COR_TEXTO_PONTOS   = (100, 255, 150)   # Pontuação
COR_TEXTO_FASE     = (255, 180, 80)    # Fase

# Cores para categorias
COR_INICIANTE      = (80,  200, 120)   # Verde suave
COR_INTERMEDIARIO  = (255, 180, 50)    # Laranja/Amarelo
COR_AVANCADO       = (220, 60,  80)    # Vermelho

# Cores de botões
COR_BOTAO          = (60,  80,  140)   # Azul médio
COR_BOTAO_HOVER    = (80,  110, 180)   # Azul claro
COR_BOTAO_BORDA    = (100, 130, 200)   # Borda do botão

# Cores do Modo Competitivo
COR_JOGADOR1       = (80,  180, 255)   # Azul claro (Jogador 1)
COR_JOGADOR2       = (255, 130, 80)    # Laranja (Jogador 2)
COR_OURO           = (255, 215, 0)     # Dourado (vencedor)
COR_PRATA          = (192, 192, 192)   # Prata (segundo lugar)
COR_EMPATE         = (180, 180, 255)   # Lilás (empate)

# --- Dimensões do Grid da Amarelinha ---
# O layout da amarelinha clássica:
#   Casa 9 (topo, sozinha - "Céu")
#   Casas 7 e 8 (lado a lado)
#   Casa 6 (sozinha)
#   Casas 4 e 5 (lado a lado)
#   Casa 3 (sozinha)
#   Casas 1 e 2 (lado a lado)
# (De baixo para cima, como na amarelinha real)

CASA_LARGURA  = 100   # Largura de cada casa
CASA_ALTURA   = 65    # Altura de cada casa
CASA_ESPACO   = 6     # Espaço entre as casas
GRID_OFFSET_X = LARGURA_TELA // 2   # Centro horizontal do grid
GRID_OFFSET_Y = 80                 # Margem superior do grid

# --- Categorias e Fases ---
# Cada categoria tem suas próprias fases de progressão
CATEGORIAS = {
    "INICIANTE": {
        "nome": "Iniciante",
        "cor": COR_INICIANTE,
        "descricao": "Sequências curtas e tempo generoso",
        "icone": "★",
        "max_rodadas": 5,
        "fases": {
            "A": {"SEQ": 3, "TMP": 6.0, "nome": "Fase 1 - Aquecimento"},
            "B": {"SEQ": 3, "TMP": 5.0, "nome": "Fase 2 - Caminhada"},
            "C": {"SEQ": 4, "TMP": 5.0, "nome": "Fase 3 - Trote"},
            "D": {"SEQ": 4, "TMP": 4.0, "nome": "Fase 4 - Corrida Leve"},
        },
        "ordem_fases": ["A", "B", "C", "D"],
    },
    "INTERMEDIARIO": {
        "nome": "Intermediário",
        "cor": COR_INTERMEDIARIO,
        "descricao": "Sequências médias e tempo moderado",
        "icone": "★★",
        "max_rodadas": 7,
        "fases": {
            "A": {"SEQ": 4, "TMP": 4.5, "nome": "Fase 1 - Desafio"},
            "B": {"SEQ": 5, "TMP": 4.0, "nome": "Fase 2 - Ritmo"},
            "C": {"SEQ": 5, "TMP": 3.5, "nome": "Fase 3 - Velocidade"},
            "D": {"SEQ": 6, "TMP": 3.0, "nome": "Fase 4 - Precisão"},
            "E": {"SEQ": 6, "TMP": 2.5, "nome": "Fase 5 - Mestre"},
        },
        "ordem_fases": ["A", "B", "C", "D", "E"],
    },
    "AVANCADO": {
        "nome": "Avançado",
        "cor": COR_AVANCADO,
        "descricao": "Sequências longas e pouco tempo",
        "icone": "★★★",
        "max_rodadas": 10,
        "fases": {
            "A": {"SEQ": 5, "TMP": 3.0, "nome": "Fase 1 - Sprint"},
            "B": {"SEQ": 6, "TMP": 2.5, "nome": "Fase 2 - Turbinado"},
            "C": {"SEQ": 7, "TMP": 2.0, "nome": "Fase 3 - Relâmpago"},
            "D": {"SEQ": 8, "TMP": 1.5, "nome": "Fase 4 - Expert"},
            "E": {"SEQ": 9, "TMP": 1.2, "nome": "Fase 5 - Lenda"},
            "F": {"SEQ": 9, "TMP": 1.0, "nome": "Fase 6 - Imortal"},
        },
        "ordem_fases": ["A", "B", "C", "D", "E", "F"],
    },
}

# --- Adjacência das casas na amarelinha ---
# Define quais casas são vizinhas/acessíveis a partir de cada casa.
# Isso garante que as sequências geradas representem caminhos reais
# que um ser humano poderia percorrer pulando na amarelinha.
#
# Layout (de baixo para cima):
#   Fileira 1 (base):  casas 1 e 2 (lado a lado)  → um pé em cada
#   Fileira 2:         casa 3 (sozinha)            → um pé só
#   Fileira 3:         casas 4 e 5 (lado a lado)   → um pé em cada
#   Fileira 4:         casa 6 (sozinha)             → um pé só
#   Fileira 5:         casas 7 e 8 (lado a lado)    → um pé em cada
#   Fileira 6 (topo):  casa 9 (sozinha - "Céu")    → um pé só
#
# Adjacência: uma casa é vizinha se está na mesma fileira (lado a lado)
# ou na fileira imediatamente acima ou abaixo.
ADJACENCIA = {
    1: [2, 3],         # 1 → vizinho de 2 (mesma fileira), 3 (fileira acima)
    2: [1, 3],         # 2 → vizinho de 1 (mesma fileira), 3 (fileira acima)
    3: [1, 2, 4, 5],   # 3 → vizinho de 1,2 (fileira abaixo), 4,5 (fileira acima)
    4: [3, 5, 6],      # 4 → vizinho de 3 (abaixo), 5 (mesma fileira), 6 (acima)
    5: [3, 4, 6],      # 5 → vizinho de 3 (abaixo), 4 (mesma fileira), 6 (acima)
    6: [4, 5, 7, 8],   # 6 → vizinho de 4,5 (abaixo), 7,8 (acima)
    7: [6, 8, 9],      # 7 → vizinho de 6 (abaixo), 8 (mesma fileira), 9 (acima)
    8: [6, 7, 9],      # 8 → vizinho de 6 (abaixo), 7 (mesma fileira), 9 (acima)
    9: [7, 8],         # 9 → vizinho de 7,8 (fileira abaixo)
}

# --- Timing ---
TEMPO_FLASH_CASA    = 1.5     # Tempo que cada casa fica iluminada na sequência (s)
TEMPO_INTERVALO     = 1.0     # Intervalo entre cada flash da sequência (s)
TEMPO_FEEDBACK      = 0.6     # Tempo que o feedback (verde/vermelho) fica visível (s)
TEMPO_DICA          = 4.0     # Segundos de inatividade antes de mostrar a dica
TEMPO_DICA_FLASH    = 1.5     # Tempo que cada casa pisca na dica (s)
TEMPO_MOSTRA_CORRETA = 1.0   # Tempo para mostrar a casa correta após erro (s)
TEMPO_CONTAGEM      = 1.0    # Tempo de cada número na contagem regressiva (s)

# --- Pontuação ---
PONTOS_ACERTO     = 10    # Pontos por casa correta
PONTOS_BONUS      = 20    # Bônus por sequência completa
PONTOS_DESCONTO   = -10   # Desconto ao usar dica
# Em caso de erro, a pontuação da rodada é zerada


