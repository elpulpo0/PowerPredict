from pydantic import BaseModel, Field
from typing import Optional

class APIFilters(BaseModel):
    annee_consommation: Optional[str] = Field(None, description="Filtrer par année de consommation")
    vecteur_energie: Optional[str] = Field(None, description="Filtrer par vecteur énergétique")
    zone_climatique: Optional[str] = Field(None, description="Filtrer par zone climatique")
    nom_commune: Optional[str] = Field(None, description="Filtrer par nom de commune")
    nom_departement: Optional[str] = Field(None, description="Filtrer par département")
    nom_region: Optional[str] = Field(None, description="Filtrer par région")
    consommation_etat: Optional[str] = Field(None, description="Filtrer par état de la consommation")

class PredictionFilters(BaseModel):
    surface_declaree: float = Field(None, description="Indiquez la surface")
    location_name: str = Field(None, description="Lieu (Ville, région, etc.)")
    vecteur_energie: Optional[str] = Field(None, description="Vecteur énergétique (ex: Électricité, Gaz, etc.)")
    annee_consommation: Optional[str] = Field(None, description="Année de consommation (ex: 2020)")
