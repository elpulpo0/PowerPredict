import streamlit as st
from fonctions import fetch_table_names, fetch_table_data, paginate_data 

# Config esthétique de la page
st.set_page_config(
    page_title="PowerPredict",
    page_icon="📊",
    layout="wide",
)

API_URL = "https://powerpredict.onrender.com"

# Import CSS apparence
st.markdown(
    """
    <link href="./style.css" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# Titres et descriptions
st.title("📊 PowerPredict")
st.write("PowerPredict est un outil de visualisation de données de consommation d'énergie")

loading_html = """
<div style="text-align: center;">
    <img src="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif" width="150px" alt="Chargement...">
    <p>Chargement des données, veuillez patienter...</p>
</div>
"""
#option2
#<iframe src="https://giphy.com/embed/l3nWhI38IWDofyDrW" 
#width="100%" height="100%" style="position:absolute" 
#frameBorder="0" class="giphy-embed" allowFullScreen>
#</iframe>
##</div>
#<p>
#<a href="https://giphy.com/gifs/thinking-l3nWhI38IWDofyDrW">via GIPHY</a>
#</p>
#"""
loading_placeholder = st.markdown(loading_html, unsafe_allow_html=True)

# Fetch data
table_names = fetch_table_names(f"{API_URL}/tables")
loading_placeholder.empty()

if table_names:
    selected_table = st.sidebar.selectbox("Sélectionner une table", table_names)



# Fetch toutes les tables dans la base de données
table_names = fetch_table_names(f"{API_URL}/tables")
selected_table = None  # Initialize selected_table

if table_names:
    selected_table = st.sidebar.selectbox("Sélectionner une table", table_names)

if selected_table:
    table_data = fetch_table_data(f"{API_URL}/data", selected_table)

    if not table_data.empty:
        page_size = st.sidebar.slider(
            "Nombre de lignes par page", min_value=5, max_value=100, value=10, step=5
        )

        paginated_data = paginate_data(table_data, page_size)
        st.dataframe(paginated_data, use_container_width=True)
    else:
        st.warning("🚫 Pas de données pour la table sélectionnée")
else:
    st.warning("🚫 Veuillez sélectionner une table")
