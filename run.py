"""
run.py - Uygulamanın giriş noktası (başlatma dosyası).

Çalıştırmak için (sanal ortam aktifken):
    python run.py
Sonra tarayıcıdan: http://127.0.0.1:5000
"""

from app import create_app

# create_app() -> "Application Factory" deseni: uygulamayı bir fonksiyon içinde
# oluştururuz. Böylece test, geliştirme ve canlı ortam için farklı ayarlarla
# aynı uygulamayı üretebiliriz.
app = create_app()

if __name__ == "__main__":
    # debug=True -> kod değişince sunucu kendini yeniden başlatır ve hata
    #               olursa detaylı hata sayfası gösterir. CANLIDA ASLA True olmamalı!
    # host="127.0.0.1" -> sadece kendi bilgisayarımızdan erişilebilir.
    # port=5000 -> tarayıcıda açacağımız port numarası.
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
