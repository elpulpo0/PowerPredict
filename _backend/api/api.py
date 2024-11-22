from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database.database import db
from loguru import logger

router = APIRouter()

VALID_COLUMNS = [
    "annee_consommation",
    "zone_climatique",
    "code_region",
    "code_departement",
    "nom_commune",
    "nombre_declaration",
    "surface_declaree",
    "consommation_declaree",
    "vecteur_energie",
]

@router.get(
    "/data",
    response_model=dict,
    tags=["Données PowerPredict"],
    responses={
        200: {
            "description": "Données récupérées avec succès.",
            "content": {
                "application/json": {
                    "example": {
                        "table_name": "clean_data",
                        "filters": {
                            "annee_consommation": 2020,
                            "zone_climatique": "GUA",
                            "nom_commune": "BAILLIF"
                        },
                        "data": [
                            {
                                "annee_consommation": "2020",
                                "zone_climatique": "GUA",
                                "code_region": "01",
                                "code_departement": "971",
                                "nom_commune": "BAILLIF",
                                "nombre_declaration": 6,
                                "surface_declaree": 7746,
                                "consommation_declaree": 1085220,
                                "vecteur_energie": "Electricite"
                            }
                        ],
                    }
                }
            },
        },
        404: {
            "description": "Aucune donnée trouvée pour les critères fournis.",
            "content": {
                "application/json": {
                    "example": {"detail": "Aucune donnée trouvée pour les critères fournis."}
                }
            },
        },
        422: {
            "description": "Unprocessable Entity - La requête ne peut être traitée.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "int_parsing",
                                "loc": ["query", "annee_consommation"],
                                "msg": "Input should be a valid integer, unable to parse string as an integer",
                                "input": "abc"
                            }
                        ]
                    }
                }
            },
        },
        500: {
            "description": "Erreur serveur interne.",
            "content": {
                "application/json": {
                    "example": {"detail": "Erreur serveur interne. Impossible de récupérer les données."}
                }
            },
        },
    },
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
    responses={
        200: {
            "description": "L'API est en ligne et fonctionnelle.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "API en ligne et fonctionnelle."
                    }
                }
            },
        },
    },
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
    responses={
        200: {
            "description": "Bienvenue sur l'API PowerPredict, visite /docs pour l'exploiter",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Bienvenue sur l'API PowerPredict, visite /docs pour l'exploiter"
                    }
                }
            },
        },
    },
)
async def home():
    """
    ### Racine de l'API.
    Renvoie un message de bienvenue.
    """
    return {"message": "Bienvenue sur l'API PowerPredict, visite /docs pour l'exploiter"}
