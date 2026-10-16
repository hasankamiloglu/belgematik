# Hafta 4 – Veritabanı Tasarımı ve Veri Erişim Katmanı

**Geliştirilen modül:** Veritabanı ve veri erişim katmanı

## Yapılan teknik çalışmalar

- [x] PostgreSQL 18 kuruldu, `belgematik` veritabanı oluşturuldu
- [x] Tablolar **migration** ile oluşturuldu: `db/migrations/001_tablolari_olustur.sql` (7 tablo)
- [x] İlişkiler ve kısıtlar: PRIMARY KEY, FOREIGN KEY (CASCADE / RESTRICT), UNIQUE, NOT NULL, CHECK, DEFAULT
- [x] İndeksler: `002_indeksleri_olustur.sql` (5 indeks, 1'i kısmi indeks) ve eklenmeyenlerin gerekçesi
- [x] Migration aracı: `app/data/migrate.py` (`schema_migrations` tablosu ile takip, transaction içinde uygulama)
- [x] Sentetik örnek veri: `db/seed/ornek_veri.sql` (KVKK uyumlu, gerçek kişisel veri yok)
- [x] Temel CRUD fonksiyonları: `app/data/repositories/` (kullanıcı, belge, çıkarım)
- [x] Transaction kullanımı: kullanıcı + abonelik ve çıkarım + değerler "ya hep ya hiç" kaydediliyor
- [x] SQL injection'a karşı parametreli sorgular (`%s`)
- [x] Yönetim komutları: `python manage.py migrate | seed | sorgular | demo`
- [x] 11 veritabanı testi (CRUD, kısıt ihlalleri, CASCADE, transaction geri alma)

## Teslim edilen çıktılar

| Çıktı | Konum |
|---|---|
| Veritabanı şeması / scriptleri | `db/migrations/*.sql` |
| Örnek veriyle dolu veritabanı | `db/seed/ornek_veri.sql` + `python manage.py seed` |
| CRUD veri erişim kodu | `app/data/repositories/*.py`, `app/data/db.py`, `app/data/migrate.py` |
| Açıklama dokümanı | `docs/veritabani.md` |

## Gösterilecek ilerleme (demo sırası)

1. pgAdmin → `belgematik` → Schemas → Tables: 7 tablo + `schema_migrations`
2. `python manage.py sorgular` → JOIN'li sorgular ve EXPLAIN (indeks kullanımı)
3. `python manage.py demo` → CREATE / READ / UPDATE / DELETE adım adım
4. `pytest` → 15 test geçiyor (kısıt ihlalleri ve transaction geri alma dahil)
5. pgAdmin'de bir kısıt ihlali denemesi: `INSERT INTO kullanicilar (ad_soyad,email,sifre_hash,rol) VALUES ('x','y@ornek.test','h','admin');` → CHECK hatası

## Kontrol kriterleri

| Kriter | Kanıt |
|---|---|
| İlişki ve kısıtlar çalışıyor | `tests/test_veritabani.py` kısıt testleri |
| CRUD işlemleri sorunsuz | `python manage.py demo`, `test_kullanici_crud` |
| Sentetik veri KVKK'ya uygun | `@ornek.test`, "(Örnek)" firmalar, sahte hash'ler |

## Yapay zekâ kullanımı

Yapay zekâ; indeks önerisi almak (hangi kolonlar sık sorgulanır), migration yaklaşımlarını
(Alembic vs. saf SQL) karşılaştırmak ve SQL sorgularını gözden geçirmek için kullanıldı.
Kısmi indeks ve `dosya_turu` kolonuna indeks eklenmemesi kararları gerekçelendirildi.

## Öğrencinin kendi geliştirdiği bölümler

- Şema, Hafta 3'teki ER modeline birebir uygun kuruldu
- Elle açıklanan ilişki/kısıtlar: `docs/veritabani.md` (1-1 abonelik, N-N ara tablo, kredi CHECK'i, RESTRICT)
