import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import sqlite3
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from fonctions import fetch_data, paginate_data

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
vecteur_energie = st.sidebar.text_input("vecteur energetique")
zone_climatique = st.sidebar.text_input("Zone climatique")
nom_commune = st.sidebar.text_input("Nom de la commune")
surface_declaree = st.sidebar.number_input("Surface déclarée", min_value=0, step=1)

# Mettre les paramètres dans un dictionnaire
filters = {
    "region": nom_region,
    "departement": nom_departement,
    "annee_consommation": annee_consommation,
    "nombre_declaration": nombre_declaration,
    "vecteur_energie": vecteur_energie,
    "zone_climatique": zone_climatique,
    "commune": nom_commune,
    "surface_declaree": surface_declaree,
}

# Charger les données
if st.button("📥 Récupérer les données"):
    with st.spinner("Chargement des données..."):
        response = fetch_data(filters)
        
        if not response:
            st.error("🚨 Impossible de récupérer les données.")
        else:
            st.success("✅ Données récupérées avec succès!")
            st.json(response)

    
    # Convertir la réponse en DataFrame si elle est au format dictionnaire
    if isinstance(response, dict):
        table_data = pd.DataFrame([response]) if response else pd.DataFrame()
    elif isinstance(response, list):
        table_data = pd.DataFrame(response) if response else pd.DataFrame()
    else:
        table_data = pd.DataFrame()

    # S'assurer que table_data est défini et non vide pour la pagination
    if filters and not table_data.empty:
        # Ajouter les valeurs des filtres comme nouvelles colonnes
        for key, value in filters.items():
            if value:  # Ajouter uniquement les valeurs non vides des filtres
                table_data[key] = value

        page_size = st.sidebar.slider(
            "Nombre de lignes par page", min_value=5, max_value=100, value=10, step=5
        )

        # Appeler paginate_data uniquement si table_data contient des lignes
        paginated_data = paginate_data(table_data, page_size)
        st.dataframe(paginated_data, use_container_width=True)

        # Affichage graphique des consommations par commune
        if "nom_commune" in table_data.columns and "consommation_declaree" in table_data.columns:
            st.subheader("Graphique des Consommations par Commune")

            # Création du graphique
            fig = px.bar(
                table_data,
                x="nom_commune",
                y="consommation_declaree",
                color="consommation_declaree",
                color_continuous_scale=["green", "yellow", "red"],
                title="Consommation Déclarée par Commune",
                labels={
                    "nom_commune": "Commune",
                    "consommation_declaree": "Consommation (kWh)"
                }
            )

            # Personnalisation du graphique
            fig.update_layout(
                title_font=dict(size=24),
                xaxis_title="Commune",
                yaxis_title="Consommation Déclarée (kWh)",
                coloraxis_colorbar=dict(title="Consommation (kWh)")
            )

            # Afficher le graphique
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("🚨 Les colonnes nécessaires pour le graphique sont absentes.")


# Charger les modèles et les colonnes sauvegardées
gb_model = joblib.load("gradient_boosting_model.pkl")
all_features = joblib.load("all_features.pkl")

# Assurez-vous que all_features est une liste
if not isinstance(all_features, list):
    all_features = list(all_features)

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="geoapi")

# Fonction pour récupérer les coordonnées GPS à partir d'un nom de lieu
def get_coordinates(location_name):
    try:
        location = geolocator.geocode(location_name, country_codes="FR")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None

# Ajout des entrées de prédiction dans la barre latérale
st.sidebar.header("Faire une prédiction")
with st.sidebar.form(key="prediction_form"):
    surface_declaree = st.number_input("Surface déclarée (en m²)", min_value=0, step=1)
    commune = st.text_input("Commune")
    annee_consommation = st.selectbox("Année de consommation", ["2020", "2021", "2022"])
    vecteur_energie = st.text_input("Vecteur énergétique")
    prediction_button = st.form_submit_button("📈 Prédire")

# Si le bouton est cliqué
if prediction_button:
    if not (surface_declaree and commune and annee_consommation and vecteur_energie):
        st.error("🚨 Veuillez remplir toutes les informations pour effectuer une prédiction.")
    else:
        st.info("⏳ Calcul des coordonnées pour la commune...")
        latitude, longitude = get_coordinates(commune)
        
        if latitude is None or longitude is None:
            st.error("🚨 Impossible de trouver la localisation. Veuillez vérifier le nom de la commune.")
        else:
            # Préparation des données d'entrée
            input_data = {
                "surface_declaree": surface_declaree,
                "latitude": latitude,
                "longitude": longitude,
                "annee_consommation": int(annee_consommation),
                "vecteur_energie": vecteur_energie,
            }

            # Ajouter les colonnes manquantes avec des valeurs par défaut
            for feature in all_features:
                if feature not in input_data:
                    input_data[feature] = 0  # Valeur par défaut

            # Convertir en DataFrame et aligner les colonnes avec all_features
            input_data_df = pd.DataFrame([input_data])  # Créer le DataFrame
            input_data_df = input_data_df.reindex(columns=all_features)  # Réordonner les colonnes

            # Vérification des colonnes
            if not all(input_data_df.columns == all_features):
                st.error("🚨 Erreur : les colonnes ne correspondent pas aux features attendues.")
            else:
                # Effectuer la prédiction
                try:
                    prediction = gb_model.predict(input_data_df)
                    prediction_original = np.expm1(prediction)[0]

                    st.success("✅ Prédiction effectuée avec succès!")
                    st.write(f"Consommation prédite pour la commune {commune}: **{prediction_original:,.2f} kWh**")

                except Exception as e:
                    st.error(f"🚨 Une erreur est survenue lors de la prédiction : {e}")
