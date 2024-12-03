import pandas as pd
import numpy as np
import joblib
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from loguru import logger
from typing import Tuple, Dict, Any

class Model:
    def __init__(self, rf_model_path: str, gb_model_path: str, features_path: str):
        # Charger les modèles et les colonnes sauvegardées
        self.rf_model = joblib.load(rf_model_path)
        self.gb_model = joblib.load(gb_model_path)
        self.all_features = joblib.load(features_path)

        if not isinstance(self.all_features, list):
            self.all_features = list(self.all_features)

        # Initialiser le géocodeur
        self.geolocator = Nominatim(user_agent="geoapi")

    def get_coordinates(self, location_name: str) -> Tuple[Any, Any]:
        """
        Récupère les coordonnées GPS pour un lieu donné.

        Args:
            location_name (str): Nom du lieu.

        Returns:
            Tuple[float, float]: Latitude et longitude.
        """
        try:
            location = self.geolocator.geocode(location_name, country_codes="FR")
            if location:
                return location.latitude, location.longitude
            else:
                logger.warning("Localisation introuvable pour: {}", location_name)
                return None, None
        except GeocoderTimedOut:
            logger.error("Le géocodeur a expiré pour: {}", location_name)
            return None, None

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fait une prédiction à partir des données fournies.

        Args:
            input_data (dict): Données d'entrée pour la prédiction.

        Returns:
            dict: Résultats de la prédiction.
        """
        try:
            # Ajouter les colonnes manquantes avec des valeurs par défaut
            for feature in self.all_features:
                if feature not in input_data:
                    input_data[feature] = 0

            # Convertir en DataFrame et aligner les colonnes
            input_data_df = pd.DataFrame([input_data])
            input_data_df = input_data_df.reindex(columns=self.all_features)

            # Vérification des colonnes
            if not all(input_data_df.columns == self.all_features):
                logger.error("Les colonnes des données d'entrée ne correspondent pas aux caractéristiques du modèle.")
                raise ValueError("Erreur dans la préparation des données.")

            # Prédictions
            rf_prediction = self.rf_model.predict(input_data_df)
            gb_prediction = self.gb_model.predict(input_data_df)

            # Reconversion des prédictions
            rf_prediction_original = np.expm1(rf_prediction)[0]
            gb_prediction_original = np.expm1(gb_prediction)[0]

            # Comparer les performances des modèles
            rf_validation_score = 0.07  # MAE moyen pour Random Forest
            gb_validation_score = 0.05  # MAE moyen pour Gradient Boosting

            if gb_validation_score < rf_validation_score:
                best_model = "Gradient Boosting"
                best_prediction = gb_prediction_original
            else:
                best_model = "Forêt Aléatoire"
                best_prediction = rf_prediction_original

            # Retourner les résultats
            return {
            "best_model": best_model,
            "best_prediction": best_prediction
            }

        except Exception as e:
            logger.error("Erreur lors de la prédiction : {}", e)
            raise

# Instanciation de la classe `Model`
model = Model(
    rf_model_path="models/random_forest_model.pkl",
    gb_model_path="models/gradient_boosting_model.pkl",
    features_path="models/all_features.pkl"
)
