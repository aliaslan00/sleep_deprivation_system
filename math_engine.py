import numpy as np


class EyeMetricsCalculator:
    """
    Göz koordinatları üzerinden geometrik analiz yapan matematik motoru.
    Mühendislik Terimi: Deterministic Mathematical Model
    """

    # MediaPipe Face Mesh standart sol ve sağ göz indeksleri (Landmark IDs)
    # P1, P2, P3, P4, P5, P6 sırasıyla: [Dış Köşe, Üst1, Üst2, İç Köşe, Alt1, Alt2]
    LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

    @staticmethod
    def calculate_euclidean_distance(point1: np.ndarray, point2: np.ndarray) -> float:
        """
        İki nokta arasındaki Öklid mesafesini vektörel olarak hesaplar.
        Optimized via NumPy L2 Norm (math.sqrt'a göre çok daha hızlıdır).
        """
        return np.linalg.norm(point1 - point2)

    def calculate_ear(self, eye_landmarks: np.ndarray) -> float:
        """
        EAR (Eye Aspect Ratio) hesaplama fonksiyonu.
        Formül: (|P2-P6| + |P3-P5|) / (2 * |P1-P4|)
        """
        # Dikey mesafelerin hesaplanması (Vertical Distances)
        v_dist1 = self.calculate_euclidean_distance(eye_landmarks[1], eye_landmarks[5])
        v_dist2 = self.calculate_euclidean_distance(eye_landmarks[2], eye_landmarks[4])

        # Yatay mesafenin hesaplanması (Horizontal Distance)
        h_dist = self.calculate_euclidean_distance(eye_landmarks[0], eye_landmarks[3])

        # EAR Oranı
        ear = (v_dist1 + v_dist2) / (2.0 * h_dist)
        return ear

    def get_eyes_average_ear(self, face_landmarks, frame_width: int, frame_height: int) -> float:
        """
        Yüz landmark matrisinden göz koordinatlarını izole eder, piksel
        uzayına normalize eder ve iki gözün EAR ortalamasını döner.
        """
        # Ham normalize koordinatları piksel koordinatlarına dönüştürme (Denormalization)
        landmarks = np.array([(pt.x * frame_width, pt.y * frame_height) for pt in face_landmarks.landmark])

        left_eye_pts = landmarks[self.LEFT_EYE_IDX]
        right_eye_pts = landmarks[self.RIGHT_EYE_IDX]

        left_ear = self.calculate_ear(left_eye_pts)
        right_ear = self.calculate_ear(right_eye_pts)

        # Bi-ocular (İki gözün) ortalaması gürültüyü azaltır
        return (left_ear + right_ear) / 2.0