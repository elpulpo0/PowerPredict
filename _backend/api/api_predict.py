from fastapi import APIRouter, HTTPException, Depends
from .filters import PredictionFilters
from .model import model
from loguru import logger
from .api_config import responses_predict

router = APIRouter()

@router.get(
    "/predict",
    response_model=dict,
    tags=["Prédiction"],
    responses=responses_predict
)
async def predict(filters: PredictionFilters = Depends()):
    """
    Prédire la consommation énergétique basée sur les données fournies et filtrées.
    """
    try:
        # Récupérer les coordonnées GPS de la localisation spécifiée dans le filtre
        latitude, longitude = model.get_coordinates(filters.location_name)
        
        # Vérification de la validité des coordonnées
        if latitude is None or longitude is None:
            raise HTTPException(status_code=400, detail="Localisation invalide.")

        # Préparer les données pour le modèle en utilisant les filtres
        input_data = {
            "surface_declaree": filters.surface_declaree,
            "latitude": latitude,
            "longitude": longitude,
            "vecteur_energie": filters.vecteur_energie if filters.vecteur_energie else "Électricité",
            "annee_consommation": filters.annee_consommation if filters.annee_consommation else "2020",
        }

        # Faire une prédiction
        prediction_result = model.predict(input_data)

        # Extraire les informations de la prédiction
        best_model = prediction_result.get("best_model")
        best_prediction = prediction_result.get("best_prediction")

        # Vérifier si la prédiction est None et lui attribuer une valeur par défaut
        if best_prediction is None:
            best_prediction = 0.0  # Valeur par défaut si la prédiction est None

        # Loguer les données utilisées pour la prédiction
        logger.info(
            f"Prédiction réalisée avec les données : "
            f"surface_declaree: {filters.surface_declaree}, "
            f"latitude: {latitude}, longitude: {longitude}, "
            f"vecteur_energie: {filters.vecteur_energie}, "
            f"annee_consommation: {filters.annee_consommation}"
        )

        # Loguer les résultats de la prédiction
        logger.info(f"Résultat du modèle : {best_model}, Prédiction : {best_prediction:.2f} kWh")

        # Retourner les résultats au format attendu
        return {
            "Modèle utilisé": best_model,
            "Prédiction (kWh)": f"{best_prediction:,.2f}"
        }

    except HTTPException as e:
        # Gestion des erreurs avec un retour HTTP approprié
        logger.error(f"Erreur dans la prédiction: {e.detail}")
        raise e

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur.")
