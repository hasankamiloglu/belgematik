"""
İŞ KATMANI (Business / Service Layer)

Görevi: Uygulamanın asıl işini yapmak. Sayfa göstermez, veritabanına SQL yazmaz.
Alt modüller (her biri ilgili haftada doldurulacak):
    ocr/         -> Fotoğraftan metin okuma (Tesseract veya yapay zekâ)   [Hafta 6]
    extraction/  -> Metinden alan bulma (tarih, vergi no, KDV, toplam)   [Hafta 7]
    validation/  -> Şema ve iş kuralı doğrulama (KDV + matrah = toplam?) [Hafta 7-8]
    export/      -> Excel / CSV / JSON çıktı üretme                      [Hafta 10]
"""
