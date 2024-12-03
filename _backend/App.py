from fastapi import FastAPI
from api.api import router as api_router
from api.api_predict import router as predict_router
from api.api_config import initialisation_FastAPI
from logging_config import configure_logging

configure_logging()

app = FastAPI(**initialisation_FastAPI)

app.include_router(api_router)
app.include_router(predict_router)
