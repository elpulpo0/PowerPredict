import pandas as pd
import requests
import streamlit as st

def fetch_table_names(api_url="https://powerpredict.onrender.com/tables"):
    """
    Fetch table names from the API.

    Args:
        api_url (str): URL of the API (e.g., "https://powerpredict.onrender.com/tables")

    Returns:
        list: List of table names
    """
    try: 
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("⛔️ Pas de réponse de l'API")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Une erreur est survenue lors de la connexion à l'API : {e}")
        return []

def fetch_table_data(api_url, table_name, params=None):
    """
    Fetch data from a table in the API.

    Args:
        api_url (str): URL of the API (e.g., "https://powerpredict.onrender.com/data")
        table_name (str): Name of the table

    Returns:
        pd.DataFrame: Data from the table
    """
    try:
        response = requests.get(f"{api_url}/{table_name}", params=params)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"🚨 La table '{table_name}' n'existe pas")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Une erreur est survenue lors de la connexion à l'API : {e}")
        return pd.DataFrame()

def fetch_table_data_db(connection, table_name, conditions=None):
    """
    Fetch data from a table in the local SQLite database.

    Args:
        connection (sqlite3.Connection): SQLite connection object
        table_name (str): Name of the table
        conditions (dict, optional): Conditions to filter rows, provided as key-value pairs

    Returns:
        pd.DataFrame: Data from the table
    """
    query = f"SELECT * FROM {table_name}"
    if conditions:
        where_clause = ' AND '.join([f"{key}='{value}'" for key, value in conditions.items()])
        query += f" WHERE {where_clause}"
    return pd.read_sql_query(query, connection)


def paginate_data(dataframe, page_size):
    """
    Paginate a DataFrame for display.

    Args:
        dataframe (pd.DataFrame): DataFrame to paginate
        page_size (int): Number of rows per page

    Returns:
        pd.DataFrame: Paginated DataFrame for the current page
    """
    total_rows = len(dataframe)
    total_pages = (total_rows // page_size) + (1 if total_rows % page_size != 0 else 0)

    # Page number selection
    page_number = st.sidebar.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

    start_row = (page_number - 1) * page_size
    end_row = start_row + page_size

    st.caption(f"Page {page_number} sur {total_pages}")
    return dataframe.iloc[start_row:end_row]
