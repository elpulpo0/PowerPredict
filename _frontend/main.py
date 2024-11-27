import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from streamlit import connection


database_path = Path(__file__).parent / "_backend/database/database.db" #en attendant de trouver le bon chemin
                                  

#streamlit frontend apparence
st.set_page_config(
    page_title="SQLite DB Viewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

#CSS apparence file style.css a la racine main
#file fonctions.py 
st.markdown(
    """
    <style>
    .main{
        background-color: #f5f5f5;
    }
    .sidebar .sidebar-content{
    background: linear-gradient(45deg, #6b9ac4, #abdcff);
    color: white;
    }
    st-df table {
    margin-top:20px;
    font-size: 14px;
    border-collapse; collapse;
    width: 100%;
    }
    .st-df th {
    background-color: 4cAF50;
    color: white
    padding: 10px;
    text-align: center;

    }
</style>
""",
unsafe_allow_html=True,
)

if not Path(database_path).exists():
    st.error("🚨 Le chemin vers le fichier de base de données n'est pas correct")
else:
    conn = sqlite3.connect(database_path)
    st.title("📊 PowerPredict")

    #Fetch toutes les tables dans la base de données
    @st.cache
    def get_table_names(connection):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        return pd.read_sql_query(query, connection)
    
    try:
        table_names = get_table_names(conn)
    except Exception as e:
        st.error(f"le nom des tables est introuvable: {e}")
        table_names = []

    if table_names:
        #selection de la table
        selected_table = st.sidebar.radio("selectionner une table", table_names, key="table_selection")

        @st.cache
        def fetch_table_data(connection, table_name):
        query = f"SELECT * FROM {table_name};" # type: ignore #query toute data mais table_name pas defini
        return pd.read_sql_query(query, connection)
    
    try:
        table_data = fetch_table_data(conn, selected_table) # type: ignore
        st.subheader(f"📋 Donnees de la table": {selected_table})
        st.dataframe(table_data.style.set_properties(**{
            "background-color": "fdfdfd",
            "color": "333333",
            "border": "1px solid #ddd",
        }),
        use_container_width=True, #width de table
        )
    except Exception as e:
        st.error(f"erreur a la recuperation des donnees de la table '{selected_table'}: {e}") # type: ignore 
                                                                      
    else:
        st.warning("⛔️ aucune table n'est selectionnee")

with st.sidebar:
    st.markdown("### A propos")
    st.info("utilisez cet outils pour explorer les tables dans la base de donnees. selectionnez une table")
    st.markdown("### Notes")
    st.write(" 💾 verifiez que le fichier est bien dans le bon chemin")

#fermer la connexion a la database
conn.close()