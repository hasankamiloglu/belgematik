"""
routes.py - Sunum katmanındaki URL tanımları.

Hafta 3: Sadece iskeletin çalıştığını gösteren sayfalar var.
Sonraki haftalarda yükleme, sonuç, düzeltme ve dışa aktarma sayfaları eklenecek.
"""

from flask import Blueprint, jsonify, render_template

# Blueprint("main", __name__) -> "main" adında bir URL grubu oluşturur.
# İleride "auth" (giriş/kayıt) ve "documents" (belgeler) gibi gruplar eklenecek.
main_bp = Blueprint("main", __name__)

# Ana modüller listesi: ana sayfada yol haritası olarak gösteriliyor.
# durum -> "hazir" (tamamlandı) veya "planli" (ileriki haftalarda)
MODULLER = [
    {"ad": "Proje iskeleti ve mimari", "hafta": 3, "durum": "hazir"},
    {"ad": "Veritabanı ve veri erişim katmanı", "hafta": 4, "durum": "planli"},
    {"ad": "Fotoğraf yükleme", "hafta": 5, "durum": "planli"},
    {"ad": "OCR / metin çıkarma", "hafta": 6, "durum": "planli"},
    {"ad": "Alan eşleme ve doğrulama", "hafta": 7, "durum": "planli"},
    {"ad": "Yapılandırılmış çıktı (JSON)", "hafta": 8, "durum": "planli"},
    {"ad": "Düzeltme arayüzü", "hafta": 9, "durum": "planli"},
    {"ad": "Dışa aktarma (Excel/CSV/JSON)", "hafta": 10, "durum": "planli"},
]


@main_bp.route("/")
def index():
    """
    Ana sayfa.
    render_template() -> templates klasöründeki HTML dosyasını doldurup döndürür.
    moduller=MODULLER -> HTML içinde {{ moduller }} olarak kullanılabilir.
    """
    return render_template("index.html", moduller=MODULLER)


@main_bp.route("/saglik")
def saglik():
    """
    Sağlık kontrolü (health check) adresi.
    Canlı sunucu (Render vb.) bu adrese istek atarak uygulamanın ayakta olup
    olmadığını kontrol eder. JSON döndürür, 200 = her şey yolunda.
    """
    return jsonify({"durum": "calisiyor", "uygulama": "Belgematik", "surum": "0.1.0"}), 200
