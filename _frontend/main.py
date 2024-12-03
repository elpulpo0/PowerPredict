import streamlit as st
import pandas as pd
# import plotly.express as px
import requests
import sqlite3
from fonctions import fetch_data

st.set_page_config(
    page_title="PowerPredict",
    page_icon="📊",
    layout="wide",
)

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

# Récupération des paramètres de filtrage
nom_region = st.sidebar.text_input("Nom de la région")
nom_departement = st.sidebar.text_input("Nom du département")
annees_possibles = ["2020", "2021", "2022", "Année de référence"]
annee_consommation = st.sidebar.selectbox("Choisissez une option :", annees_possibles)
nombre_declaration = st.sidebar.number_input("Nombre de déclarations", min_value=0, step=1)
vecteur_energie = st.sidebar.text_input("Vecteur d'énergie")
zone_climatique = st.sidebar.text_input("Zone climatique")
nom_commune = st.sidebar.text_input("Nom de la commune")

# Saisie des filtres par l'utilisateur
# region = st.text_input("Région", "guadeloupe", help="Entrez la région à filtrer")
# zone_climatique = st.text_input("Zone Climatique", "GUA", help="Entrez la zone climatique à filtrer")

# Mettre les paramètres dans un dictionnaire
filters = {
    "region": nom_region,
    "departement": nom_departement,
    "annee_consommation": annee_consommation,
    "nombre_declaration": nombre_declaration,
    "vecteur_energie": vecteur_energie,
    "zone_climatique": zone_climatique,
    "commune": nom_commune
}

if st.button("📥 Récupérer les données"):
    with st.spinner("Chargement des données..."):
        response = fetch_data(filters)
        
        if not response:
            st.error("🚨 Impossible de récupérer les données.")
        else:
            st.success("✅ Données récupérées avec succès!")
            st.json(response)
