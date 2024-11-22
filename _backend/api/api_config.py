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

# Réponses routes API

responses_data={
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
    }

responses_health={
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
    }

responses_home={
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
    }

initialisation_FastAPI = {
    "title": "PowerPredict API",
    "description": (
        "Une API pour interagir avec les données PowerPredict. "
        "Elle permet de filtrer les données et de vérifier l'état de l'application."
    ),
    "version": "1.0.0",
    "openapi_tags": [
        {
            "name": "Données PowerPredict",
            "description": "Endpoints pour interagir avec les données PowerPredict.",
        },
        {
            "name": "Santé API",
            "description": "Endpoint pour vérifier l'état de santé de l'API.",
        },
        {
            "name": "Home",
            "description": "Endpoint de démarrage de l'API.",
        },
    ],
}

