from fastapi import FastAPI
from _backend.api.api import router as api_router

app = FastAPI()

# Ajouter les routes de l'API
app.include_router(api_router, prefix="/api", tags=["Database API"])
