"""
===============================================================================
CAMERA_POSE: Ponte entre a câmera (MediaPipe) e o jogo AMAR-É-LINDO
===============================================================================
Este módulo faz duas coisas:
    1. Captura a webcam e detecta a pose do jogador (MediaPipe Pose Landmarker).
    2. Converte a posição dos pés (coordenadas da câmera) para o espaço virtual
       do jogo (LARGURA_TELA x ALTURA_TELA), usando uma transformação de
       perspectiva — a mesma técnica do slide 48-62 do material do professor,
       só que aplicada a um ponto em vez de uma imagem inteira.

Como calibrar (fazer uma vez, com o tapete/área de jogo já posicionado):
    1. Rode este arquivo diretamente: python camera_pose.py
    2. Clique nos 4 cantos da área de jogo na janela da câmera, na ordem:
       1) superior-esquerdo  2) superior-direito
       3) inferior-esquerdo  4) inferior-direito
    3. As coordenadas serão impressas no terminal — copie para
       PONTOS_CAMERA em constants.py (ou direto abaixo, se preferir).
===============================================================================
"""

import cv2
import numpy as np
import mediapipe as mp

# =============================================================================
# CONFIGURAÇÃO — ajuste conforme seu setup físico
# =============================================================================
CAMINHO_MODELO = "pose_landmarker_full.task"

# IDs dos landmarks dos pés (ver slide 65 do material — MediaPipe Pose)
LEFT_ANKLE = 27
RIGHT_ANKLE = 28
LEFT_FOOT_INDEX = 31
RIGHT_FOOT_INDEX = 32

# Pontos dos 4 cantos da área de jogo, DENTRO DA IMAGEM DA CÂMERA (pixels).
# Preencha depois de calibrar (rodando este arquivo isoladamente).
# Ordem: [superior-esquerdo, superior-direito, inferior-esquerdo, inferior-direito]
PONTOS_CAMERA = np.float32([
    [80, 60],
    [560, 60],
    [80, 420],
    [560, 420],
])


class DetectorPose:
    """
    Encapsula o MediaPipe PoseLandmarker + a transformação de perspectiva
    que converte posição do pé (câmera) -> posição no grid do jogo.
    """

    def __init__(self, largura_jogo, altura_jogo, pontos_camera=PONTOS_CAMERA,
                 caminho_modelo=CAMINHO_MODELO, indice_camera=0, mostrar_debug=True):
        self.largura_jogo = largura_jogo
        self.altura_jogo = altura_jogo
        self.mostrar_debug = mostrar_debug
        self.pontos_camera = pontos_camera

        # --- Configura o MediaPipe em modo VÍDEO (streaming contínuo) ---
        base_options = mp.tasks.BaseOptions(model_asset_path=caminho_modelo)
        options = mp.tasks.vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.landmarker = mp.tasks.vision.PoseLandmarker.create_from_options(options)

        # --- Matriz de transformação: câmera -> espaço do jogo ---
        pontos_jogo = np.float32([
            [0, 0],
            [largura_jogo, 0],
            [0, altura_jogo],
            [largura_jogo, altura_jogo],
        ])
        self.matriz = cv2.getPerspectiveTransform(pontos_camera, pontos_jogo)

        # --- Captura de câmera ---
        self.cap = cv2.VideoCapture(indice_camera)
        self._timestamp_ms = 0

    def _mapear_para_jogo(self, x_cam, y_cam):
        """Aplica a matriz de perspectiva a um único ponto (x, y) da câmera."""
        ponto = np.array([[[x_cam, y_cam]]], dtype=np.float32)
        ponto_transformado = cv2.perspectiveTransform(ponto, self.matriz)
        x_jogo, y_jogo = ponto_transformado[0][0]
        return int(x_jogo), int(y_jogo)

    def detectar_posicao_pe(self):
        """
        Lê um frame da câmera, detecta a pose e retorna a posição do(s) pé(s)
        já convertida para o espaço do jogo.

        Se mostrar_debug=True (padrão), também abre/atualiza uma janela do
        OpenCV mostrando a câmera ao vivo, com:
            - Um retângulo amarelo marcando a área calibrada (os 4 pontos)
            - Um círculo verde na posição detectada do pé

        Retorna:
            (x, y) no espaço do jogo, ou None se nenhuma pessoa foi detectada
            ou se o pé estiver fora da área calibrada.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        self._timestamp_ms += 33  # ~30 fps; ajuste se necessário
        resultado = self.landmarker.detect_for_video(mp_image, self._timestamp_ms)

        pos_jogo = None
        x_cam, y_cam = None, None

        if resultado.pose_landmarks:
            landmarks = resultado.pose_landmarks[0]
            altura_frame, largura_frame = frame.shape[:2]

            # Usa a média dos dois tornozelos como "posição do jogador"
            # (mais estável que usar um pé só, que pode estar levantado)
            #pe_esq = landmarks[LEFT_ANKLE]
            #pe_dir = landmarks[RIGHT_ANKLE]
            #x_norm = (pe_esq.x + pe_dir.x) / 2
            #y_norm = (pe_esq.y + pe_dir.y) / 2

            # Exemplo se quiser mudar temporariamente no camera_pose.py:
            nariz = landmarks[0]
            x_cam = (1.0 - nariz.x) * largura_frame
            y_cam = nariz.y * altura_frame

            #x_cam = x_norm * largura_frame
            #y_cam = y_norm * altura_frame
            pos_jogo = self._mapear_para_jogo(x_cam, y_cam)

        if self.mostrar_debug:
            self._mostrar_janela_debug(frame, x_cam, y_cam, pos_jogo)

        return pos_jogo

    def _mostrar_janela_debug(self, frame, x_cam, y_cam, pos_jogo):
        """Desenha a área calibrada e o ponto detectado, e exibe a janela."""
        frame_debug = frame.copy()

        # Desenha a área calibrada (os 4 cantos que você marcou na calibração)
        pontos = self.pontos_camera.astype(int)
        cv2.polylines(frame_debug, [pontos[[0, 1, 3, 2]]], isClosed=True,
                      color=(0, 255, 255), thickness=2)

        # Desenha o ponto detectado do pé (se houver)
        if x_cam is not None:
            cv2.circle(frame_debug, (int(x_cam), int(y_cam)), 10, (0, 255, 0), -1)
            texto = f"Jogo: {pos_jogo}" if pos_jogo else "Fora da area"
            cv2.putText(frame_debug, texto, (int(x_cam) + 15, int(y_cam)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            cv2.putText(frame_debug, "Nenhuma pessoa detectada", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("AMAR-E-LINDO - Camera (debug)", frame_debug)
        # Necessario para o OpenCV atualizar a janela no Windows
        cv2.waitKey(1)

    def liberar(self):
        self.cap.release()
        self.landmarker.close()
        cv2.destroyAllWindows()


# =============================================================================
# MODO DE CALIBRAÇÃO: rode "python camera_pose.py" para descobrir os 4 pontos
# =============================================================================
if __name__ == "__main__":
    pontos_clicados = []

    def _on_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(pontos_clicados) < 4:
            pontos_clicados.append((x, y))
            print(f"Ponto {len(pontos_clicados)}: [{x}, {y}]")

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Calibracao - clique nos 4 cantos da area de jogo")
    cv2.setMouseCallback("Calibracao - clique nos 4 cantos da area de jogo", _on_click)

    print("Clique na ordem: 1) sup-esquerdo 2) sup-direito 3) inf-esquerdo 4) inf-direito")
    print("Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for i, (px, py) in enumerate(pontos_clicados):
            cv2.circle(frame, (px, py), 6, (0, 255, 0), -1)
            cv2.putText(frame, str(i + 1), (px + 8, py), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

        cv2.imshow("Calibracao - clique nos 4 cantos da area de jogo", frame)

        if len(pontos_clicados) == 4:
            print("\nCopie isso para PONTOS_CAMERA em camera_pose.py:")
            print(f"PONTOS_CAMERA = np.float32({pontos_clicados})")

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()