from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from api.model import model
from api.api_predict import router
from App import app

client = TestClient(app)

def mock_get_coordinates(location_name):
    if location_name == "abcdef":
        return (None, None)  # Simulate invalid coordinates for "abcdef"
    return (48.8566, 2.3522)  # Valid coordinates for Paris

# Mock the model's get_coordinates function
model.get_coordinates = MagicMock(side_effect=mock_get_coordinates)

# Mocking the model's prediction function
def mock_predict(input_data):
    return {
        "best_model": "Gradient Boosting",
        "best_prediction": 7265166.68
    }

# Remplacer la fonction predict du modèle par le mock
model.predict = MagicMock(side_effect=mock_predict)

def test_predict_endpoint():
    filters = {
        "surface_declaree": 200.0,
        "location_name": "Paris",
        "vecteur_energie": "electricite",
        "annee_consommation": "2020"
    }

    # Faire la requête à l'endpoint de prédiction
    response = client.get("/predict", params=filters)

    assert response.status_code == 200  # Vérifier que la réponse est OK
    data = response.json()

    # Vérifier que les résultats sont ceux du mock
    assert data["Modèle utilisé"] == "Gradient Boosting"
    assert data["Prédiction (kWh)"] == "7,265,166.68"  # Vérifier la prédiction formatée

def test_predict_invalid_location():
    # Tester avec une localisation invalide
    filters = {
        "surface_declaree": 150.0,
        "location_name": "abcdef",
        "vecteur_energie": "electricite",
        "annee_consommation": "2020"
    }

    response = client.get("/predict", params=filters)

    assert response.status_code == 400  # Erreur attendue pour une localisation invalide
    assert response.json() == {"detail": "Localisation invalide."}  # Vérifier que l'erreur correspond

def test_predict_missing_parameters():
    # Tester avec des paramètres manquants
    filters = {
        "surface_declaree": 150.0,
        "location_name": "Paris"  # Manque 'vecteur_energie' et 'annee_consommation'
    }

    response = client.get("/predict", params=filters)

    assert response.status_code == 200  # Vérifier que la réponse est OK malgré les paramètres manquants
    data = response.json()

    # Vérifier que la prédiction utilise les valeurs par défaut
    assert data["Modèle utilisé"] == "Gradient Boosting"
    assert data["Prédiction (kWh)"] == "7,265,166.68"
