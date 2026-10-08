"""
test_app.py - İskeletin çalıştığını kontrol eden otomatik testler.

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


def test_ana_sayfa_aciliyor(client):
    """Ana sayfa 200 (başarılı) döndürmeli ve ürün adını içermeli."""
    cevap = client.get("/")
    assert cevap.status_code == 200
    assert "Belgematik".encode() in cevap.data


def test_saglik_kontrolu(client):
    """/saglik adresi JSON ile 'calisiyor' döndürmeli."""
    cevap = client.get("/saglik")
    assert cevap.status_code == 200
    assert cevap.get_json()["durum"] == "calisiyor"
