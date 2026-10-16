"""
VERİ KATMANI (Data Layer)

Görevi: Veritabanı ile konuşan TEK katman.
    db.py          -> PostgreSQL bağlantısı
    migrate.py     -> Migration aracı (db/migrations/*.sql dosyalarını sırayla uygular)
    models.py      -> Tablolardaki izinli değerler (CHECK kısıtlarının Python karşılığı)
    repositories/  -> CRUD fonksiyonları (ekle, oku, güncelle, sil)

Tablo tasarımı için: docs/veri-modeli.md, docs/veritabani.md ve docs/er-diyagrami.png
"""
