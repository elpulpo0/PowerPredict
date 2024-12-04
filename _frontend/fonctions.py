import pandas as pd
import requests
import streamlit as st
from loguru import logger

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
    valid_filters = {key: value for key, value in filters.items() if value}
    try:
        url = f"{API_BASE_URL}/data?"
        response = requests.get(url, params=valid_filters)
        response.raise_for_status()
        logger.info(f"Requête effectuée : {response.url}")

        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la connexion à l'API : {e}")
        st.error(f"🚨 Une erreur est survenue lors de la connexion à l'API : {e}")
        return {}

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


