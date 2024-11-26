from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from database.database import db
from .filters import APIFilters
from loguru import logger
from .api_config import responses_data, responses_health

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
