from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from api.database import db

from App import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")  
    assert response.status_code == 200
    assert response.json() == {"status": "API en ligne et fonctionnelle."}

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
        "annee_consommation": "2020",
        "surface_declaree": 205643,
        "nombre_declaration": 4,
        "consommation_declaree": 38442621,
        "densite_energetique": 186.938631511892,
        "latitude": 16.2679458,
        "longitude": -61.5870766,
        "consommation_log": 17.464677349937865,
        "consommation_etat": "Normale",
        "nom_commune": "TOULOUSE",
        "nom_departement": "Guadeloupe",
        "nom_region": "Guadeloupe",
        "vecteur_energie": "electricite",
        "zone_climatique": "H1a"
    }])

    response = client.get("/data", params=filters)

    assert response.status_code == 200
    data = response.json()

    # Compare the filters but exclude 'nombre_declaration' from the comparison
    filters_without_nombre_declaration = {key: value for key, value in filters.items() if key != 'nombre_declaration'}
    assert data["filters"] == filters_without_nombre_declaration  # Compare without 'nombre_declaration'
    
    assert data["table_name"] == "consommation"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0

    # Additional assertions
    assert data["data"][0]["nombre_declaration"] == 4
    assert data["data"][0]["nom_commune"] == "TOULOUSE"
    assert data["data"][0]["zone_climatique"] == "H1a"
