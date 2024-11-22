import streamlit as st
from fonctions import fetch_table_names, fetch_table_data, paginate_data 


#config esthetique de la page
st.set_page_config(
    page_title="PowerPredict",
    page_icon="📊",
    layout="wide",
)

API_URL = "http://127.0.0.1:8000"

#import CSS apparence
st.markdown(
    """
    <link href="./style.css" rel="stylesheet">
    """,
unsafe_allow_html=True,
)
#fin CSS apparence     


#titres et descriptions
st.title("📊 PowerPredict")
st.write("PowerPredict est un outil de visualisation de données de consommation d'energie")

#Fetch toutes les tables dans la base de données
table_names = fetch_table_names(f"{API_URL}/tables")
if table_names:
    selected_table = st.sidebar.selectbox("Selectionner une table", table_names)

if selected_table:
    table_data = fetch_table_data(f"{API_URL}/data", selected_table)

    if not table_data.empty:
        page_size = st.sidebar.slider(
            "Nombre de lignes par page", min_value=5, max_value=100, value=10, step=5
        )

        paginate_data = paginate_data(table_data, page_size)
        st.dataframe(paginate_data, use_container_width=True)
    else:
        st.warning("🚫 Pas de donnees pour la table selectionnee")
else:
    st.warning("🚫 Veuillez selectionner une table")