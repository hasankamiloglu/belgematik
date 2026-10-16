"""
migrate.py - Basit MIGRATION aracı.

MIGRATION nedir?
    Veritabanı şemasındaki her değişikliğin (tablo ekleme, kolon ekleme, indeks...)
    numaralı bir SQL dosyası olarak saklanmasıdır:
        db/migrations/001_tablolari_olustur.sql
        db/migrations/002_indeksleri_olustur.sql
        db/migrations/003_...   (ileride eklenecekler)

NEDEN kullanılır?
    1) Şemanın TARİHÇESİ Git'te tutulur: kim, ne zaman, neyi değiştirdi görülür.
    2) Başka bir bilgisayarda (ya da canlı sunucuda) tek komutla AYNI şema kurulur.
    3) Her dosya SADECE BİR KEZ çalışır. Hangilerinin çalıştığı veritabanındaki
       "schema_migrations" tablosunda tutulur, böylece tablo iki kez oluşturulmaya
       çalışılmaz.

Çalıştırmak için:  python manage.py migrate
"""

from pathlib import Path

# Migration dosyalarının bulunduğu klasör: proje_kökü/db/migrations
MIGRATION_KLASORU = Path(__file__).resolve().parents[2] / "db" / "migrations"


def _takip_tablosunu_olustur(conn):
    """Hangi migration'ların uygulandığını tutan tabloyu (yoksa) oluşturur."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            surum            VARCHAR(255) PRIMARY KEY,   -- dosya adı, ör. 001_tablolari_olustur.sql
            uygulanma_tarihi TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )


def uygulananlar(conn):
    """Daha önce uygulanmış migration dosyalarının adlarını küme (set) olarak döndürür."""
    _takip_tablosunu_olustur(conn)
    satirlar = conn.execute("SELECT surum FROM schema_migrations").fetchall()
    return {satir["surum"] for satir in satirlar}


def migrate(conn, klasor=MIGRATION_KLASORU):
    """
    Henüz uygulanmamış migration dosyalarını SIRAYLA çalıştırır.

    sorted() -> dosyalar ada göre sıralanır; 001, 002, 003... sırası bu yüzden önemli.
    Döndürür: bu çalıştırmada uygulanan dosya adlarının listesi.
    """
    yapilmis = uygulananlar(conn)
    yeni_uygulananlar = []

    for dosya in sorted(klasor.glob("*.sql")):
        if dosya.name in yapilmis:
            continue  # bu dosya daha önce çalışmış, atla

        sql = dosya.read_text(encoding="utf-8")

        # TRANSACTION (İŞLEM): Dosyadaki komutlar ve takip kaydı "ya hep ya hiç" çalışır.
        # Dosyanın ortasında hata olursa her şey geri alınır (ROLLBACK);
        # veritabanı yarım kalmış bir şemayla bırakılmaz.
        with conn.transaction():
            conn.execute(sql)
            conn.execute("INSERT INTO schema_migrations (surum) VALUES (%s)", (dosya.name,))

        yeni_uygulananlar.append(dosya.name)

    return yeni_uygulananlar
