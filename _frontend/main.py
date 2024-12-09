import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Configuration de la page
st.set_page_config(
    page_title="PowerPredict",
    page_icon="\U0001F4CA",
    layout="wide",
    initial_sidebar_state="expanded"
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

# URL de l'API
API_BASE_URL = "https://powerpredict.onrender.com"

# Titre principal
st.title("\U0001F4CA PowerPredict")
st.write("Analyse et prédiction de la consommation énergétique.")

# Hero section
st.image("https://hvacrcareerconnectny.com/wp-content/uploads/2022/06/Shutterstock_1936882618-1-1200x400.jpg?text=Bienvenue+sur+PowerPredict", caption="Optimisez votre consommation énergétique grâce à des prédictions précises.", use_container_width=True)

# Bouton "Réveiller l'API"
if st.button("\U0001F501 Réveiller l'API"):
    with st.spinner("Réveil et vérification de l'API en cours..."):
        health_status = check_api_health()
    if health_status == "OK":
        st.success("✅ API réveillée avec succès!")
    else:
        st.error(f"🚨 Problème avec l'API: {health_status}")

# Bloc 1 : Visualisation des données
st.header("🔍 Visualisation des données")
with st.form(key="data_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        annee_consommation = st.selectbox("Année de consommation", ["2020", "2021", "2022"], key="annee")
        vecteur_energie = st.text_input("Vecteur énergétique", key="vecteur")
    
    with col2:
        zone_climatique = st.text_input("Zone Climatique", key="zone")
        commune = st.text_input("Nom de la commune", key="commune")

    with col3:
        departement = st.text_input("Nom du département", key="departement")
        region = st.text_input("Nom de la région", key="region")
        consommation_etat = st.text_input("Etat consommation", key="etat")

    # Bouton de soumission des filtres
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
                            template="plotly_white",
                        )
                        st.plotly_chart(fig)
                else:
                    st.error(f"🚨 Erreur: {response.json().get('detail', 'Impossible de récupérer les données.')}")
            except Exception as e:
                st.error(f"🚨 Une erreur est survenue : {e}")

# Bloc 2 : Prédictions
st.header("📈 Prédictions de consommation")
with st.form(key="predict_form"):
    col1, col2 = st.columns(2)

    with col1:
        surface_declaree = st.number_input("Surface déclarée (m²)", min_value=1, step=1, key="surface")
        commune = st.text_input("Commune", key="predict_commune")

    with col2:
        annee_consommation = st.text_input("Année de consommation", key="predict_annee")
        vecteur_energie = st.text_input("Vecteur énergétique (Fioul, électricité ou gaz)", key="predict_vecteur")

    # Bouton de soumission pour la prédiction
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
                    st.write(f"Le modèle **{prediction['Modèle utilisé']}** à estimé la consommation à **{prediction['Prédiction (kWh)']} kWh**")
                else:
                    # Gestion des erreurs API
                    st.error(f"🚨 Erreur: {response.json().get('detail', 'Impossible d’effectuer la prédiction.')}")

            except Exception as e:
                st.error(f"🚨 Une erreur est survenue : {e}")
