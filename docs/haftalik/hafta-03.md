# Hafta 3 – Kurulum, Mimari ve Veri Modeli

**Geliştirilen modül:** Proje iskeleti ve depo yapısı

## Yapılan teknik çalışmalar

- [x] Teknoloji yığını seçildi: Python, Flask, PostgreSQL, Tesseract OCR, Git/GitHub. Kurulanlar: Python 3.14, VS Code, Git, Flask. PostgreSQL ve Tesseract Hafta 4'te kurulacak.
- [x] Boş proje iskeleti ve **3 katmanlı** klasör yapısı oluşturuldu (sunum / iş / veri)
- [x] Application Factory deseni ile çalışan Flask uygulaması (`run.py`, `app/__init__.py`)
- [x] Ortama göre ayar yönetimi (`config.py`: development / testing / production)
- [x] Gizli bilgiler `.env` dosyasına ayrıldı, örneği `.env.example`
- [x] `.gitignore` hazırlandı (.env, venv, __pycache__, uploads hariç tutuldu)
- [x] README taslağı yazıldı
- [x] ER diyagramı: kullanıcı, belge görüntüsü, çıkarım kaydı, şema (+ abonelik, şema alanı, çıkarım değeri)
- [x] Mimari şema çizildi
- [x] İskeletin çalıştığını gösteren 2 otomatik test yazıldı (`tests/test_app.py`)
- [x] GitHub deposu oluşturuldu ve ilk commit gönderildi

## Teslim edilen çıktılar

| Çıktı | Konum |
|---|---|
| GitHub deposu (README + .gitignore) | github.com/hasankamiloglu/belgematik-backend |
| ER diyagramı | `docs/er-diyagrami.png`, `docs/er-diyagrami.mmd` |
| Veri modeli açıklaması | `docs/veri-modeli.md` |
| Mimari şema | `docs/mimari-sema.png` |

## Gösterilecek ilerleme (demo sırası)

1. GitHub deposunu aç → README, diyagramlar, düzenli klasör yapısı
2. VS Code’da klasör yapısını göster → `api`, `services`, `data`
3. `python run.py` → http://127.0.0.1:5000 ana sayfa
4. http://127.0.0.1:5000/saglik → `{"durum": "calisiyor"}`
5. `pytest` → `2 passed`
6. ER diyagramını açıp ilişkileri anlat (1-1, 1-N, N-N)

## Yapay zekâ kullanımı

Yapay zekâ; katmanlı mimari ile alternatif desenleri (MVC, tek dosya) karşılaştırmak ve ER diyagramı
için varlık önerisi almak amacıyla kullanıldı. Nihai kararlar (abonelik tablosunun eklenmesi,
şema alanlarının ayrı tabloya alınması, N-N için ara tablo) öğrenci tarafından gerekçelendirildi.

## Öğrencinin kendi geliştirdiği bölümler

- Projeye özgü varlıklar: `semalar` + `sema_alanlari` ile kod değiştirmeden yeni belge türü ekleyebilme
- `abonelikler` tablosu: ücretsiz / pro paket ayrımı (iş modelinin veri tarafı)
- Klasör/katman yapısının gerekçesi: her katman yalnızca altındakiyle konuşur

## Ek: Hoca geri bildirimi – Frontend ve backend ayrı depolar

Hocanın isteği üzerine proje iki ayrı depoya bölündü:

| Depo | Teknoloji | Görev |
|---|---|---|
| `belgematik-backend` | Python + Flask | JSON döndüren API, iş kuralları, veritabanı |
| `belgematik-frontend` | React + Vite | Kullanıcı arayüzü; veriyi API'den `fetch` ile alır |

Yapılan değişiklikler:
- [x] Eski depo `belgematik` → `belgematik-backend` olarak yeniden adlandırıldı (commit geçmişi korundu)
- [x] Backend'deki HTML şablonları kaldırıldı; sunum katmanı `app/presentation/` → `app/api/` oldu
- [x] API uçları: `GET /api/`, `GET /api/saglik`, `GET /api/moduller`
- [x] CORS eklendi: sadece izin verilen frontend adresleri (`localhost:5173`) API'ye erişebilir
- [x] Testler 4'e çıkarıldı (sağlık, modüller, izinli CORS, izinsiz CORS)
- [x] `belgematik-frontend` deposu oluşturuldu: React bileşenleri, API istemcisi (`api/client.js`)
- [x] Mimari şema iki depolu yapıya göre güncellendi
