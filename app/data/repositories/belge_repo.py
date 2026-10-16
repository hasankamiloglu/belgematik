"""
belge_repo.py - belgeler tablosu için CRUD fonksiyonları.
"""


def ekle(conn, kullanici_id, dosya_adi, dosya_yolu, dosya_turu, boyut_kb):
    """
    Yeni belge kaydı ekler (durum otomatik 'yuklendi' olur -> DEFAULT).
    kullanici_id var olmayan bir kullanıcıysa YABANCI ANAHTAR kısıtı hata verir.
    """
    return conn.execute(
        """
        INSERT INTO belgeler (kullanici_id, dosya_adi, dosya_yolu, dosya_turu, boyut_kb)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
        """,
        (kullanici_id, dosya_adi, dosya_yolu, dosya_turu, boyut_kb),
    ).fetchone()


def getir(conn, belge_id):
    """id ile tek belge döndürür; yoksa None."""
    return conn.execute("SELECT * FROM belgeler WHERE id = %s", (belge_id,)).fetchone()


def kullaniciya_gore_listele(conn, kullanici_id, limit=20):
    """
    Bir kullanıcının belgelerini en yeniden eskiye listeler.
    Bu sorgu idx_belgeler_kullanici_tarih indeksini kullanır
    (WHERE kullanici_id + ORDER BY yuklenme_tarihi DESC).
    """
    return conn.execute(
        """
        SELECT id, dosya_adi, dosya_turu, boyut_kb, durum, yuklenme_tarihi
        FROM belgeler
        WHERE kullanici_id = %s
        ORDER BY yuklenme_tarihi DESC
        LIMIT %s
        """,
        (kullanici_id, limit),
    ).fetchall()


def durum_guncelle(conn, belge_id, yeni_durum):
    """
    Belgenin durumunu değiştirir ('yuklendi' -> 'islendi' / 'hatali').
    Listede olmayan bir durum yazılırsa CHECK kısıtı hata verir.
    """
    return conn.execute(
        "UPDATE belgeler SET durum = %s WHERE id = %s RETURNING *",
        (yeni_durum, belge_id),
    ).fetchone()


def sil(conn, belge_id):
    """Belgeyi siler (çıkarım kayıtları CASCADE ile silinir). True/False döndürür."""
    return conn.execute("DELETE FROM belgeler WHERE id = %s", (belge_id,)).rowcount == 1
