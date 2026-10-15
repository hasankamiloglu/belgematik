"""
config.py - Uygulama ayarları (yapılandırma).

Gizli bilgiler (şifre, API anahtarı) KODUN İÇİNE YAZILMAZ.
.env dosyasından okunur. .env dosyası .gitignore sayesinde GitHub'a gitmez.
"""

import os

from dotenv import load_dotenv

# load_dotenv() -> proje klasöründeki .env dosyasını okuyup içindeki
# değerleri ortam değişkeni (environment variable) olarak yükler.
load_dotenv()

# Projenin ana klasörünün tam yolu (dosya yollarını buna göre kuruyoruz).
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Tüm ortamlarda ortak olan temel ayarlar."""

    # SECRET_KEY -> Flask'ın oturum (session) ve form güvenliği için kullandığı
    # gizli anahtar. .env içinde yoksa sadece geliştirme için yedek değer kullanılır.
    SECRET_KEY = os.getenv("SECRET_KEY", "gelistirme-icin-gecici-anahtar")

    # DATABASE_URL -> PostgreSQL bağlantı adresi (4. haftada kullanılacak).
    # Biçim: postgresql://kullanici:sifre@sunucu:port/veritabani_adi
    DATABASE_URL = os.getenv("DATABASE_URL", "")

    # Yüklenen belge fotoğraflarının kaydedileceği klasör.
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    # MAX_CONTENT_LENGTH -> tek seferde yüklenebilecek en büyük dosya boyutu.
    # 10 * 1024 * 1024 = 10 MB. Daha büyük dosyada Flask otomatik 413 hatası verir.
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # Kabul edilen dosya uzantıları (fotoğraf ve PDF).
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

    # CORS_ORIGINS -> Backend'e istek atmasına izin verilen frontend adresleri.
    # React geliştirme sunucusu varsayılan olarak 5173 portunda çalışır.
    # .env içinde virgülle ayırarak değiştirilebilir (canlıda frontend'in adresi yazılır).
    CORS_ORIGINS = [
        adres.strip()
        for adres in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
    ]

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Kendi bilgisayarımızda geliştirme yaparken kullanılan ayarlar."""

    DEBUG = True


class TestingConfig(Config):
    """Otomatik testler çalışırken kullanılan ayarlar."""

    TESTING = True


class ProductionConfig(Config):
    """Canlı (production) sunucuda kullanılan ayarlar."""

    DEBUG = False


# Ortam adı -> ayar sınıfı eşlemesi.
# .env içindeki FLASK_ENV değeri hangi ayarın kullanılacağını belirler.
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
