import sqlite3
from typing import Dict, Any
from loguru import logger

class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def fetch_filtered_data(self, table: str, filters: Dict[str, Any]):
        """
        Récupérer les données filtrées d'une table spécifique.

        Args:
            table (str): Nom de la table à interroger.
            filters (Dict): Un dictionnaire contenant les colonnes et les valeurs à filtrer.

        Returns:
            List[Dict]: Liste de dictionnaires représentant les données filtrées.
        """
        try:
            query = f"SELECT * FROM {table} WHERE " + " AND ".join([f"{key} = ?" for key in filters.keys()])
            conn = sqlite3.connect(self.db_url)
            cursor = conn.cursor()
            cursor.execute(query, tuple(filters.values()))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            conn.close()

            return [dict(zip(columns, row)) for row in rows]
        
        except sqlite3.Error as e:
            logger.error(f"Erreur lors de la récupération des données de {table} : {e}")
            return []

db_clean = Database('database/clean_data.db')
db_encoded = Database('database/energy_consumption.db')

