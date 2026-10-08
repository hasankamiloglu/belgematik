"""
OCR modülü (Optical Character Recognition = Optik Karakter Tanıma).

Plan: İki motor olacak ve ikisi de AYNI arayüzü (fonksiyon imzasını) kullanacak.
    TesseractMotoru -> ücretsiz, internetsiz çalışır (ücretsiz paket)
    YapayZekaMotoru -> görsel destekli LLM API'si, daha doğru (ücretli paket)
Böylece motor değiştirmek için kodun geri kalanına dokunmak gerekmez
(Strateji tasarım deseni / Strategy pattern).
"""
