import pygame

pygame.init()

# Constantes para a tela
LARGURA_TELA = 640
ALTURA_TELA = 480
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Amarelinha Virtual")

clock = pygame.time.Clock()
running = True

# Configurações dos blocos da amarelinha
TAMANHO_BLOCO = 60
CENTRO_X = LARGURA_TELA // 2
ESPESSURA_LINHA = 4

# Fonte para os números (preta, como na imagem)
fonte = pygame.font.SysFont("Arial", 40, bold=True)

# Dicionário com as informações de cada casa da amarelinha
# As cores foram aproximadas da imagem de referência
casas = [
    {"num": "1", "rect": [CENTRO_X - TAMANHO_BLOCO//2, 400, TAMANHO_BLOCO, TAMANHO_BLOCO], "cor": (250, 190, 20)},
    {"num": "2", "rect": [CENTRO_X - TAMANHO_BLOCO, 340, TAMANHO_BLOCO, TAMANHO_BLOCO], "cor": (0, 150, 150)},
    {"num": "3", "rect": [CENTRO_X, 340, TAMANHO_BLOCO, TAMANHO_BLOCO], "cor": (170, 220, 255)},
    {"num": "4", "rect": [CENTRO_X - TAMANHO_BLOCO//2, 280, TAMANHO_BLOCO, TAMANHO_BLOCO], "cor": (140, 40, 180)},
    {"num": "5", "rect": [CENTRO_X - TAMANHO_BLOCO, 220, TAMANHO_BLOCO, TAMANHO_BLOCO], "cor": (100, 140, 40)},
    {"num": "6", "rect": [CENTRO_X, 220, TAMANHO_BLOCO, TAMANHO_BLOCO], "cor": (255, 150, 180)},
    {"num": "7", "rect": [CENTRO_X - TAMANHO_BLOCO//2, 160, TAMANHO_BLOCO, TAMANHO_BLOCO], "cor": (235, 70, 60)},
    {"num": "8", "rect": [CENTRO_X - TAMANHO_BLOCO, 100, TAMANHO_BLOCO, TAMANHO_BLOCO], "cor": (110, 80, 70)},
    {"num": "9", "rect": [CENTRO_X, 100, TAMANHO_BLOCO, TAMANHO_BLOCO], "cor": (60, 170, 240)},
]

# Inicia o loop principal do jogo
while running:
    pos = pygame.mouse.get_pos()

    # Fundo da tela (cinza claro para destacar as cores)
    tela.fill((230, 230, 230))

    # --- DESENHANDO A AMARELINHA ---
    
    # 1. Desenha o bloco 10 (Semicírculo no topo)
    raio_10 = TAMANHO_BLOCO
    centro_10 = (CENTRO_X, 100)
    cor_10 = (140, 200, 60)
    
    # Desenha o preenchimento do semicírculo
    pygame.draw.circle(tela, cor_10, centro_10, raio_10, draw_top_left=True, draw_top_right=True)
    # Desenha o contorno do semicírculo
    pygame.draw.circle(tela, "black", centro_10, raio_10, width=ESPESSURA_LINHA, draw_top_left=True, draw_top_right=True)
    
    # Texto do bloco 10
    texto_10 = fonte.render("CÉU", True, "black")
    x_texto_10 = CENTRO_X - texto_10.get_width() // 2 - 3
    y_texto_10 = 100 - raio_10 + 18 # Um pouco abaixo do topo do arco
    tela.blit(texto_10, (x_texto_10, y_texto_10))


    # 2. Desenha os blocos de 1 a 9 (Retângulos)
    for casa in casas:
        retangulo = casa["rect"]
        
        # Preenchimento
        pygame.draw.rect(tela, casa["cor"], retangulo)
        # Contorno preto
        pygame.draw.rect(tela, "black", retangulo, ESPESSURA_LINHA)
        
        # Renderiza o texto (número)
        texto_num = fonte.render(casa["num"], True, "black")
        
        # Centraliza o texto dentro do bloco correspondente
        largura_texto = texto_num.get_width()
        altura_texto = texto_num.get_height()
        texto_x = retangulo[0] + (TAMANHO_BLOCO - largura_texto) // 2
        texto_y = retangulo[1] + (TAMANHO_BLOCO - altura_texto) // 2
        
        tela.blit(texto_num, (texto_x, texto_y))


    # Círculos do mouse (mantidos do seu código original)
    pygame.draw.circle(tela, "white", pos, 5)
    pygame.draw.circle(tela, "black", pos, 3)

    # Observa os eventos de teclado e mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza a tela com tudo o que foi desenhado
    pygame.display.flip()

    # Controla a taxa de quadros (FPS)
    clock.tick(60)

pygame.quit()