# Veri Modeli (ER Tasarımı)

![ER diyagramı](er-diyagrami.png)

Kaynak dosya: `er-diyagrami.mmd` (Mermaid formatı, GitHub'da da görüntülenir)

## Varlıklar (tablolar)

| Tablo | Ne tutar? | Birincil anahtar (PK) | Yabancı anahtar (FK) |
|---|---|---|---|
| **kullanicilar** | Sisteme kayıtlı kişi (bireysel, KOBİ, muhasebeci) | id | – |
| **abonelikler** | Kullanıcının paketi ve kalan kredisi | id | kullanici_id (UNIQUE) |
| **belgeler** | Yüklenen fiş/fatura/kartvizit görüntüsü | id | kullanici_id |
| **semalar** | Belge türü şablonu (fiş, fatura, kartvizit) | id | kullanici_id (boş olabilir) |
| **sema_alanlari** | Bir şemadaki alanlar (toplam_tutar, kdv, vergi_no…) | id | sema_id |
| **cikarim_kayitlari** | Bir belgenin bir kez işlenmesi (OCR çalıştırması) | id | belge_id, sema_id |
| **cikarim_degerleri** | Çıkarılan her alanın değeri | id | cikarim_id, alan_id |

## İlişkiler

| İlişki | Tür | Açıklama |
|---|---|---|
| kullanicilar – abonelikler | **1-1** | Her kullanıcının tek bir aboneliği vardır. `abonelikler.kullanici_id` UNIQUE olduğu için ikinci kayıt eklenemez. |
| kullanicilar – belgeler | **1-N** | Bir kullanıcı çok belge yükler, her belge tek kullanıcıya aittir. |
| kullanicilar – semalar | **1-N (isteğe bağlı)** | Kullanıcı kendi şablonunu oluşturabilir. `kullanici_id` boşsa (NULL) şema sistemindir, herkes kullanır. |
| belgeler – cikarim_kayitlari | **1-N** | Aynı belge farklı motorla (Tesseract / yapay zekâ) tekrar işlenebilir. |
| semalar – sema_alanlari | **1-N** | Fiş şemasında; firma_adi, tarih, kdv, toplam_tutar gibi alanlar bulunur. |
| cikarim_kayitlari – sema_alanlari | **N-N** | Bir çıkarımda çok alan, bir alan çok çıkarımda bulunur. Ara tablo: **cikarim_degerleri**. |

## Neden bu tasarım? (Normalizasyon)

- **1NF:** Her hücrede tek değer var. Alanlar tek bir JSON sütununa yığılmadı; her alan değeri `cikarim_degerleri` tablosunda ayrı satır.
- **2NF:** Ara tablo `cikarim_degerleri` kendi `id`'sine sahip; değer bilgisi `(cikarim_id, alan_id)` ikilisinin tamamına bağlı.
- **3NF:** Alanın veri tipi, zorunluluğu gibi bilgiler değerlerin yanında tekrar edilmedi; sadece `sema_alanlari` tablosunda bir kez tutuluyor.

**İş açısından faydası:** Yeni bir belge türü (örneğin "gider pusulası") eklemek için kod değiştirmeye gerek yok.
`semalar` ve `sema_alanlari` tablolarına kayıt eklemek yeterli. Bu, ileride "şablon öğrenme" özelliğinin temelidir.
