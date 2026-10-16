-- =====================================================================
-- MIGRATION 001: Tabloların oluşturulması
-- =====================================================================
-- Bu dosya DDL (Data Definition Language / Veri Tanımlama Dili) içerir:
-- CREATE TABLE -> tablo oluşturur, kolonları ve KISITLARI tanımlar.
--
-- Kısıt (constraint) türleri:
--   PRIMARY KEY  -> Birincil anahtar: her satırı benzersiz tanımlar, boş olamaz.
--   REFERENCES   -> Yabancı anahtar (FOREIGN KEY): başka tablodaki bir satıra bağlar.
--                   Var olmayan bir kullanıcıya belge eklenemez (referans bütünlüğü).
--   NOT NULL     -> Bu kolon boş bırakılamaz.
--   UNIQUE       -> Bu değer tabloda iki kez geçemez (ör. aynı e-posta).
--   CHECK        -> Değer bir kurala uymalı (ör. rol sadece 3 değerden biri olabilir).
--   DEFAULT      -> Değer verilmezse kullanılacak varsayılan değer.
--
-- ON DELETE CASCADE  -> Üst kayıt silinince bağlı alt kayıtlar da silinir.
-- ON DELETE RESTRICT -> Bağlı alt kayıt varken üst kayıt SİLİNEMEZ.
--
-- Bu dosyayı elle çalıştırmayın: "python manage.py migrate" komutu çalıştırır.
-- =====================================================================


-- ---------------------------------------------------------------------
-- 1) KULLANICILAR: Sisteme kayıtlı kişiler
-- ---------------------------------------------------------------------
CREATE TABLE kullanicilar (
    -- GENERATED ALWAYS AS IDENTITY -> id'yi veritabanı otomatik verir (1, 2, 3...)
    id               INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ad_soyad         VARCHAR(100) NOT NULL,
    -- UNIQUE: aynı e-posta ile iki hesap açılamaz
    email            VARCHAR(255) NOT NULL UNIQUE,
    -- Şifrenin kendisi DEĞİL, şifrelenmiş (hash) hali saklanır
    sifre_hash       VARCHAR(255) NOT NULL,
    rol              VARCHAR(20)  NOT NULL DEFAULT 'bireysel'
                     CHECK (rol IN ('bireysel', 'kobi', 'muhasebeci')),
    -- TIMESTAMPTZ -> saat dilimi bilgisiyle tarih-saat; now() -> şu an
    olusturma_tarihi TIMESTAMPTZ  NOT NULL DEFAULT now()
);


-- ---------------------------------------------------------------------
-- 2) ABONELİKLER: Kullanıcının paketi ve kalan kredisi  (1-1 ilişki)
-- ---------------------------------------------------------------------
CREATE TABLE abonelikler (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- REFERENCES + UNIQUE birlikte = 1-1 ilişki:
    --   REFERENCES -> abonelik mutlaka var olan bir kullanıcıya ait olmalı
    --   UNIQUE     -> bir kullanıcının İKİNCİ aboneliği olamaz
    kullanici_id INTEGER NOT NULL UNIQUE
                 REFERENCES kullanicilar(id) ON DELETE CASCADE,
    paket        VARCHAR(20) NOT NULL DEFAULT 'ucretsiz'
                 CHECK (paket IN ('ucretsiz', 'pro')),
    aylik_kredi  INTEGER NOT NULL CHECK (aylik_kredi >= 0),
    kalan_kredi  INTEGER NOT NULL,
    baslangic    DATE    NOT NULL DEFAULT CURRENT_DATE,
    bitis        DATE,
    -- Kalan kredi eksiye düşemez ve aylık krediden fazla olamaz
    CONSTRAINT chk_kalan_kredi CHECK (kalan_kredi BETWEEN 0 AND aylik_kredi),
    -- Bitiş tarihi (varsa) başlangıçtan önce olamaz
    CONSTRAINT chk_tarih_sirasi CHECK (bitis IS NULL OR bitis >= baslangic)
);


-- ---------------------------------------------------------------------
-- 3) BELGELER: Yüklenen fiş / fatura / kartvizit görüntüleri  (1-N ilişki)
-- ---------------------------------------------------------------------
CREATE TABLE belgeler (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- Bir kullanıcının ÇOK belgesi olabilir (UNIQUE yok) -> 1-N ilişki
    kullanici_id    INTEGER NOT NULL
                    REFERENCES kullanicilar(id) ON DELETE CASCADE,
    dosya_adi       VARCHAR(255) NOT NULL,
    dosya_yolu      VARCHAR(500) NOT NULL,
    dosya_turu      VARCHAR(10)  NOT NULL
                    CHECK (dosya_turu IN ('png', 'jpg', 'jpeg', 'pdf')),
    -- 0'dan büyük, en fazla 10 MB (10240 KB) -> config.py'deki sınırla aynı
    boyut_kb        INTEGER NOT NULL CHECK (boyut_kb > 0 AND boyut_kb <= 10240),
    durum           VARCHAR(20) NOT NULL DEFAULT 'yuklendi'
                    CHECK (durum IN ('yuklendi', 'islendi', 'hatali')),
    yuklenme_tarihi TIMESTAMPTZ NOT NULL DEFAULT now()
);


-- ---------------------------------------------------------------------
-- 4) ŞEMALAR: Belge türü şablonları (fiş, fatura, kartvizit...)
-- ---------------------------------------------------------------------
CREATE TABLE semalar (
    id               INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- NULL olabilir: kullanici_id boşsa bu bir SİSTEM şemasıdır (herkes kullanır)
    kullanici_id     INTEGER REFERENCES kullanicilar(id) ON DELETE CASCADE,
    ad               VARCHAR(50) NOT NULL,
    aciklama         TEXT,
    sistem_semasi_mi BOOLEAN NOT NULL DEFAULT false,
    -- Tutarlılık kuralı: sistem şemasının sahibi olmaz, kullanıcı şemasının sahibi olur
    CONSTRAINT chk_sema_sahibi CHECK (
        (sistem_semasi_mi AND kullanici_id IS NULL)
        OR (NOT sistem_semasi_mi AND kullanici_id IS NOT NULL)
    ),
    -- Aynı sahip aynı isimde iki şema oluşturamaz.
    -- NULLS NOT DISTINCT -> iki sistem şeması (ikisi de NULL) da aynı adı alamaz.
    CONSTRAINT uq_sema_adi UNIQUE NULLS NOT DISTINCT (kullanici_id, ad)
);


-- ---------------------------------------------------------------------
-- 5) ŞEMA ALANLARI: Bir şemadaki alanlar (toplam_tutar, kdv_tutari...)
-- ---------------------------------------------------------------------
CREATE TABLE sema_alanlari (
    id               INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sema_id          INTEGER NOT NULL REFERENCES semalar(id) ON DELETE CASCADE,
    alan_adi         VARCHAR(50) NOT NULL,
    veri_tipi        VARCHAR(10) NOT NULL
                     CHECK (veri_tipi IN ('metin', 'tarih', 'para', 'sayi')),
    zorunlu_mu       BOOLEAN NOT NULL DEFAULT false,
    -- Değeri kontrol etmek için düzenli ifade (regex). Örn. vergi no: ^[0-9]{10}$
    dogrulama_kurali VARCHAR(255),
    -- Bir şemada aynı alan adı iki kez olamaz
    CONSTRAINT uq_sema_alan UNIQUE (sema_id, alan_adi)
);


-- ---------------------------------------------------------------------
-- 6) ÇIKARIM KAYITLARI: Bir belgenin bir kez işlenmesi (OCR çalıştırması)
-- ---------------------------------------------------------------------
CREATE TABLE cikarim_kayitlari (
    id               INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    belge_id         INTEGER NOT NULL REFERENCES belgeler(id) ON DELETE CASCADE,
    -- RESTRICT: kullanımda olan bir şema silinemez (geçmiş kayıtlar bozulmasın)
    sema_id          INTEGER NOT NULL REFERENCES semalar(id) ON DELETE RESTRICT,
    ocr_motoru       VARCHAR(20) NOT NULL
                     CHECK (ocr_motoru IN ('tesseract', 'yapay_zeka')),
    ham_metin        TEXT,
    -- NUMERIC(4,3) -> 0.000 ile 9.999 arası; CHECK ile 0-1 aralığına sınırlıyoruz
    guven_skoru      NUMERIC(4,3) CHECK (guven_skoru BETWEEN 0 AND 1),
    durum            VARCHAR(20) NOT NULL DEFAULT 'bekliyor'
                     CHECK (durum IN ('bekliyor', 'dogrulandi', 'duzeltildi')),
    olusturma_tarihi TIMESTAMPTZ NOT NULL DEFAULT now()
);


-- ---------------------------------------------------------------------
-- 7) ÇIKARIM DEĞERLERİ: N-N ilişkinin ARA TABLOSU
--    Bir çıkarımda çok alan var, bir alan çok çıkarımda kullanılıyor.
--    Bu tablo ikisini birbirine bağlar ve "değer" bilgisini de taşır.
-- ---------------------------------------------------------------------
CREATE TABLE cikarim_degerleri (
    id            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cikarim_id    INTEGER NOT NULL REFERENCES cikarim_kayitlari(id) ON DELETE CASCADE,
    alan_id       INTEGER NOT NULL REFERENCES sema_alanlari(id) ON DELETE RESTRICT,
    deger         TEXT,
    guven_skoru   NUMERIC(4,3) CHECK (guven_skoru BETWEEN 0 AND 1),
    gecerli_mi    BOOLEAN NOT NULL DEFAULT true,
    duzeltildi_mi BOOLEAN NOT NULL DEFAULT false,
    -- Bir çıkarımda aynı alan iki kez olamaz (ör. iki tane "toplam_tutar")
    CONSTRAINT uq_cikarim_alan UNIQUE (cikarim_id, alan_id)
);
