"""
test_app.py - Backend API'nin çalıştığını kontrol eden otomatik testler.

Çalıştırmak için:  pytest
"""

import pytest

from app import create_app


@pytest.fixture
def client():
    """
    fixture -> her testten önce çalışan hazırlık fonksiyonu.
    "testing" ayarıyla uygulama oluşturup sahte bir tarayıcı (test client) verir.
    """
    app = create_app("testing")
    return app.test_client()


def test_saglik_kontrolu(client):
    """/api/saglik adresi JSON ile 'calisiyor' döndürmeli."""
    cevap = client.get("/api/saglik")
    assert cevap.status_code == 200
    assert cevap.get_json()["durum"] == "calisiyor"


def test_moduller_listesi(client):
    """/api/moduller bir liste döndürmeli ve Hafta 3 modülü 'hazir' olmalı."""
    cevap = client.get("/api/moduller")
    assert cevap.status_code == 200
    veri = cevap.get_json()
    assert isinstance(veri, list)
    assert veri[0]["hafta"] == 3
    assert veri[0]["durum"] == "hazir"


def test_cors_izinli_adres(client):
    """React'in adresinden (5173) gelen isteğe CORS izni verilmeli."""
    cevap = client.get("/api/saglik", headers={"Origin": "http://localhost:5173"})
    assert cevap.headers["Access-Control-Allow-Origin"] == "http://localhost:5173"


def test_cors_izinsiz_adres(client):
    """Tanımadığımız bir siteden gelen isteğe CORS izni VERİLMEMELİ."""
    cevap = client.get("/api/saglik", headers={"Origin": "http://kotu-site.com"})
    assert "Access-Control-Allow-Origin" not in cevap.headers
