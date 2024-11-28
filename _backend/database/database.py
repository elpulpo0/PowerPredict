import sqlite3
from typing import Dict, Any
from loguru import logger

class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def fetch_filtered_data(self, filters: Dict[str, Any]):
        """
        Récupérer les données jointes filtrées à partir des relations entre tables.

        Args:
            filters (Dict): Filtres à appliquer aux données.

        Returns:
            List[Dict]: Liste de données filtrées avec jointures.
        """
        try:
            # Base de la requête SQL
            query = """
                SELECT 
                    consommation.surface_declaree,
                    consommation.nombre_declaration,
                    consommation.consommation_declaree,
                    commune.nom_commune,
                    departement.nom_departement,
                    region.nom_region,
                    vecteur_energie.vecteur_energie,
                    zone_climatique.zone_climatique
                FROM 
                    consommation
                JOIN 
                    commune ON consommation.id_commune = commune.id_commune
                JOIN 
                    departement ON commune.id_departement = departement.id_departement
                JOIN 
                    region ON departement.id_region = region.id_region
                JOIN 
                    vecteur_energie ON consommation.id_vecteur_energie = vecteur_energie.id_vecteur_energie
                JOIN 
                    zone_climatique ON consommation.id_zone_climatique = zone_climatique.id_zone_climatique
            """

            # Ajout des filtres dynamiques
            if filters:
                conditions = " AND ".join([f"LOWER({key}) = LOWER(?)" for key in filters.keys()])
                query += f" WHERE {conditions}"

            # Connexion à la base de données avec gestion contextuelle
            with sqlite3.connect(self.db_url) as conn:
                cursor = conn.cursor()

                # Exécution de la requête
                cursor.execute(query, tuple(filters.values()))
                rows = cursor.fetchall()

                if not rows:
                    logger.warning("Aucune ligne retournée pour cette requête.")

                # Récupérer les noms de colonnes
                columns = [desc[0] for desc in cursor.description]

            return [dict(zip(columns, row)) for row in rows]

        except sqlite3.Error as e:
            logger.error(f"Erreur SQLite : {e}")
            return []

# Instanciation de la base de données
db = Database('database/energy_consumption.db')
