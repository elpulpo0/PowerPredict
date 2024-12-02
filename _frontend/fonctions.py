import pandas as pd
import requests
import streamlit as st

# URL de base de l'API
API_BASE_URL = "https://powerpredict.onrender.com"

def fetch_data(filters):
    """
    Appelle l'API /data avec des filtres.

    Args:
        filters (dict): Dictionnaire contenant les filtres pour la requête.

    Returns:
        dict: Réponse de l'API au format JSON.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/data", params=filters)
        response.raise_for_status()  # Vérifie s'il y a une erreur HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Une erreur est survenue lors de la connexion à l'API : {e}")
        return {}

def fetch_table_names(api_url=f"{API_BASE_URL}/data"):
    """
    Récupère les noms des tables disponibles via l'API.

    Args:
        api_url (str): URL de l'API pour récupérer les noms des tables.

    Returns:
        list: Liste des noms de tables disponibles.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Une erreur est survenue lors de la connexion à l'API : {e}")
        return []

def fetch_table_data(api_url, table_name):
    """
    Récupère les données d'une table via l'API.

    Args:
        api_url (str): URL de l'API.
        table_name (str): Nom de la table à récupérer.

    Returns:
        pd.DataFrame: Données de la table au format DataFrame.
    """
    try:
        response = requests.get(f"{api_url}/{table_name}")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Une erreur est survenue lors de la connexion à l'API : {e}")
        return pd.DataFrame()

def paginate_data(dataframe, page_size):
    """
    Paginer un DataFrame pour l'affichage.

    Args:
        dataframe (pd.DataFrame): DataFrame à paginer.
        page_size (int): Nombre de lignes par page.

    Returns:
        pd.DataFrame: DataFrame paginé pour la page actuelle.
    """
    total_rows = len(dataframe)
    total_pages = (total_rows // page_size) + (1 if total_rows % page_size != 0 else 0)

    # Sélection du numéro de page
    page_number = st.sidebar.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

    start_row = (page_number - 1) * page_size
    end_row = start_row + page_size

    st.caption(f"Page {page_number} sur {total_pages}")
    return dataframe.iloc[start_row:end_row]

# Récupération des paramètres de filtrage
nom_region = st.sidebar.text_input("Nom de la région")
nom_departement = st.sidebar.text_input("Nom du département")
annee_consommation = st.sidebar.number_input("Année de consommation", min_value=2020, max_value=2025, step=1)
surface_declaree = st.sidebar.number_input("Surface déclarée (m²)", min_value=0.0, step=1.0)
nombre_declaration = st.sidebar.number_input("Nombre de déclarations", min_value=0, step=1)
vecteur_energie = st.sidebar.text_input("Vecteur d'énergie")
zone_climatique = st.sidebar.text_input("Zone climatique")
nom_commune = st.sidebar.text_input("Nom de la commune")

# Mettre les paramètres dans un dictionnaire
filters = {
    "region": nom_region,
    "departement": nom_departement,
    "annee_consommation": annee_consommation,
    "surface_declaree": surface_declaree,
    "nombre_declaration": nombre_declaration,
    "vecteur_energie": vecteur_energie,
    "zone_climatique": zone_climatique,
    "commune": nom_commune
}

# Appeler la fonction pour récupérer les données
filtered_data = fetch_data(filters)
