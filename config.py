"""
Sistem Hiperparametreleri ve Konfigürasyon Yönetimi
Mühendislik Terimi: Centralized Configuration Management
"""

# Gözün kapalı sayılması için EAR eşik değeri
# Kalibrasyon yapılana kadar baseline (taban çizgisi) olarak kullanılacaktır.
EAR_THRESHOLD = 0.24

# Sürücünün uykuda olduğunu doğrulamak için gözlerin ardışık olarak kaç saniye kapalı kalması gerektiği
# Mikro-uykuları (Micro-sleep) yakalamak için 1.5 - 2.0 saniye endüstri standardıdır.
SLEEP_DURATION_THRESHOLD_SEC = 2.0

# Görüntü işleme penceremizin boyutları
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Alarm ses dosyasının yolu (Path)
ALARM_SOUND_PATH = "alarm.wav"