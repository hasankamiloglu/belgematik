-- =====================================================================
-- MIGRATION 002: İndeksler
-- =====================================================================
-- İndeks nedir? Kitabın arkasındaki "dizin" gibi. Bir kolonda arama yaparken
-- veritabanı tüm tabloyu satır satır okumak yerine indeksten doğrudan bulur.
--
-- Bedeli: Her INSERT/UPDATE'te indeks de güncellenir ve diskte yer kaplar.
-- Bu yüzden HER kolona indeks eklenmez; sadece SIK ARANAN kolonlara eklenir.
--
-- ÖNEMLİ: PostgreSQL, PRIMARY KEY ve UNIQUE kısıtları için indeksi KENDİSİ
-- oluşturur. Ama yabancı anahtarlara (REFERENCES) otomatik indeks EKLEMEZ.
-- =====================================================================


-- ✅ EKLENDİ: "Bir kullanıcının belgelerini en yeniden eskiye listele"
--    uygulamanın en sık yapacağı sorgu. İki kolonlu (bileşik) indeks hem
--    kullanici_id ile filtrelemeyi hem de tarihe göre sıralamayı hızlandırır.
--    Ayrıca kullanıcı silinirken CASCADE için bağlı belgeleri hızlı bulur.
CREATE INDEX idx_belgeler_kullanici_tarih
    ON belgeler (kullanici_id, yuklenme_tarihi DESC);

-- ✅ EKLENDİ: "Bu belgenin çıkarım kayıtları" sorgusu ve belge silinirken
--    CASCADE için. belge_id bir yabancı anahtar; otomatik indeksi yok.
CREATE INDEX idx_cikarim_kayitlari_belge
    ON cikarim_kayitlari (belge_id);

-- ✅ EKLENDİ (KISMİ İNDEKS): Sadece 'bekliyor' durumundaki kayıtları içerir.
--    "Doğrulama bekleyen işler" listesi çok sık sorgulanacak, ama kayıtların
--    çoğu zamanla 'dogrulandi' olacak. Sadece ihtiyacımız olan satırları
--    indeksleyerek indeks küçük ve hızlı kalır.
CREATE INDEX idx_cikarim_kayitlari_bekleyen
    ON cikarim_kayitlari (olusturma_tarihi)
    WHERE durum = 'bekliyor';

-- ✅ EKLENDİ: Bir şema silinmek istendiğinde (RESTRICT kontrolü) ve
--    "bu şemayla yapılan çıkarımlar" raporunda kullanılır.
CREATE INDEX idx_cikarim_kayitlari_sema
    ON cikarim_kayitlari (sema_id);

-- ✅ EKLENDİ: alan_id yabancı anahtar; sema alanı silinmek istendiğinde
--    RESTRICT kontrolü bu kolonda arama yapar.
CREATE INDEX idx_cikarim_degerleri_alan
    ON cikarim_degerleri (alan_id);


-- ❌ EKLENMEDİ (ve nedeni):
--  - kullanicilar(email)        -> UNIQUE kısıtı zaten indeks oluşturdu.
--  - abonelikler(kullanici_id)  -> UNIQUE kısıtı zaten indeks oluşturdu.
--  - sema_alanlari(sema_id)     -> UNIQUE (sema_id, alan_adi) indeksinin ilk
--                                  kolonu sema_id; o indeks bu aramada da kullanılır.
--  - cikarim_degerleri(cikarim_id) -> UNIQUE (cikarim_id, alan_id) için aynı durum.
--  - belgeler(dosya_turu)       -> Sadece 4 farklı değer alıyor (düşük seçicilik).
--                                  İndeks tablonun çeyreğini döndürür; tam tarama
--                                  zaten daha hızlıdır, indeks gereksiz yük olur.
