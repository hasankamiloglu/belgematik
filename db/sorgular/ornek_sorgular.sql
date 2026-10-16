-- =====================================================================
-- ÖRNEK SORGULAR  (pgAdmin > Query Tool içinde tek tek çalıştırılabilir)
-- =====================================================================
-- Bu sorgular hem hocaya "şema ve örnek veriyle çalışan sorgular" olarak
-- gösterilir, hem de manage.py demo komutu tarafından çalıştırılır.


-- 1) Kullanıcılar ve paketleri (1-1 ilişki: kullanicilar JOIN abonelikler)
SELECT k.ad_soyad, k.rol, a.paket, a.kalan_kredi, a.aylik_kredi
FROM kullanicilar k
JOIN abonelikler a ON a.kullanici_id = k.id
ORDER BY k.id;


-- 2) Her kullanıcının kaç belgesi var? (1-N ilişki + GROUP BY)
--    LEFT JOIN -> belgesi olmayan kullanıcı da listede 0 ile görünür
SELECT k.ad_soyad, COUNT(b.id) AS belge_sayisi
FROM kullanicilar k
LEFT JOIN belgeler b ON b.kullanici_id = k.id
GROUP BY k.id, k.ad_soyad
ORDER BY belge_sayisi DESC;


-- 3) Bir belgeden çıkarılan tüm alanlar (N-N ilişki: ara tablo üzerinden)
SELECT b.dosya_adi, sa.alan_adi, cd.deger, cd.gecerli_mi, cd.duzeltildi_mi
FROM cikarim_degerleri cd
JOIN cikarim_kayitlari ck ON ck.id = cd.cikarim_id
JOIN belgeler b           ON b.id  = ck.belge_id
JOIN sema_alanlari sa     ON sa.id = cd.alan_id
WHERE b.dosya_adi = 'market_fisi_001.jpg'
ORDER BY sa.id;


-- 4) Doğrulamaya takılan (geçersiz) alanlar -> düzeltme ekranında gösterilecek
SELECT b.dosya_adi, sa.alan_adi, cd.deger, sa.dogrulama_kurali
FROM cikarim_degerleri cd
JOIN sema_alanlari sa     ON sa.id = cd.alan_id
JOIN cikarim_kayitlari ck ON ck.id = cd.cikarim_id
JOIN belgeler b           ON b.id  = ck.belge_id
WHERE cd.gecerli_mi = false;


-- 5) Doğrulama bekleyen işler (kısmi indeks idx_cikarim_kayitlari_bekleyen kullanılır)
SELECT ck.id, b.dosya_adi, ck.guven_skoru, ck.olusturma_tarihi
FROM cikarim_kayitlari ck
JOIN belgeler b ON b.id = ck.belge_id
WHERE ck.durum = 'bekliyor'
ORDER BY ck.olusturma_tarihi;


-- 6) İndeksin kullanıldığını görmek için: EXPLAIN sorgunun NASIL çalışacağını gösterir.
--    (Az veride PostgreSQL tam taramayı da seçebilir, veri büyüdükçe indeksi kullanır.)
EXPLAIN
SELECT * FROM belgeler WHERE kullanici_id = 1 ORDER BY yuklenme_tarihi DESC;
