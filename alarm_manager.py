import time
import pygame
from config import EAR_THRESHOLD, SLEEP_DURATION_THRESHOLD_SEC, ALARM_SOUND_PATH


class AlarmManager:
    """
    Sonlu Durum Makinesi (Finite State Machine - FSM) prensibiyle sürücü durumunu
    ve asenkron alarm tetiklemelerini yöneten kontrolör katmanı.
    Mühendislik Terimi: State-Driven Alert System
    """

    def __init__(self):
        # Pygame ses mikserini ilklendiriyoruz (Main Thread'i engellemez)
        pygame.mixer.init()
        self.alarm_sound_path = ALARM_SOUND_PATH
        self.is_alarm_playing = False

        # FSM Durum Değişkenleri
        self.eye_closed_start_time = None
        self.is_drowsy = False

    def trigger_alarm(self):
        """Alarmı arka planda (Thread-safe benzeri) çalar."""
        if not self.is_alarm_playing:
            try:
                pygame.mixer.music.load(self.alarm_sound_path)
                pygame.mixer.music.play(-1)  # -1 parametresi sesin döngüsel (loop) çalmasını sağlar
                self.is_alarm_playing = True
            except Exception as e:
                print(f"[MÜHENDİSLİK UYARISI] Ses dosyası yüklenemedi: {e}")

    def stop_alarm(self):
        """Alarmı durdurur ve ses kanalını serbest bırakır."""
        if self.is_alarm_playing:
            pygame.mixer.music.stop()
            self.is_alarm_playing = False

    def update_state(self, current_ear: float, face_detected: bool):
        """
        Gelen EAR verisine göre FSM geçişlerini yürütür.
        Edge-Case: face_detected False ise (yüz kaybolduysa) zamanlayıcıyı
        sıfırlamaz, son durumu korur (State Retention).
        """
        if not face_detected:
            # Yüz algılanamadıysa analitik olarak kararsız durumdayız.
            # Sayacı sıfırlama, sistemi dondur ve bir sonraki kareyi bekle.
            return self.is_drowsy, 0.0

        elapsed_time = 0.0

        # DURUM 1: Göz Eşik Değerinin Altında (Kapalı)
        if current_ear < EAR_THRESHOLD:
            if self.eye_closed_start_time is None:
                # Gözün kapandığı anlık zaman damgası (Timestamp) alınır
                self.eye_closed_start_time = time.time()
            else:
                # Gözün ne kadar süredir kapalı kaldığı hesaplanır
                elapsed_time = time.time() - self.eye_closed_start_time

            # Eğer geçen süre kritik eşiği aşmışsa alarm durumuna geç
            if elapsed_time >= SLEEP_DURATION_THRESHOLD_SEC:
                self.is_drowsy = True
                self.trigger_alarm()

        # DURUM 2: Göz Açık
        else:
            self.eye_closed_start_time = None
            self.is_drowsy = False
            self.stop_alarm()

        return self.is_drowsy, elapsed_time