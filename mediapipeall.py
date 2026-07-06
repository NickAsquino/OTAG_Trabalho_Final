import os
import sys

import cv2
import mediapipe as mp
from mediapipe.tasks import python

import pygame

PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "pose_landmarker_full.task")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Modelo do MediaPipe não encontrado em: {MODEL_PATH}. "
        "Coloque o arquivo pose_landmarker_full.task na pasta do projeto."
    )

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

LARGURA_TELA = 630
ALTURA_TELA = 480
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Piano Virtual Tasks - Live Stream")
fonte = pygame.font.SysFont("Arial", 40, bold=True, italic=True)

# Configuração das Teclas
INICIO_E_TECLAS = 240
LARGURA_TECLA = 90
ALTURA_TECLA = 280

teclas_info = [
    {"cor": "red", "nota": "DÓ", "som": "sons/do.mp3", "x": 0},
    {"cor": "orange", "nota": "RÉ", "som": "sons/re.mp3", "x": 90},
    {"cor": "yellow", "nota": "MI", "som": "sons/mi.mp3", "x": 180},
    {"cor": "green", "nota": "FÁ", "som": "sons/fa.mp3", "x": 270},
    {"cor": "pink", "nota": "SOL", "som": "sons/sol.mp3", "x": 360},
    {"cor": "purple", "nota": "LÁ", "som": "sons/la.mp3", "x": 450},
    {"cor": "blue", "nota": "SI", "som": "sons/si.mp3", "x": 540},
]

# Carrega os sons
for tecla in teclas_info:
    if os.path.exists(tecla["som"]):
        tecla["objeto_som"] = pygame.mixer.Sound(tecla["som"])
        tecla["canal"] = None
    else:
        tecla["objeto_som"] = None

# Variável global
pos_cursor = None


# Função de callback para o MediaPipe Tasks
def receber_resultado(result, output_image, timestamp_ms):
    global pos_cursor
    if result.pose_landmarks:
        landmarks = result.pose_landmarks[0]
        nariz = landmarks[0]  # Índice 0 é o Nariz
        # Converte as coordenadas normalizadas diretamente para pixels da tela
        pos_cursor = (int(nariz.x * LARGURA_TELA), int(nariz.y * ALTURA_TELA))
    else:
        pos_cursor = None


# Configuração do MediaPipe Tasks para LIVE_STREAM
options = PoseLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.LIVE_STREAM,
    result_callback=receber_resultado,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)


def abrir_camera(indices=(0, 1, 2)):
    for idx in indices:
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            print(f"Webcam aberta no índice {idx}")
            return cap
        cap.release()

    raise RuntimeError(
        "Nenhuma câmera foi encontrada. Conecte uma webcam ou altere o índice da câmera."
    )


camera_index = int(os.environ.get("CAMERA_INDEX", "0"))
cap = abrir_camera((camera_index, 0, 1, 2))
# cap = cv2.VideoCapture("video/video_para_testar_mediapipe.mp4")
clock = pygame.time.Clock()

with PoseLandmarker.create_from_options(options) as landmarker:
    executando = True

    while cap.isOpened() and executando:
        # Trata eventos do Pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Espelha horizontalmente

        # Prepara a imagem para o MediaPipe
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

        # Envio Assíncrono: Pega o tempo atual em milissegundos e envia para processamento
        timestamp_atual = pygame.time.get_ticks()
        landmarker.detect_async(mp_image, timestamp_atual)

        # Interface do Pygame (Usa o 'pos_cursor' atualizado pelo callback em background)
        tela.fill((0, 0, 0))
        pygame.draw.line(
            tela,
            "white",
            (0, INICIO_E_TECLAS),
            (LARGURA_TELA, INICIO_E_TECLAS),
            10,
        )

        # Desenha o cabeçalho
        pygame.draw.ellipse(tela, "yellow", (80, 35, 440, 100), 5)
        texto_titulo = fonte.render("Piano Virtual", True, "white")
        tela.blit(texto_titulo, (180, 60))

        # Loop para desenhar e checar colisões das teclas
        for tecla in teclas_info:
            cor_atual = tecla["cor"]

            if pos_cursor:
                x_dentro = (
                    tecla["x"] <= pos_cursor[0] < (tecla["x"] + LARGURA_TECLA)
                )
                y_dentro = pos_cursor[1] >= INICIO_E_TECLAS

                if x_dentro and y_dentro:
                    cor_atual = "black"  # Altera a cor se pressionado

                    # Toca o som sem floodar o canal
                    if tecla["objeto_som"] and (
                        tecla["canal"] is None or not tecla["canal"].get_busy()
                    ):
                        tecla["canal"] = tecla["objeto_som"].play()

            # Desenha a tecla correspondente
            pygame.draw.rect(
                tela,
                cor_atual,
                [tecla["x"], INICIO_E_TECLAS, LARGURA_TECLA, ALTURA_TECLA],
            )

            # Desenha o texto da nota musical
            texto_nota = fonte.render(
                tecla["nota"],
                True,
                "white" if cor_atual != "white" else "black",
            )
            tela.blit(texto_nota, (tecla["x"] + 15, 400))

        # Desenha o cursor (utilizando a posição rastreada no callback)
        if pos_cursor:
            pygame.draw.circle(tela, "white", pos_cursor, 8)
            pygame.draw.circle(tela, "black", pos_cursor, 5)

        # Atualiza a tela e limita a taxa de quadros (60 FPS mantém o Pygame estável)
        pygame.display.flip()
        clock.tick(60)

        # Mostra o feedback da câmera OpenCV
        cv2.imshow("MediaPipe Tasks - Modo Live Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
