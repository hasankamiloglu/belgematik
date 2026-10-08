# GitHub Deposu Oluşturma ve Yükleme

## 1. Hesap aç
1. https://github.com adresinde **Sign up** ile hesap açın.
2. Kullanıcı adını profesyonel seçin (örn. `adsoyad`); ileride CV'nizde bu görünecek.
3. Öğrenciyseniz https://education.github.com/pack adresinden okul e-postanızla **Student Developer Pack** başvurusu yapın (ücretsiz araçlar).

## 2. GitHub'da boş depo oluştur
1. Sağ üstteki **+** → **New repository**
2. Repository name: `belgematik`
3. Description: `Fiş, fatura ve kartvizit fotoğraflarından yapılandırılmış veri çıkaran web uygulaması`
4. **Public** seçin (hoca erişebilsin).
5. "Add a README", ".gitignore", "license" seçeneklerini **İŞARETLEMEYİN** (bizde zaten var).
6. **Create repository**

## 3. Projeyi yükle (VS Code terminalinde, proje klasöründe)

```powershell
git init                                  # klasörü Git deposu yap
git branch -M main                        # ana dal adını "main" yap
git add .                                 # tüm dosyaları hazırla (.gitignore'dakiler hariç)
git status                                # KONTROL: .env ve venv listede OLMAMALI!
git commit -m "Hafta 3: proje iskeleti, katmanli mimari, ER diyagrami"
git remote add origin https://github.com/hasankamiloglu/belgematik.git
git push -u origin main
```

İlk `push`ta tarayıcı açılıp GitHub girişi isteyecek; giriş yapın ve izin verin.

## 4. Kontrol
- github.com/hasankamiloglu/belgematik sayfasında README ve diyagramlar görünmeli.
- `.env` dosyası **görünmemeli**.

## Her hafta sonu
```powershell
git add .
git commit -m "Hafta X: yapilan isin kisa ozeti"
git push
```
Düzenli commit geçmişi, hocaya işi haftalara yayarak yaptığınızı gösterir.
