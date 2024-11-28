import streamlit as st
from fonctions import fetch_table_names, fetch_table_data, paginate_data 
import pandas as pd
import plotly.express as px

# Configuration esthétique de la page
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

# Initialiser selected_table et year_selected
selected_table = None
year_selected = None  # Initialiser year_selected à None

# Récupérer tous les noms de tables depuis la base de données
table_names = fetch_table_names(f"{API_URL}/tables")

if table_names:
    selected_table = st.sidebar.selectbox("Sélectionner une table", table_names)

# Vérifier si selected_table est défini avant de l'utiliser
if selected_table:
    table_data = fetch_table_data(f"{API_URL}/data", selected_table)

    if not table_data.empty:
        # Supprimer l'animation de chargement une fois les données récupérées
        loading_placeholder.empty()

        # Créer un widget de saisie de date pour sélectionner l'année
        year_selected = st.sidebar.date_input(
            "Sélectionner l'année",
            value=pd.to_datetime('2023-01-01'),
            min_value=pd.to_datetime('2020-01-01'),
            max_value=pd.to_datetime('2024-01-01'),
        ).year
        
        # Utiliser year_selected en toute sécurité
        st.write(f'Année sélectionnée: {year_selected}')

        # Vérifier si 'year' est une colonne dans les données
        if 'year' in table_data.columns:
            # Diagramme linéaire des tendances de consommation d'énergie par année
            fig = px.line(table_data[table_data['year'] == year_selected], x='month', y='consumption', title=f'Tendances de consommation pour l\'année {year_selected}')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("🚫 Pas de données disponibles pour l'année sélectionnée")

        # Créer un diagramme en barres pour la consommation totale par vecteurs d'énergie
        if 'vecteur_energie' in table_data.columns and 'consumption' in table_data.columns:
            total_consumption = table_data.groupby('vecteur_energie')['consumption'].sum().reset_index()
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
    paginated_data = paginate_data(table_data, page_size)
    st.dataframe(paginated_data, use_container_width=True)
else:
    st.warning("🚫 Pas de données à afficher pour la table sélectionnée.")
