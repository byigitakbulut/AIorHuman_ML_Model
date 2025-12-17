import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from webAPI import fetch_general_cc_by_data


# 1. Başarılı Veri Çekme Senaryosu
@patch('webAPI.requests.get')
def test_fetch_success(mock_get):
    # API'den dönecek sahte cevabı ayarla
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'response': {
            'docs': [
                {'abstract': ['Bu bir test özetidir. Yeterince uzun olması gerek.'], 'title_display': 'Test Başlık'},
                {'abstract': ['Kısa'], 'title_display': 'Elenen Başlık'}  # Bu elenmeli (<50 karakter)
            ]
        }
    }
    mock_get.return_value = mock_response

    # Fonksiyonu çalıştır
    df = fetch_general_cc_by_data(rows=10)

    # Kontroller
    assert not df.empty
    assert len(df) == 1  # Biri elendi, biri kaldı
    assert df.iloc[0]['title'] == 'Test Başlık'
    assert df.iloc[0]['source_license'] == 'CC-BY (PLOS)'


# 2. API Hatası Senaryosu (Örn: 404 veya 500)
@patch('webAPI.requests.get')
def test_fetch_api_error(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500  # Sunucu hatası
    mock_get.return_value = mock_response

    df = fetch_general_cc_by_data()

    assert df.empty


# 3. Bağlantı Hatası Senaryosu (Exception)
@patch('webAPI.requests.get')
def test_fetch_connection_error(mock_get):
    # İstek atıldığında hata fırlat
    mock_get.side_effect = Exception("Bağlantı koptu")

    df = fetch_general_cc_by_data()

    assert df.empty