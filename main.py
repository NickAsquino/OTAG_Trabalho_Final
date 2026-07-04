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
import random
import sys
import os
import time
import math

# =============================================================================
# COMPATIBILIDADE WINDOWS (encoding do console)
# =============================================================================
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass  # Fallback caso o terminal nao suporte reconfigure

# =============================================================================
# INICIALIZAÇÃO DO PYGAME
# =============================================================================
pygame.init()
pygame.mixer.init()


from game import JogoAmarelinha

# =============================================================================
# PONTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    jogo = JogoAmarelinha()
    jogo.executar()
