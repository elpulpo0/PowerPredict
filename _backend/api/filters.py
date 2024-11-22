from pydantic import BaseModel, Field
from typing import Optional

class APIFilters(BaseModel):
    nombre_declaration: Optional[int] = Field(None, description="Filtrer par nombre de déclarations")
    surface_declaree: Optional[int] = Field(None, description="Filtrer par surface déclarée")
    vecteur_energie: Optional[str] = Field(None, description="Filtrer par vecteur énergie")
    annee_consommation: Optional[int] = Field(None, description="Filtrer par année de consommation")
    zone_climatique: Optional[str] = Field(None, description="Filtrer par zone climatique")
    code_region: Optional[str] = Field(None, description="Filtrer par code région")
    code_departement: Optional[str] = Field(None, description="Filtrer par code département")
    nom_commune: Optional[str] = Field(None, description="Filtrer par nom de commune")