# Belgematik – Backend (API)

**Fiş, fatura ve kartvizit fotoğraflarından yapılandırılmış veri (JSON / tablo) çıkaran uygulamanın backend'i.**

KOBİ'ler ve muhasebeciler her ay yüzlerce belgeyi elle sisteme giriyor. Bu hem yorucu hem de hataya açık.
Belgematik belgenin fotoğrafını alır, OCR ve yapay zekâ ile alanları (firma, vergi no, tarih, KDV, toplam…)
çıkarır, kurallarla doğrular ve sonucu Excel / CSV / JSON olarak verir.

> Proje iki ayrı depodan oluşur:
> - **belgematik-backend** (bu depo): Python + Flask API, iş kuralları, veritabanı
> - **[belgematik-frontend](https://github.com/hasankamiloglu/belgematik-frontend)**: React arayüzü
>
> Durum: **v0.2 – Proje iskeleti (Hafta 3)**. Modüller haftalık olarak eklenmektedir.

## API uçları

| Yöntem | Adres | Açıklama |
|---|---|---|
| GET | `/api/` | API hakkında bilgi |
| GET | `/api/saglik` | Sağlık kontrolü (sunucu ayakta mı?) |
| GET | `/api/moduller` | Modüllerin geliştirme durumu |

## Özellikler (yol haritası)

| Modül | Açıklama | Durum |
|---|---|---|
| Proje iskeleti | Katmanlı mimari, API, CORS, testler | ✅ Hafta 3 |
| Veritabanı | PostgreSQL tabloları ve CRUD | ⏳ Hafta 4 |
| Fotoğraf yükleme | PNG / JPG / PDF yükleme ve ön işleme | ⏳ |
| OCR | Tesseract (ücretsiz) + Yapay zekâ (pro) | ⏳ |
| Alan eşleme ve doğrulama | Şema ve iş kuralı kontrolü | ⏳ |
| Düzeltme | Hatalı alanları düzeltme API'si | ⏳ |
| Dışa aktarma | Excel, CSV, JSON | ⏳ |

## Teknolojiler

Python · Flask · PostgreSQL · Tesseract OCR · Görsel destekli LLM API · Pydantic · pytest · Git/GitHub

## Mimari

![Mimari şema](docs/mimari-sema.png)

Backend **3 katmanlı mimari** ile geliştirilmektedir:

```
app/
├── api/            # 1) SUNUM katmanı : API uçları, JSON cevaplar
├── services/       # 2) İŞ katmanı    : OCR, alan eşleme, doğrulama, dışa aktarma
│   ├── ocr/
│   ├── extraction/
│   ├── validation/
│   └── export/
└── data/           # 3) VERİ katmanı  : Veritabanı modelleri ve veri erişimi
    ├── models.py
    └── repositories/
```

## Veri modeli (ER diyagramı)

![ER diyagramı](docs/er-diyagrami.png)

Tabloların ve ilişkilerin açıklaması: [docs/veri-modeli.md](docs/veri-modeli.md)

## Kurulum (Windows)

```powershell
git clone https://github.com/hasankamiloglu/belgematik-backend.git
cd belgematik-backend
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Kontrol: http://127.0.0.1:5000/api/saglik

Testleri çalıştırmak için: `pytest`

Ekranları görmek için frontend'i de çalıştırın: [belgematik-frontend](https://github.com/hasankamiloglu/belgematik-frontend)

## Klasör yapısı

```
belgematik-backend/
├── app/               # Uygulama kodu (3 katman)
├── tests/             # Otomatik testler
├── uploads/           # Yüklenen belgeler (Git'e gitmez)
├── docs/              # Diyagramlar, kurulum ve haftalık raporlar
├── config.py          # Ortam ayarları (geliştirme / test / canlı) ve CORS
├── run.py             # API'yi başlatan dosya
├── requirements.txt   # Python kütüphaneleri
├── .env.example       # Örnek gizli ayar dosyası
└── .gitignore         # Git'e gönderilmeyecek dosyalar
```

## Lisans

Bu proje Bilgisayar Uygulamaları I dersi kapsamında geliştirilmektedir.
