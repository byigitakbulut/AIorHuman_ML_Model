import pytest
from unittest.mock import MagicMock, patch
import sys

# app.py'yi import etmeden ÖNCE joblib'i sahte hale getiriyoruz.
# Böylece .pkl dosyalarındaki sürüm hatası (ValueError) engellenir.
mock_joblib = MagicMock()
sys.modules['joblib'] = mock_joblib



from app import app

# SAHTE MODEL SINIFI (MOCK)
# Test senaryolarında kullanacağımız kontrollü model
class MockModel:
    def __init__(self, prediction_value, probability_value):
        self.prediction_value = prediction_value
        self.probability_value = probability_value

    def predict(self, data):
        return [self.prediction_value]

    def predict_proba(self, data):
        return [[1 - self.probability_value, self.probability_value]]

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# TEST 1: Ana Sayfa Kontrolü
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

# TEST 2: Boş Metin Gönderme
def test_predict_empty_input(client):
    response = client.post('/predict', data={'metin_kutusu': ''})
    assert response.status_code == 200
    

# TEST 3: "AI" (Yapay Zeka) Senaryosu
def test_predict_ai_detected(client, monkeypatch):
    # Tüm modellerin "AI" dediği bir senaryo hazırlıyoruz
    fake_ai_model = MockModel(prediction_value=1, probability_value=0.95)
    
    # app.models sözlüğünü sahte modellerle dolduruyoruz
    # Dictionary içindeki değerlerin her biri bizim MockModel'imiz olmalı
    sahte_modeller = {
        'Logistic Regression': fake_ai_model,
        'SVM': fake_ai_model,
        'Naive Bayes': fake_ai_model,
        'Random Forest': fake_ai_model
    }
    monkeypatch.setattr('app.models', sahte_modeller)

    response = client.post('/predict', data={'metin_kutusu': 'Test metni'})
    
    assert response.status_code == 200
    text_data = response.data.decode('utf-8')
    assert "AI (Yapay Zeka)" in text_data
    assert "red" in text_data

# TEST 4: "İNSAN" Senaryosu
def test_predict_human_detected(client, monkeypatch):
    # Tüm modellerin "İNSAN" dediği bir senaryo
    fake_human_model = MockModel(prediction_value=0, probability_value=0.10)
    
    sahte_modeller = {
        'Logistic Regression': fake_human_model,
        'SVM': fake_human_model,
        'Naive Bayes': fake_human_model,
        'Random Forest': fake_human_model
    }
    monkeypatch.setattr('app.models', sahte_modeller)

    response = client.post('/predict', data={'metin_kutusu': 'Test metni'})

    assert response.status_code == 200
    text_data = response.data.decode('utf-8')
    assert "İNSAN" in text_data
    assert "green" in text_data