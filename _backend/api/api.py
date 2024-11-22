from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database.database import db
from loguru import logger
from .api_config import VALID_COLUMNS, responses_data, responses_health, responses_home

router = APIRouter()

@router.get(
    "/data",
    response_model=dict,
    tags=["Données PowerPredict"],
    responses=responses_data
)
async def get_clean_data_data(
    annee_consommation: Optional[int] = Query(None, description="Filtrer par année de consommation"),
    zone_climatique: Optional[str] = Query(None, description="Filtrer par zone climatique"),
    code_region: Optional[str] = Query(None, description="Filtrer par code région"),
    code_departement: Optional[str] = Query(None, description="Filtrer par code département"),
    nom_commune: Optional[str] = Query(None, description="Filtrer par nom de commune"),
):
    """
    Récupérer les données de la table clean_data avec des filtres optionnels.
    """
    try:
        logger.info("Récupération des données filtrées de clean_data.")

        filters = {col: value for col, value in locals().items() if value is not None and col in VALID_COLUMNS}

        data = db.fetch_filtered_data(filters)
        if not data:
            logger.warning("Aucune donnée trouvée pour les critères fournis.")
            raise HTTPException(status_code=404, detail="Aucune donnée trouvée pour les critères fournis.")
        
        return {"table_name": "clean_data", "filters": filters, "data": data}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données : {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la récupération des données.")
    
@router.get(
    "/health",
    response_model=dict,
    tags=["Santé API"],
    responses=responses_health
)
async def health_check():
    """
    ### Vérifier l'état de santé de l'API
    Renvoie un message indiquant que l'API est fonctionnelle.
    """
    logger.info("Vérification de l'état de santé de l'API.")
    return {"status": "API en ligne et fonctionnelle."}

@router.get(
    "/",
    response_model=dict,
    tags=["Home"],
    responses=responses_home
)
async def home():
    """
    ### Racine de l'API.
    Renvoie un message de bienvenue.
    """
    return {"message": "Bienvenue sur l'API PowerPredict, visite /docs pour l'exploiter"}
