"""
app paketi - Uygulamanın kendisi.

KATMANLI MİMARİ (3 katman):
    app/presentation/  -> SUNUM katmanı : Kullanıcının gördüğü sayfalar ve URL'ler
    app/services/      -> İŞ katmanı    : OCR, alan eşleme, doğrulama, dışa aktarma
    app/data/          -> VERİ katmanı  : Veritabanı modelleri ve veri erişimi

Kural: Her katman sadece BİR ALTINDAKİ katmanla konuşur.
    Sunum -> İş -> Veri
Sunum katmanı veritabanına DOĞRUDAN erişmez.
"""

import os

from flask import Flask

from config import config_by_name


def create_app(config_name=None):
    """
    Flask uygulamasını oluşturur ve yapılandırır (Application Factory).

    Parametre:
        config_name -> "development", "testing" veya "production".
                       Verilmezse .env içindeki FLASK_ENV okunur,
                       o da yoksa "development" kullanılır.
    Döndürür:
        Hazır Flask uygulama nesnesi.
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    # template_folder ve static_folder -> HTML ve CSS dosyaları sunum katmanında
    # durduğu için Flask'a yerlerini açıkça söylüyoruz.
    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="presentation/static",
    )

    # Seçilen ortamın ayarlarını uygulamaya yükle.
    app.config.from_object(config_by_name[config_name])

    # uploads klasörü yoksa oluştur (exist_ok=True -> varsa hata verme).
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Blueprint -> URL'leri modüllere bölmemizi sağlayan Flask yapısı.
    # Sunum katmanındaki sayfaları uygulamaya kaydediyoruz.
    from app.presentation.routes import main_bp

    app.register_blueprint(main_bp)

    return app
