from fastapi import FastAPI
from api.api import router as api_router

app = FastAPI(
    title="PowerPredict API",
    description=(
        "Une API pour interagir avec les données PowerPredict. "
        "Elle permet de filtrer les données et de vérifier l'état de l'application."
    ),
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Données PowerPredict",
            "description": "Endpoints pour interagir avec les données PowerPredict.",
        },
        {
            "name": "Santé API",
            "description": "Endpoints pour vérifier l'état de santé de l'API.",
        },
    ],
)

app.include_router(api_router)
