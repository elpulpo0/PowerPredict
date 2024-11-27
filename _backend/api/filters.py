from pydantic import BaseModel, Field
from typing import Optional

class APIFilters(BaseModel):
    annee_consommation: Optional[str] = Field(None, description="Filtrer par année de consommation")
    surface_declaree: Optional[int] = Field(None, description="Filtrer par surface déclarée")
    nombre_declaration: Optional[int] = Field(None, description="Filtrer par nombre de déclarations")
    vecteur_energie: Optional[str] = Field(None, description="Filtrer par vecteur énergétique")
    zone_climatique: Optional[str] = Field(None, description="Filtrer par zone climatique")
    nom_commune: Optional[str] = Field(None, description="Filtrer par nom de commune")
    nom_departement: Optional[str] = Field(None, description="Filtrer par département")
    nom_region: Optional[str] = Field(None, description="Filtrer par région")
