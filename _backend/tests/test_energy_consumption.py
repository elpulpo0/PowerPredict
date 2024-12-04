import pytest
from sqlalchemy import create_engine, inspect, text
import pandas as pd
import os

# Ajuster le chemin pour accéder à la base de données
DB_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "database",
        "energy_consumption.db"
    )
)

# Configurer la connexion à la base de données
@pytest.fixture(scope="module")
def db_connection():
    """Fixture pour se connecter à la base de données."""
    engine = create_engine(f"sqlite:///{DB_PATH}")
    connection = engine.connect()
    yield connection
    connection.close()

# Test 1 : Vérifier la connexion à la base de données
def test_database_connection(db_connection):
    """Vérifie si la connexion à la base de données est établie."""
    assert db_connection is not None, "Connexion à la base de données échouée."

# Test 2 : Vérifier la présence des tables attendues
def test_table_presence(db_connection):
    """Vérifie que toutes les tables attendues sont présentes."""
    inspector = inspect(db_connection)
    expected_tables = {"consommation", "commune", "departement", "region", "zone_climatique", "vecteur_energie"}
    actual_tables = set(inspector.get_table_names())
    missing_tables = expected_tables - actual_tables
    assert missing_tables == set(), f"Tables manquantes : {missing_tables}"

# Test 3 : Vérifier la structure des colonnes pour chaque table
@pytest.mark.parametrize("table_name, expected_columns", [
    ("consommation", ["id_consommation", "annee_consommation", "surface_declaree", "nombre_declaration",
                      "consommation_declaree", "densite_energetique",
                      "consommation_log", "consommation_etat", "id_zone_climatique", "id_vecteur_energie", "id_commune"]),
    ("commune", ["id_commune", "nom_commune", "id_departement"]),
    ("departement", ["id_departement", "nom_departement", "id_region"]),
    ("region", ["id_region", "nom_region"]),
    ("zone_climatique", ["id_zone_climatique", "zone_climatique"]),
    ("vecteur_energie", ["id_vecteur_energie", "vecteur_energie"]),
])
def test_table_columns(db_connection, table_name, expected_columns):
    """Vérifie que chaque table contient les colonnes attendues."""
    inspector = inspect(db_connection)
    actual_columns = [column["name"] for column in inspector.get_columns(table_name)]
    missing_columns = set(expected_columns) - set(actual_columns)
    assert missing_columns == set(), f"Colonnes manquantes dans {table_name} : {missing_columns}"

# Test 4 : Vérifier les relations entre les tables
def test_foreign_key_constraints(db_connection):
    """Vérifie les contraintes de clé étrangère entre les tables."""
    inspector = inspect(db_connection)
    fk_checks = [
        ("consommation", "id_zone_climatique", "zone_climatique", "id_zone_climatique"),
        ("consommation", "id_vecteur_energie", "vecteur_energie", "id_vecteur_energie"),
        ("consommation", "id_commune", "commune", "id_commune"),
        ("commune", "id_departement", "departement", "id_departement"),
        ("departement", "id_region", "region", "id_region"),
    ]
    for table, column, ref_table, ref_column in fk_checks:
        fks = inspector.get_foreign_keys(table)
        assert any(
            fk["constrained_columns"] == [column] and
            fk["referred_table"] == ref_table and
            fk["referred_columns"] == [ref_column]
            for fk in fks
        ), f"Clé étrangère manquante ou incorrecte : {table}.{column} -> {ref_table}.{ref_column}"

# Test 5 : Vérifier que les tables contiennent des données
@pytest.mark.parametrize("table_name", ["consommation", "commune", "departement", "region", "zone_climatique", "vecteur_energie"])
def test_table_data(db_connection, table_name):
    """Vérifie que chaque table contient au moins une ligne."""
    query = text(f"SELECT COUNT(*) FROM {table_name}")
    result = db_connection.execute(query).scalar()
    assert result > 0, f"La table {table_name} est vide."

# Test 6 : Vérifier la cohérence des données
def test_data_consistency(db_connection):
    """Vérifie que les densités énergétiques sont cohérentes avec la consommation et la surface."""
    query = text("""
        SELECT id_consommation, surface_declaree, consommation_declaree, densite_energetique
        FROM consommation
        WHERE surface_declaree > 0
    """)
    df = pd.read_sql_query(query, db_connection)
    df["calculated_density"] = df["consommation_declaree"] / df["surface_declaree"]
    tolerance = 1e-6  # Tolérance pour les flottants
    inconsistent_rows = df[abs(df["calculated_density"] - df["densite_energetique"]) > tolerance]
    assert inconsistent_rows.empty, f"Densité énergétique incohérente pour les ID : {inconsistent_rows['id_consommation'].tolist()}"