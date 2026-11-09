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
#edit_df = st.data_editor(df)

#iterrows stampa una riga alla volta
for index, row in df.iterrows():

    #colonna 1 contiene il nostro dataframe
    #colonna 2 contiene pulsanti per la modifica
    col1, col2 = st.columns([3, 1])

    with col1:
        st.dataframe(pd.DataFrame([row]), width="stretch")

    with col2:
        #key = identificatore del pulsante
        if st.button("Modifica", key=f"modifica_{index}"):
            print("Pagina 2")