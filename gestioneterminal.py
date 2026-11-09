import pandas as pd
import sqlite3
import streamlit as st

#connessione file csv
df = pd.read_csv("dati.csv")

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
st.dataframe(df)

'''# Input box
name = st.text_input("Enter your name")
# Button
if st.button("Submit"):
    st.write(f"Hello, {name}!")
# Slider
window = st.slider("Choose a window", 1, 100, 15)
st.write("Selected window:", window)'''




while True:
    print("[a] aggiungi ticket  [m] modifica  [e] elimina  [s] stampa")
    sel = input("Inserisci l'azione da svolgere: ")
    match sel:
        case 'a':
            #nel sito aprirà una form
            nome = input("Nome: ")
            cognome = input("Cognome: ")
            desc = input("Descrizione: ")
            cell = input("Cellulare: ")

            ticket = pd.DataFrame([{
            "Nome": nome,
            "Cognome": cognome,
            "Desc": desc,
            "Cellulare": cell
            }])

            df = pd.concat([df, ticket], ignore_index=True)
        case 'm':
            #chiedi ticket da scegliere.
            #mostra 
            #apre form come la pagina aggiunta ticket, ma con dati precompilati
            #una volta confermato, sostituisce i dati
            pass
        case 's':
            print(df)


    #aggiorna file database con il dataframe nuovo