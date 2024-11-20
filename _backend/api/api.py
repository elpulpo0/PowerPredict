from fastapi import APIRouter, HTTPException
from _backend.database.database import db
from loguru import logger

router = APIRouter()

logger.add(
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)


@router.get("/tables/", response_model=dict)
async def list_tables():
    """
    Obtenir la liste des tables disponibles dans la base de données.

    Returns:
        dict: Un dictionnaire contenant la liste des tables disponibles.
    """
    try:
        logger.info("Récupération des noms de tables.")
        tables = db.get_table_names()
        if not tables:
            logger.warning("Aucune table trouvée dans la base de données.")
        return {"tables": tables}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des noms de tables : {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la récupération des tables.")


@router.get("/tables/{table_name}/data/", response_model=dict)
async def get_table_data(table_name: str):
    """
    Récupérer les données d'une table spécifique.

    Args:
        table_name (str): Le nom de la table à récupérer.

    Returns:
        dict: Un dictionnaire contenant le nom de la table et ses données.

    Raises:
        HTTPException: Si la table n'existe pas ou si une erreur se produit.
    """
    try:
        logger.info(f"Récupération des données pour la table '{table_name}'.")
        data = db.fetch_table_data(table_name)
        if not data:
            logger.warning(f"Aucune donnée trouvée dans la table '{table_name}'.")
            raise HTTPException(status_code=404, detail=f"Aucune donnée trouvée dans la table '{table_name}'.")
        return {"table_name": table_name, "data": data}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données pour la table '{table_name}' : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur lors de la récupération des données pour '{table_name}'.")


@router.get("/health/", response_model=dict)
async def health_check():
    """
    Vérifier l'état de santé de l'API.

    Returns:
        dict: Un message indiquant que l'API fonctionne.
    """
    logger.info("Vérification de l'état de santé de l'API.")
    return {"status": "API en ligne et fonctionnelle."}
