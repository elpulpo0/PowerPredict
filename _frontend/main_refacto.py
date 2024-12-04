import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import sqlite3
from fonctions import fetch_table_names, fetch_table_data, paginate_data 

st.set_page_config(
    page_title="PowerPredict",
    page_icon="📊",
    layout="wide",
)

API_URL = "https://powerpredict.onrender.com"

# Importer le CSS pour l'apparence
st.markdown(
    """
    <link href="./style.css" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# Titres et descriptions de la page
st.title("📊 PowerPredict")
st.write("PowerPredict est un outil de visualisation de données de consommation d'énergie")

loading_html = """
<div style="text-align: center;">
    <img src="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif" width="150px" alt="Chargement...">
    <p>Chargement des données, veuillez patienter...</p>
</div>
"""
loading_placeholder = st.markdown(loading_html, unsafe_allow_html=True)

# Initialiser selected_table
selected_table = None

# Récupérer tous les noms de tables depuis la base de données
try:
    response = requests.get(f"{API_URL}/data")
    response.raise_for_status()
    table_names = response.json().get('tables', []) if 'tables' in response.json() else []
except Exception as e:
    st.error(f"🚨 Une erreur est survenue lors de la connexion à l'API : {e}")
    table_names = []

if table_names:
    selected_table = st.sidebar.selectbox("Sélectionner une table", table_names)

# Vérifier si selected_table est défini avant de l'utiliser
if selected_table:
    try:
        # Définir les filtres pour l'année de consommation et d'autres paramètres
        filters = {
            "annee_consommation": st.sidebar.selectbox("Année de consommation", ["2020", "2021", "2022", "2023", "Année de référence"]),
            "region": st.sidebar.text_input("Région"),
            "departement": st.sidebar.text_input("Département"),
            "vecteur_energie": st.sidebar.text_input("Vecteur d'énergie"),
            "surface_declaree": st.sidebar.number_input("Surface déclarée", min_value=0.0, step=0.1),
            "nombre_declaration": st.sidebar.number_input("Nombre de déclarations", min_value=0, step=1),
            "zone_climatique": st.sidebar.text_input("Zone climatique"),
            "commune": st.sidebar.text_input("Commune"),
        }

        # Construire les paramètres de requête dynamiquement en omettant les valeurs vides
        params = {key: value for key, value in filters.items() if value and value != "Toutes" and value != "Tous" and value != "Année de référence"}

        # Passer les paramètres valides uniquement
        response = requests.get(f"{API_URL}/data", params=params)
        response.raise_for_status()
        table_data = pd.DataFrame(response.json())
    except requests.exceptions.HTTPError as http_err:
        st.error(f"🚨 Une erreur HTTP est survenue : {http_err}")
        st.write(f"URL: {response.url}")
        st.write(f"Response Content: {response.text}")
        table_data = pd.DataFrame()
    except Exception as e:
        st.error(f"🚨 Une erreur est survenue lors de la connexion à l'API : {e}")
        table_data = pd.DataFrame()

    if not table_data.empty:
        # Supprimer l'animation de chargement une fois les données récupérées
        loading_placeholder.empty()

        # Extraire les valeurs uniques pour les colonnes pertinentes
        regions = table_data['region'].unique() if 'region' in table_data.columns else []
        departements = table_data['departement'].unique() if 'departement' in table_data.columns else []
        vecteurs_energie = table_data['vecteur_energie'].unique() if 'vecteur_energie' in table_data.columns else []

        # Créer des menus déroulants basés sur les données de l'API
        selected_region = st.sidebar.selectbox("Sélectionner une région", ["Toutes"] + list(regions))
        selected_departement = st.sidebar.selectbox("Sélectionner un département", ["Tous"] + list(departements))
        selected_vecteur_energie = st.sidebar.selectbox("Sélectionner un vecteur d'énergie", ["Tous"] + list(vecteurs_energie))

        # Appliquer les filtres sur les données
        filtered_data = table_data.copy()
        if selected_region != "Toutes":
            filtered_data = filtered_data[filtered_data['region'] == selected_region]
        if selected_departement != "Tous":
            filtered_data = filtered_data[filtered_data['departement'] == selected_departement]
        if selected_vecteur_energie != "Tous":
            filtered_data = filtered_data[filtered_data['vecteur_energie'] == selected_vecteur_energie]

        # Vérifier si 'year' est une colonne dans les données
        if 'year' in filtered_data.columns:
            # Diagramme linéaire des tendances de consommation d'énergie par année
            fig = px.line(
                filtered_data[filtered_data['year'] == int(filters['annee_consommation'])] if filters['annee_consommation'] != 'Année de référence' else filtered_data,
                x='month',
                y='consumption',
                title=f"Tendances de consommation pour l'année {filters['annee_consommation']}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("🚫 Pas de données disponibles pour l'année sélectionnée")

        # Créer un diagramme en barres pour la consommation totale par vecteurs d'énergie
        if 'vecteur_energie' in filtered_data.columns and 'consumption' in filtered_data.columns:
            total_consumption = filtered_data.groupby('vecteur_energie')['consumption'].sum().reset_index()
            bar_fig = px.bar(total_consumption, x='vecteur_energie', y='consumption', title="Consommation totale par vecteur d'énergie")
            st.plotly_chart(bar_fig, use_container_width=True)
        else:
            st.warning("🚫 Les colonnes 'vecteur_energie' et 'consumption' sont manquantes dans les données")
        
    else:
        st.warning("🚨 Pas de données pour la table sélectionnée")
else:
    st.warning("🚨 Veuillez sélectionner une table.")

# S'assurer que table_data est défini et non vide pour la pagination
if selected_table and not table_data.empty:
    page_size = st.sidebar.slider(
        "Nombre de lignes par page", min_value=5, max_value=100, value=10, step=5
    )

    # Appeler paginate_data uniquement si table_data contient des lignes
    paginated_data = paginate_data(filtered_data, page_size)
    st.dataframe(paginated_data, use_container_width=True)
else:
    st.warning("🚫 Pas de données à afficher pour la table sélectionnée.")





#main.py

 # Vérifier si 'year' est une colonne dans les données
if 'year' in filters.columns:
            # Diagramme linéaire des tendances de consommation d'énergie par année
            fig = px.line(
                filters[filters['year'] == int(filters['annee_consommation'])] if filters['annee_consommation'] != 'Année de référence' else filters,
                x='month',
                y='consumption',
                title=f"Tendances de consommation pour l'année {filters['annee_consommation']}"
            )
            st.plotly_chart(fig, use_container_width=True)
else:
            st.warning("🚫 Pas de données disponibles pour l'année sélectionnée")

        # Créer un diagramme en barres pour la consommation totale par vecteurs d'énergie
if 'vecteur_energie' in filters.columns and 'consumption' in filters.columns:
            total_consumption = filters.groupby('vecteur_energie')['consumption'].sum().reset_index()
            bar_fig = px.bar(total_consumption, x='vecteur_energie', y='consumption', title="Consommation totale par vecteur d'énergie")
            st.plotly_chart(bar_fig, use_container_width=True)
else:
            st.warning("🚫 Les colonnes 'vecteur_energie' et 'consumption' sont manquantes dans les données")