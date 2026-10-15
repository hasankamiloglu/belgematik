# Windows Kurulum Rehberi

Sırayla yapın. Her programı kurduktan sonra açık olan terminalleri kapatıp yeniden açın.

## 1. Python 3.12
1. https://www.python.org/downloads/ adresinden **Python 3.12.x** Windows installer'ı indirin.
2. Kurulumun ilk ekranında **"Add python.exe to PATH"** kutusunu MUTLAKA işaretleyin.
3. "Install Now" deyin.
4. Kontrol (PowerShell): `python --version` → `Python 3.12.x` yazmalı.

## 2. VS Code
1. https://code.visualstudio.com/ adresinden indirip kurun ("Add to PATH" ve "Open with Code" kutularını işaretleyin).
2. Sol menüdeki Eklentiler (Extensions) bölümünden kurun:
   - **Python** (Microsoft)
   - **Pylance** (Microsoft)
   - **Markdown Preview Mermaid Support** (README'deki diyagramlar için, isteğe bağlı)

## 3. Git
1. https://git-scm.com/download/win adresinden indirip varsayılan ayarlarla kurun.
2. Kontrol: `git --version`
3. Kimliğinizi tanıtın (GitHub'da kullanacağınız ad ve e-posta):
   ```powershell
   git config --global user.name "Adınız Soyadınız"
   git config --global user.email "eposta@ornek.com"
   ```

## 4. Tesseract OCR (Hafta 6'da kullanılacak, şimdiden kurun)
1. GitHub'da "UB-Mannheim/tesseract" sayfasından Windows installer'ı (.exe) indirin.
2. Kurulumda **"Additional language data"** altından **Turkish** dilini işaretleyin.
3. Kurulum yolu varsayılan: `C:\Program Files\Tesseract-OCR`
4. Bu klasörü Windows PATH'e ekleyin (Başlat → "ortam değişkenleri" → Path → Yeni).
5. Kontrol: `tesseract --version` ve `tesseract --list-langs` (listede `tur` olmalı).

## 5. PostgreSQL (Hafta 4'te kullanılacak, şimdiden kurun)
1. https://www.postgresql.org/download/windows/ adresinden installer'ı indirin.
2. Kurulumda **pgAdmin 4** seçili kalsın.
3. `postgres` kullanıcısı için bir şifre belirleyin ve **NOT ALIN**. Port: `5432`.
4. Kurulumdan sonra pgAdmin'i açıp şifreyle bağlanabildiğinizi kontrol edin.

## 6. Projeyi çalıştırma
1. Zip'i örneğin `C:\Users\<ad>\Desktop\projeler\belgematik-backend` klasörüne çıkarın.
2. VS Code → File → Open Folder → `belgematik-backend` klasörünü açın.
3. VS Code içinde terminal açın (Ctrl + ö  veya  Terminal → New Terminal) ve sırayla:

```powershell
py -m venv venv                  # sanal ortam oluştur (projeye özel Python)
venv\Scripts\activate            # sanal ortamı aktif et; satır başında (venv) görünmeli
pip install -r requirements.txt  # kütüphaneleri kur
copy .env.example .env           # gizli ayar dosyasını oluştur
python run.py                    # uygulamayı başlat
```

4. Tarayıcıda açın: http://127.0.0.1:5000/api/saglik (ekranlar için frontend ayrıca `npm run dev` ile çalıştırılır)
5. Durdurmak için terminalde **Ctrl + C**.
6. Testler: `pytest` → `2 passed` yazmalı.

### Sık karşılaşılan hata
`venv\Scripts\activate` komutu **"running scripts is disabled"** hatası verirse, bir kez şunu çalıştırın:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Sonra "Y" deyip tekrar `venv\Scripts\activate` yazın.

VS Code sağ altta Python yorumlayıcısı sorarsa `.\venv\Scripts\python.exe` seçin.

## 7. Node.js ve frontend (React)
1. https://nodejs.org adresinden **LTS** sürümünü indirip varsayılan ayarlarla kurun.
2. Kontrol: `node --version` ve `npm --version`
3. Frontend deposunun README'sindeki adımları izleyin: `npm install` → `npm run dev` → http://localhost:5173
