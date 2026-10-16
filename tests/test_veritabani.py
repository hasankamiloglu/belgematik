"""
test_veritabani.py - Veritabanı şeması ve CRUD fonksiyonlarının testleri.

Bu testler GERÇEK PostgreSQL veritabanına bağlanır. Çalışması için:
    1) .env içinde DATABASE_URL doğru olmalı
    2) "python manage.py migrate" ile tablolar oluşturulmuş olmalı
Veritabanına ulaşılamazsa testler hata vermez, ATLANIR (skipped).

Testlerin eklediği kayıtlar "test_" ile başlayan e-postalar kullanır ve
her testten sonra silinir; örnek veriye dokunulmaz.
"""

import pytest

# psycopg kurulu değilse bu dosyadaki tüm testleri atla
psycopg = pytest.importorskip("psycopg")
from psycopg import errors  # noqa: E402

from app.data.db import baglanti  # noqa: E402
from app.data.repositories import belge_repo, cikarim_repo, kullanici_repo  # noqa: E402


@pytest.fixture
def conn():
    """
    Her test için veritabanı bağlantısı açar.
    yield'den sonraki kısım test BİTTİKTEN sonra çalışır (temizlik):
    test kullanıcılarını siler, CASCADE sayesinde bağlı her şey de silinir.
    """
    try:
        c = baglanti()
        c.execute("SELECT 1 FROM kullanicilar LIMIT 1")
    except Exception as hata:  # bağlantı yok veya tablolar oluşturulmamış
        pytest.skip(f"Veritabanına ulaşılamadı: {hata}")
    yield c
    c.execute("DELETE FROM kullanicilar WHERE email LIKE 'test\\_%%@ornek.test'")
    c.close()


def _test_kullanicisi(conn, ek="1", rol="bireysel"):
    """Testlerde tekrar tekrar kullanılan yardımcı: test kullanıcısı ekler."""
    return kullanici_repo.ekle(conn, "Test Kisi", f"test_{ek}@ornek.test", "hash", rol)


# --------------------------------------------------------------- CRUD testleri
def test_kullanici_crud(conn):
    """Ekle -> oku -> güncelle -> sil zinciri çalışmalı."""
    k = _test_kullanicisi(conn)
    assert k["id"] is not None

    assert kullanici_repo.getir(conn, k["id"])["email"] == "test_1@ornek.test"

    guncel = kullanici_repo.guncelle(conn, k["id"], rol="kobi")
    assert guncel["rol"] == "kobi"
    assert guncel["ad_soyad"] == "Test Kisi"  # verilmeyen alan değişmemeli

    assert kullanici_repo.sil(conn, k["id"]) is True
    assert kullanici_repo.getir(conn, k["id"]) is None


def test_belge_ekle_ve_listele(conn):
    k = _test_kullanicisi(conn)
    belge_repo.ekle(conn, k["id"], "a.jpg", "uploads/a.jpg", "jpg", 100)
    belge_repo.ekle(conn, k["id"], "b.pdf", "uploads/b.pdf", "pdf", 200)
    assert len(belge_repo.kullaniciya_gore_listele(conn, k["id"])) == 2


# ------------------------------------------------------------ Kısıt testleri
def test_ayni_email_ikinci_kez_eklenemez(conn):
    """UNIQUE kısıtı: aynı e-posta ile ikinci kayıt reddedilmeli."""
    _test_kullanicisi(conn)
    with pytest.raises(errors.UniqueViolation):
        _test_kullanicisi(conn)


def test_gecersiz_rol_reddedilir(conn):
    """CHECK kısıtı: rol sadece bireysel / kobi / muhasebeci olabilir."""
    with pytest.raises(errors.CheckViolation):
        _test_kullanicisi(conn, rol="admin")


def test_olmayan_kullaniciya_belge_eklenemez(conn):
    """YABANCI ANAHTAR kısıtı: var olmayan kullanıcıya belge bağlanamaz."""
    with pytest.raises(errors.ForeignKeyViolation):
        belge_repo.ekle(conn, 999999, "x.jpg", "uploads/x.jpg", "jpg", 10)


def test_10mb_ustu_belge_reddedilir(conn):
    """CHECK kısıtı: boyut 0 ile 10240 KB arasında olmalı."""
    k = _test_kullanicisi(conn)
    with pytest.raises(errors.CheckViolation):
        belge_repo.ekle(conn, k["id"], "dev.pdf", "uploads/dev.pdf", "pdf", 50000)


def test_kullanici_silinince_belgeleri_de_silinir(conn):
    """ON DELETE CASCADE: kullanıcı silinince belgeleri de silinmeli."""
    k = _test_kullanicisi(conn)
    b = belge_repo.ekle(conn, k["id"], "a.jpg", "uploads/a.jpg", "jpg", 100)
    kullanici_repo.sil(conn, k["id"])
    assert belge_repo.getir(conn, b["id"]) is None


def test_kredi_eksiye_dusemez(conn):
    """CHECK kısıtı: kalan kredi 0'ın altına inemez."""
    k = kullanici_repo.abonelikli_ekle(conn, "Test Kisi", "test_kredi@ornek.test", "hash")
    with pytest.raises(errors.CheckViolation):
        kullanici_repo.kredi_dus(conn, k["id"], miktar=1000)


# ------------------------------------------------------- Transaction testleri
def test_abonelik_hata_verirse_kullanici_da_geri_alinir(conn):
    """
    abonelikli_ekle() iki INSERT'i tek transaction'da yapar.
    Aboneliği bilerek HATALI yapıyoruz (eksi kredi). Kullanıcı da kaydedilmemeli.
    """
    eski = kullanici_repo.UCRETSIZ_AYLIK_KREDI
    kullanici_repo.UCRETSIZ_AYLIK_KREDI = -5  # CHECK (aylik_kredi >= 0) kısıtını bozar
    try:
        with pytest.raises(errors.CheckViolation):
            kullanici_repo.abonelikli_ekle(conn, "Test Kisi", "test_tx@ornek.test", "hash")
    finally:
        kullanici_repo.UCRETSIZ_AYLIK_KREDI = eski

    assert kullanici_repo.email_ile_getir(conn, "test_tx@ornek.test") is None


def test_cikarim_hatali_alan_varsa_hicbir_sey_kaydedilmez(conn):
    """Şemada olmayan bir alan gönderilirse çıkarım kaydı da oluşmamalı."""
    k = _test_kullanicisi(conn)
    b = belge_repo.ekle(conn, k["id"], "a.jpg", "uploads/a.jpg", "jpg", 100)
    with pytest.raises(ValueError):
        cikarim_repo.kaydet(
            conn, b["id"], "fis", "tesseract", "metin", 0.9,
            {"toplam_tutar": "10.00", "olmayan_alan": "x"},
        )
    sayi = conn.execute(
        "SELECT count(*) AS n FROM cikarim_kayitlari WHERE belge_id = %s", (b["id"],)
    ).fetchone()
    assert sayi["n"] == 0


def test_deger_duzeltme(conn):
    """Düzeltilen değer kaydedilmeli ve duzeltildi_mi işaretlenmeli."""
    k = _test_kullanicisi(conn)
    b = belge_repo.ekle(conn, k["id"], "a.jpg", "uploads/a.jpg", "jpg", 100)
    c = cikarim_repo.kaydet(conn, b["id"], "fis", "tesseract", "m", 0.9, {"toplam_tutar": "10.00"})
    duzelen = cikarim_repo.deger_duzelt(conn, c["id"], "toplam_tutar", "12.00")
    assert duzelen["deger"] == "12.00"
    assert duzelen["duzeltildi_mi"] is True
