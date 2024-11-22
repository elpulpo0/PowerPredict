from fastapi import FastAPI
from api.api import router as api_router
from api.api_config import initialisation_FastAPI

app = FastAPI(**initialisation_FastAPI)

app.include_router(api_router)
