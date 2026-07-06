import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

# Configuração do PoseLandmarker para rodar em modo de imagem
options = mp.tasks.vision.PoseLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(
        model_asset_path="pose_landmarker_full.task"
    ),
    running_mode=mp.tasks.vision.RunningMode.IMAGE,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)

# Inicializa Captura de Vídeo OpenCV (0 para webcam, ou caminho para vídeo)
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("video/video_para_testar_mediapipe.mp4")

with mp.tasks.vision.PoseLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        annotated_image = frame.copy()

        # Converte o frame e roda o detector
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
        )
        results = landmarker.detect(mp_image)

        if results.pose_landmarks:
            for pose_landmarks in results.pose_landmarks:
                # Converte os landmarks para o formato do desenho
                proto = landmark_pb2.NormalizedLandmarkList()
                proto.landmark.extend(
                    [
                        landmark_pb2.NormalizedLandmark(x=l.x, y=l.y, z=l.z)
                        for l in pose_landmarks
                    ]
                )

                # Desenha apenas na imagem anotada
                mp.solutions.drawing_utils.draw_landmarks(
                    annotated_image, proto, mp.solutions.pose.POSE_CONNECTIONS
                )

                # Print do Nariz (ID 0)
                nose = pose_landmarks[0]
                print(f"Nariz -> X: {nose.x:.4f}, Y: {nose.y:.4f}")

        # Agora temos as duas telas de volta!
        cv2.imshow("MediaPipe Tasks", annotated_image)
        cv2.imshow("Original", frame)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
