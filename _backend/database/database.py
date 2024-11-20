import sqlite3
from pathlib import Path
from typing import List, Dict

# Chemin vers la base de données
DATABASE_PATH = Path(__file__).parent / "database.db"

class SQLiteDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_table_names(self) -> List[str]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
        return tables

    def fetch_table_data(self, table_name: str) -> List[Dict]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name};")
            columns = [description[0] for description in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return data

db = SQLiteDatabase(DATABASE_PATH)
