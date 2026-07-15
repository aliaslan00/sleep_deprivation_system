import cv2
import numpy as np
import mediapipe as mp
# ÇÖZÜM A: solutions modülünü doğrudan hafızaya zorla yüklüyoruz (Explicit Import)
import mediapipe.python.solutions.face_mesh as mp_face_mesh
from config import FRAME_WIDTH, FRAME_HEIGHT


class FaceProcessor:
    """
    Kameradan gelen video akışını işleyen ve MediaPipe Face Mesh
    modeli ile yüz koordinatlarını çıkaran bağımsız pipeline katmanı.
    """

    def __init__(self):
        # Üst nesne yerine direkt import ettiğimiz sınıfı ilklendiriyoruz
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

    def process_frame(self, frame: np.ndarray):
        """
        Gelen ham matrisi (frame) işler, RGB dönüşümü yapar ve yüz landmark'larını döner.
        """
        frame.flags.writeable = False
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb_frame)

        frame.flags.writeable = True

        if results.multi_face_landmarks:
            return results.multi_face_landmarks[0]

        return None

    def release_resources(self):
        """
        Donanım kaynaklarını temizler.
        """
        self.face_mesh.close()