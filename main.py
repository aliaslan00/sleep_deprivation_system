import cv2
from config import FRAME_WIDTH, FRAME_HEIGHT
from math_engine import EyeMetricsCalculator
from face_processor import FaceProcessor
from alarm_manager import AlarmManager


def main():
    """
    Sistemi başlatan, donanım girdi hatlarını (Video I/O) yöneten ana orkestrasyon fonksiyonu.
    Mühendislik Terimi: Runtime Orchestrator
    """
    # Pencere ismini merkezi bir değişkende tutuyoruz (String Literal yerine Constant)
    WINDOW_NAME = "Anti-Sleep Driver Safety System"

    # Nesne İlklendirmeleri (Dependency Injection)
    camera = cv2.VideoCapture(0)  # Varsayılan dahili/harici web kamerası
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    processor = FaceProcessor()
    calculator = EyeMetricsCalculator()
    manager = AlarmManager()

    # OpenCV penceresini döngüden önce açıkça oluşturuyoruz
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)

    print(f"[{WINDOW_NAME}] Görüntü işleme pipeline'ı aktif.")
    print("-> Kapatmak için klavyeden 'q' tuşuna basabilir veya pencerenin 'X' butonunu kullanabilirsiniz.")

    try:
        while camera.isOpened():
            success, frame = camera.read()
            if not success:
                print("[HATA] Kamera akışı kesildi.")
                break

            # Frame optimizasyonu: Aynalama efekti (Görsel ergonomi için)
            frame = cv2.flip(frame, 1)

            # 1. Adım: Görüntüyü İşle (Yüz Ağını Çıkar)
            face_landmarks = processor.process_frame(frame)

            face_detected = face_landmarks is not None
            current_ear = 0.0

            if face_detected:
                # 2. Adım: Matematik Motoru ile EAR Değerini Hesapla
                current_ear = calculator.get_eyes_average_ear(face_landmarks, FRAME_WIDTH, FRAME_HEIGHT)

                # Ekranda göz koordinatlarını debug etmek amaçlı görselleştirme (Telemetry Feed)
                cv2.putText(frame, f"EAR: {current_ear:.2f}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # 3. Adım: FSM Güncellemesi ve Alarm Kontrolü
            is_drowsy, closed_time = manager.update_state(current_ear, face_detected)

            # UI Üzerinde Durum Bilgisi Gösterme
            if is_drowsy:
                cv2.putText(frame, f"!!! TEHLIKE: UYKU TESPIT EDILDI !!! ({closed_time:.1f}s)", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elif face_detected and current_ear < 0.24:
                cv2.putText(frame, f"Goz Kapali: {closed_time:.1f}s", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            # Canlı Video Penceresi Güncellemesi
            cv2.imshow(WINDOW_NAME, frame)

            # ---- KESME YÖNETİMİ (INTERRUPT HANDLING) ----

            # Kontrol A: Klavyeden 'q' tuşuna basıldıysa döngüyü kır
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Kontrol B: Kullanıcı pencerenin çarpı (X) butonuna bastıysa döngüyü kır
            # cv2.getWindowProperty pencerenin ekranda görünür olup olmadığını denetler (Görünmüyorsa -1 veya 0 döner)
            if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break

    finally:
        # Donanım kaynaklarının güvenli bir şekilde kapatılması (Resource Cleanup)
        print("[SİSTEM KAPATILIYOR] Donanım kaynakları serbest bırakılıyor...")
        camera.release()
        processor.release_resources()
        cv2.destroyAllWindows()
        print("[SİSTEM] Güvenli şekilde sonlandırıldı.")


if __name__ == "__main__":
    main()