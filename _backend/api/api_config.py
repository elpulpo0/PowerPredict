VALID_COLUMNS_DATA = [
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

VALID_COLUMNS_TRAIN = ['id', 'nombre_declaration', 'surface_declaree', 'annee_consommation_2020', 'annee_consommation_2021', 'annee_consommation_2022', 'annee_consommation_Année de référence', 'zone_climatique_GUA', 'zone_climatique_GUY', 'zone_climatique_H1a', 'zone_climatique_H1b', 'zone_climatique_H1c', 'zone_climatique_H2a', 'zone_climatique_H2b', 'zone_climatique_H2c', 'zone_climatique_H2d', 'zone_climatique_H3', 'zone_climatique_MAR', 'zone_climatique_MAY', 'zone_climatique_REU', 'code_region_00', 'code_region_01', 'code_region_02', 'code_region_03', 'code_region_04', 'code_region_06', 'code_region_11', 'code_region_24', 'code_region_27', 'code_region_28', 'code_region_32', 'code_region_44', 'code_region_52', 'code_region_53', 'code_region_75', 'code_region_76', 'code_region_84', 'code_region_93', 'code_region_94', 'code_region_ND', 'code_departement_encoded', 'commune_frequency', 'vecteur_energie_Bois', 'vecteur_energie_Electricite', 'vecteur_energie_Fioul', 'vecteur_energie_Gaz', 'vecteur_energie_Non spécifié', 'vecteur_energie_Reseau de chaleur', 'vecteur_energie_Reseau de froid', 'annee_consommation_reference', 'densite_energetique', 'ratio_declaration_consommation', 'consommation_relative_climat', 'surface_par_declaration', 'consommation_log', 'consommation_declaree', 'consommation_anormale_Anormale', 'consommation_anormale_Normale']
VALID_COLUMNS_TEST = VALID_COLUMNS_TRAIN

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

responses_test_train={
        200: {"description": "Données encodées récupérées avec succès."},
        404: {"description": "Aucune donnée trouvée."},
        500: {"description": "Erreur serveur."},
    }

# Arguments FastAPI

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
            "name": "Données Encodées",
            "description": "Endpoints pour interagir avec les données encodées",
        },
        {
            "name": "Santé API",
            "description": "Endpoint pour vérifier l'état de santé de l'API.",
        },
    ],
}
