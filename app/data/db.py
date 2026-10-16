"""
db.py - Veritabanı bağlantısı.

Veri katmanındaki TÜM dosyalar bağlantıyı buradan alır.
Bağlantı adresi .env dosyasındaki DATABASE_URL değişkenidir:
    postgresql://kullanici:sifre@sunucu:port/veritabani_adi
    Örnek: postgresql://postgres:Belge2026@localhost:5432/belgematik
"""

import os

import psycopg
from psycopg.rows import dict_row

# config.py import edilince .env dosyası okunur (load_dotenv orada çalışır).
import config  # noqa: F401  (sadece .env'yi yüklemek için)


def baglanti(url=None):
    """
    PostgreSQL'e yeni bir bağlantı açar ve döndürür.

    Parametre:
        url -> Bağlantı adresi. Verilmezse .env içindeki DATABASE_URL kullanılır.

    Ayarlar:
        row_factory=dict_row -> Sorgu sonuçları sözlük (dict) olarak gelir:
                                {"id": 1, "email": "..."}  (sütun adıyla erişilir)
        autocommit=True      -> Her komut çalıştığı anda kalıcı olur (COMMIT).
                                Birden fazla komutu "ya hep ya hiç" çalıştırmak
                                istediğimizde  `with conn.transaction():`  kullanırız.

    Kullanım (with bloğu bitince bağlantı otomatik kapanır):
        with baglanti() as conn:
            kullanici_repo.listele(conn)
    """
    url = url or os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL tanımlı değil. .env dosyasına şu satırı ekleyin:\n"
            "DATABASE_URL=postgresql://postgres:SIFRENIZ@localhost:5432/belgematik"
        )
    return psycopg.connect(url, row_factory=dict_row, autocommit=True)
