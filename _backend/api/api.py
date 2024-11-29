from fastapi import APIRouter, HTTPException, Depends
from database.database import db
from .filters import APIFilters
import numpy as np
import joblib
from loguru import logger
from .api_config import responses_data, responses_health, PredictionData

router = APIRouter()

@router.get(
    "/data",
    response_model=dict,
    tags=["Données PowerPredict"],
    responses=responses_data
)
async def get_data(filters: APIFilters = Depends()):
    """
    Récupérer les données de consommation avec filtres optionnels.
    """
    try:
        query_filters = {
            key.lower(): value.lower() if isinstance(value, str) else value
            for key, value in filters.dict(exclude_none=True).items()
        }

        data = db.fetch_filtered_data(query_filters)

        if not data:
            logger.warning("Aucune donnée trouvée pour les critères fournis.")
            raise HTTPException(status_code=404, detail="Aucune donnée trouvée pour les critères fournis.")
    
        logger.info(f"PowerPredict db called with filters: {query_filters}")
        return {"table_name": "consommation", "filters": query_filters, "data": data}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données : {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur.")


@router.get(
    "/health",
    response_model=dict,
    tags=["Santé API"],
    responses=responses_health
)
async def health_check():
    """
    Vérifie que l'API fonctionne correctement.
    """
    logger.info("Vérification de l'état de santé de l'API.")
    return {"status": "API en ligne et fonctionnelle."}

@router.get(
    "/",
    include_in_schema=False
)
async def home():
    """
    Racine de l'API.
    """
    return {"message": "Bienvenue sur l'API PowerPredict, visite /docs pour l'exploiter"}

# @router.post("/predict/")
# async def predict(data: PredictionData):
#     """
#     Faire une prédiction des consommations à partir des modèles Random Forest et Gradient Boosting.
#     """
#     try:
#         # Convertir les données en array (format attendu pour les modèles)
#         input_data = np.array([[data.surface_declaree, data.nombre_declaration,
#                                 data.annee_consommation, data.zone_climatique, data.vecteur_energie]])

#         # Prédictions avec les deux modèles
#         rf_prediction = rf_model.predict(input_data)
#         gb_prediction = gb_model.predict(input_data)

#         # Si le modèle prédit sur une échelle logarithmique, inverser la transformation log
#         rf_prediction_original = np.expm1(rf_prediction)  # Si la prédiction est log-transformée
#         gb_prediction_original = np.expm1(gb_prediction)

#         return {
#             "Random Forest Prediction": rf_prediction_original[0],
#             "Gradient Boosting Prediction": gb_prediction_original[0]
#         }

#     except Exception as e:
#         logger.error(f"Erreur lors de la prédiction : {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur lors de la prédiction.")


# from pydantic import BaseModel
# import pandas as pd

# # Charger le modèle
# rf_model = joblib.load("database/random_forest_model.pkl")

# # Données d'entrée
# class PredictionData(BaseModel):
#     surface_declaree: float
#     nombre_declaration: int
#     annee_consommation: int
#     zone_climatique: str
#     vecteur_energie: str

# # Fonction pour sélectionner les features
# def select_features(data, selected_features):
#     """
#     Sélectionne un sous-ensemble de features dans les données.
#     """
#     # Créer une liste contenant les valeurs des features, et non pas une liste de listes.
#     # Le tableau doit être de forme (1, N) où N est le nombre de features sélectionnées
#     return pd.DataFrame([list(data[feature] for feature in selected_features)], columns=selected_features)

# # Route de prédiction
# @router.post("/predict/")
# async def predict(data: PredictionData):
#     try:
#         # Liste des features à sélectionner pour la prédiction
#         selected_features = ['surface_declaree', 'nombre_declaration', 'zone_climatique', 'vecteur_energie']

#         # Convertir les données en un dictionnaire et sélectionner les features
#         input_data = select_features(data.dict(), selected_features)

#         # Faire la prédiction
#         prediction = rf_model.predict(input_data)

#         # Retourner la prédiction
#         return {"Prediction": prediction[0]}

#     except Exception as e:
#         # Loguer l'erreur avec Loguru
#         logger.error(f"Erreur lors de la prédiction : {e}")
        
#         # Retourner l'erreur à l'utilisateur avec le détail
#         raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {e}")

