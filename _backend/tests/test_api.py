from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from database.database import db

from App import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")  
    assert response.status_code == 200
    assert response.json() == {"status":"API en ligne et fonctionnelle."}

def test_home_endpoint():
    response = client.get("/")  
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API PowerPredict, visite /docs pour l'exploiter"}

def test_data_endpoint():
    filters = {
        "annee_consommation": "2020",
        "nombre_declaration": 4,
        "vecteur_energie": "electricite",
        "nom_commune": "toulouse"
    }

    # Mocking the db call to return dummy data
    db.fetch_filtered_data = MagicMock(return_value=[{
        "surface_declaree": 2112,
        "nombre_declaration": 4,
        "consommation_declaree": 181828,
        "nom_commune": "TOULOUSE",
        "nom_departement": "Haute-Garonne",
        "nom_region": "Occitanie",
        "vecteur_energie": "Electricite",
        "zone_climatique": "H1a"
    }])

    response = client.get("/data", params=filters)

    assert response.status_code == 200
    data = response.json()

    assert data["table_name"] == "consommation"
    assert data["filters"] == filters
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0

    assert data["data"][0]["nombre_declaration"] == 4
    assert data["data"][0]["nom_commune"] == "TOULOUSE"
    assert data["data"][0]["zone_climatique"] == "H1a"
