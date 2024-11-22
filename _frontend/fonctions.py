import pandas as pd
import requests
import streamlit as st 

def fetch_table_names(api_url):
    """
    Fetch noms de table depuis l'API
    args:
        api_url (str): URL de l'API
    Returns:
        list: Liste des noms de table
    """

    try: 
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("⛔️ Pas de réponse de l'API")
            return []
    except Exception as e:
        st.error(f"🚨 Une erreur est survenue : {e}")
        return []
    
    def fetch_table_data(api_url, table_name):
        """ 
        Fetch data from a table in the API
        Args:
            api_url (str): URL of the API
            table_name (str): Name of the table
        Returns:
            pd.DataFrame: Data from the table
        """
        try:
            response = requests.get(f"{api_url}/{table_name}")
            if response.status_code == 200:
                return pd.DataFrame(response.json())
            else:
                st.error(f"🚨 la table {table_name} n'existe pas")
                return pd.DataFrame()
        except Exception as e:
            st.error(f"🚨 Une erreur est survenue : {e}")
            return pd.DataFrame()
        


def paginate_data(dataframe, page_size):
    """
    Fetch data from a table in the API
    args:
        dataframe (pd.Dataframe): Dataframe to paginate
        page_size (int): Nombre de lignes par page
    Returns:
        pd.DataFrame: Dataframe de la page
    """
total_rows = len(dataframe)
total_pages = (total_rows // page_size)  + (1 if total_rows % page_size != 0 else 0)

#nro de page
page_number = st.sidebar.number_input("Page", min_value=1, max_value=total_pages, value=1,step=1)

start_row = (page_number - 1) * page_size
end_row = start_row + page_size

st.caption(f"Page {page_number} of {total_pages}")
return dataframe.iloc[start_row:end_row]

