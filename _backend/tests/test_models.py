import pytest
import os
import joblib
import pandas as pd
import numpy as np

# Définir le chemin absolu vers le dossier des modèles
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

@pytest.fixture
def models_and_features():
    """Fixture pour charger les modèles et les colonnes sauvegardées."""
    # Chemins des fichiers
    rf_model_path = os.path.join(MODELS_DIR, "random_forest_model.pkl")
    gb_model_path = os.path.join(MODELS_DIR, "gradient_boosting_model.pkl")
    all_features_path = os.path.join(MODELS_DIR, "all_features.pkl")

    # Vérifier l'existence des fichiers
    assert os.path.exists(rf_model_path), f"Fichier non trouvé : {rf_model_path}"
    assert os.path.exists(gb_model_path), f"Fichier non trouvé : {gb_model_path}"
    assert os.path.exists(all_features_path), f"Fichier non trouvé : {all_features_path}"

    # Charger les modèles et les colonnes
    rf_model = joblib.load(rf_model_path)
    gb_model = joblib.load(gb_model_path)
    all_features = joblib.load(all_features_path)

    return rf_model, gb_model, all_features

# Test 1 : Vérification du chargement des modèles
def test_model_loading(models_and_features):
    """Test pour vérifier que les modèles et les features sont correctement chargés."""
    rf_model, gb_model, all_features = models_and_features

    assert rf_model is not None, "Random Forest model non chargé correctement."
    assert gb_model is not None, "Gradient Boosting model non chargé correctement."
    assert isinstance(all_features, list), "Les features doivent être une liste."

# Test 2 : Vérification de l'alignement des colonnes
def test_feature_alignment(models_and_features):
    """Test pour vérifier que les colonnes des données correspondent aux features."""
    _, _, all_features = models_and_features

    # Exemple d'entrée fictive
    input_data = {
        "surface_declaree": 100,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "vecteur_energie": "Electricite",
        "annee_consommation": 2020,
    }

    # Ajouter les colonnes manquantes
    for feature in all_features:
        if feature not in input_data:
            input_data[feature] = 0  # Valeur par défaut

    # Convertir en DataFrame et réordonner
    input_data_df = pd.DataFrame([input_data])
    input_data_df = input_data_df.reindex(columns=all_features)

    assert all(input_data_df.columns == all_features), "Les colonnes ne correspondent pas aux features attendues."

# Test 3 : Vérification des prédictions des modèles
def test_model_predictions(models_and_features):
    """Test pour vérifier que les modèles génèrent des prédictions valides."""
    rf_model, gb_model, all_features = models_and_features

    # Exemple d'entrée fictive
    input_data = {
        "surface_declaree": 150,
        "latitude": 45.764,
        "longitude": 4.8357,
        "vecteur_energie": "Electricite",
        "annee_consommation": 2021,
    }

    # Ajouter les colonnes manquantes
    for feature in all_features:
        if feature not in input_data:
            input_data[feature] = 0  # Valeur par défaut

    # Convertir en DataFrame et réordonner
    input_data_df = pd.DataFrame([input_data])
    input_data_df = input_data_df.reindex(columns=all_features)

    # Prédictions
    rf_prediction = rf_model.predict(input_data_df)
    gb_prediction = gb_model.predict(input_data_df)

    # Vérifications
    assert isinstance(rf_prediction, np.ndarray), "La prédiction de Random Forest doit être un tableau numpy."
    assert isinstance(gb_prediction, np.ndarray), "La prédiction de Gradient Boosting doit être un tableau numpy."
    assert len(rf_prediction) == 1, "La prédiction de Random Forest doit avoir une seule valeur."
    assert len(gb_prediction) == 1, "La prédiction de Gradient Boosting doit avoir une seule valeur."

# Test 4 : Vérification des valeurs des prédictions
def test_prediction_values(models_and_features):
    """Test pour vérifier que les prédictions sont logiques (ex. positives)."""
    rf_model, gb_model, all_features = models_and_features

    # Exemple d'entrée fictive
    input_data = {
        "surface_declaree": 200,
        "latitude": 43.2965,
        "longitude": 5.3698,
        "vecteur_energie": "Gaz",
        "annee_consommation": 2019,
    }

    # Ajouter les colonnes manquantes
    for feature in all_features:
        if feature not in input_data:
            input_data[feature] = 0  # Valeur par défaut

    # Convertir en DataFrame et réordonner
    input_data_df = pd.DataFrame([input_data])
    input_data_df = input_data_df.reindex(columns=all_features)

    # Prédictions
    rf_prediction = rf_model.predict(input_data_df)
    gb_prediction = gb_model.predict(input_data_df)

    # Vérifications
    assert rf_prediction[0] >= 0, "La prédiction de Random Forest doit être positive."
    assert gb_prediction[0] >= 0, "La prédiction de Gradient Boosting doit être positive."