import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Configuration de la page
st.set_page_config(
    page_title="PowerPredict",
    page_icon="📊",
    layout="wide",
)

# Fonction pour vérifier la santé de l'API
def check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            return "OK"
        else:
            return f"Erreur: {response.status_code}"
    except Exception as e:
        return f"Erreur: {e}"

# Titres de la page
st.title("📊 PowerPredict")
st.write("Analyse et prédiction de la consommation énergétique.")

# URL de l'API
API_BASE_URL = "https://powerpredict.onrender.com"

# Bouton "Réveiller l'API"
with st.spinner("Vérification de l'API..."):
    if st.button("🔄 Réveiller l'API"):
        with st.spinner("En attente de la réponse de l'API..."):
            health_status = check_api_health()
        if health_status == "OK":
            st.success("✅ API réveillée avec succès!")
        else:
            st.error(f"🚨 Problème avec l'API: {health_status}")

# Bloc 1 : Visualisation des données
st.header("🔍 Visualisation des données")
with st.form(key="data_form"):
    st.sidebar.subheader("Filtres")
    annee_consommation = st.sidebar.selectbox("Année de consommation", ["2020", "2021", "2022"])
    vecteur_energie = st.sidebar.text_input("Vecteur énergétique")
    zone_climatique = st.sidebar.text_input("Zone Climatique")
    commune = st.sidebar.text_input("Nom de la commune")
    departement = st.sidebar.text_input("Nom du département")
    region = st.sidebar.text_input("Nom de la région")
    consommation_etat = st.sidebar.text_input("Etat consommation")

    # Filtrer les données
    data_submit = st.form_submit_button("📥 Charger les données")
    if data_submit:
        with st.spinner("Chargement des données..."):
            filters = {
                "annee_consommation": annee_consommation,
                "vecteur_energie": vecteur_energie,
                "zone_climatique": zone_climatique,
                "commune": commune,
                "departement": departement,
                "region": region,
                "consommation_etat": consommation_etat,
            }
            valid_filters = {key: value for key, value in filters.items() if value}
            try:
                response = requests.get(f"{API_BASE_URL}/data", params=valid_filters)
                if response.status_code == 200:
                    data = response.json()["data"]
                    st.success("✅ Données récupérées avec succès!")
                    df = pd.DataFrame(data)

                    # Affichage du tableau de données
                    st.dataframe(df)

                    # Affichage graphique des consommations
                    if "nom_commune" in df.columns and "consommation_declaree" in df.columns:
                        fig = px.bar(
                            df,
                            x="nom_commune",
                            y="consommation_declaree",
                            color="consommation_declaree",
                            title="Consommation par commune",
                            labels={"nom_commune": "Commune", "consommation_declaree": "Consommation (kWh)"},
                        )
                        st.plotly_chart(fig)
                else:
                    st.error(f"🚨 Erreur: {response.json().get('detail', 'Impossible de récupérer les données.')}")
            except Exception as e:
                st.error(f"🚨 Une erreur est survenue : {e}")

# Bloc 2 : Prédictions
st.header("📈 Prédictions de consommation")
with st.form(key="predict_form"):
    st.sidebar.subheader("Données de prédiction")
    surface_declaree = st.sidebar.number_input("Surface déclarée (m²)", min_value=1, step=1)
    commune = st.sidebar.text_input("Commune")
    annee_consommation = st.sidebar.text_input("Année de consommation")
    vecteur_energie = st.sidebar.text_input("Vecteur énergétique (Fioul, électricité ou gaz)")

    # Bouton de soumission
    predict_submit = st.form_submit_button("🔮 Prédire")
    if predict_submit:
        with st.spinner("Calcul de la prédiction..."):
            # Préparation des données au format attendu par l'API
            prediction_input = {
                "surface_declaree": surface_declaree,
                "location_name": commune,
                "annee_consommation": annee_consommation,
                "vecteur_energie": vecteur_energie,
            }

            try:
                # Appel à l'API pour effectuer la prédiction
                response = requests.get(f"{API_BASE_URL}/predict", params=prediction_input)

                if response.status_code == 200:
                    prediction = response.json()
                    st.success("✅ Prédiction effectuée avec succès!")

                    # Affichage des résultats
                    st.write(f"### Modèle utilisé : **{prediction['Modèle utilisé']}**")
                    st.write(f"### Consommation estimée : **{prediction['Prédiction (kWh)']} kWh**")
                else:
                    # Gestion des erreurs API
                    st.error(f"🚨 Erreur: {response.json().get('detail', 'Impossible d’effectuer la prédiction.')}")

            except Exception as e:
                st.error(f"🚨 Une erreur est survenue : {e}")
