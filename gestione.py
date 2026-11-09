import pandas as pd
import sqlite3
import streamlit as st

#connessione file csv
df = pd.read_csv("dati.csv")
df = df.set_index('ID')

# Configurazione pagina
st.set_page_config(
    page_title="My Application",
    page_icon="",
    layout="wide"
)

# Title
st.title("Gestore Ticket")

# Subtitle
st.header("Lista")

# Text
st.write("Ticket in attesa.")

#df
edit_df = st.data_editor(df)
