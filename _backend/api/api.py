from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from database.database import db_clean, db_encoded
from .filters import APIFilters
from loguru import logger
from .api_config import VALID_COLUMNS_DATA, VALID_COLUMNS_TEST, VALID_COLUMNS_TRAIN, responses_data, responses_health, responses_home, responses_test_train

router = APIRouter()

@router.get(
    "/data",
    response_model=dict,
    tags=["Données PowerPredict"],
    responses=responses_data
)
async def get_clean_data_data(filters: APIFilters = Depends()):
    """
    Récupérer les données de la table clean_data avec des filtres optionnels.
    """
    try:
        logger.info("Récupération des données filtrées de clean_data.")

        filters = {col: value for col, value in locals().items() if value is not None and col in VALID_COLUMNS_DATA}

        data = db_clean.fetch_filtered_data(filters)
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
    include_in_schema=False
)
async def home():
    """
    ### Racine de l'API.
    Renvoie un message de bienvenue.
    """
    return {"message": "Bienvenue sur l'API PowerPredict, visite /docs pour l'exploiter"}

@router.get(
    "/test",
    response_model=dict,
    tags=["Données Encodées"],
    responses=responses_test_train
    )

async def get_test_data(filters: APIFilters = Depends()):
    """
    Récupérer les données encodées depuis la table 'test_data' avec des filtres optionnels.
    """
    try:
        logger.info("Récupération des données de test_data.")
        
        filters = {col: value for col, value in locals().items() if value is not None and col in VALID_COLUMNS_TEST}

        data = db_encoded.fetch_filtered_data("test_data", filters)
        if not data:
            logger.warning("Aucune donnée trouvée pour les critères fournis.")
            raise HTTPException(status_code=404, detail="Aucune donnée trouvée pour les critères fournis.")
        
        return {"table_name": "test_data", "filters": filters, "data": data}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données : {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la récupération des données.")
    
@router.get(
    "/train",
    response_model=dict,
    tags=["Données Encodées"],
    responses=responses_test_train
    )

async def get_train_data(filters: APIFilters = Depends()):
    """
    Récupérer les données encodées depuis la table 'train_data' avec des filtres optionnels.
    """
    try:
        logger.info("Récupération des données de train_data.")
        
        filters = {col: value for col, value in locals().items() if value is not None and col in VALID_COLUMNS_TRAIN}

        data = db_encoded.fetch_filtered_data("test_data", filters)
        if not data:
            logger.warning("Aucune donnée trouvée pour les critères fournis.")
            raise HTTPException(status_code=404, detail="Aucune donnée trouvée pour les critères fournis.")
        
        return {"table_name": "train_data", "filters": filters, "data": data}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données : {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la récupération des données.")

