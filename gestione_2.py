import pandas as pd
import streamlit as st

df = pd.read_csv("dati.csv")
df = df.set_index("ID")

st.set_page_config(page_title="My Application", layout="wide")

st.title("Gestore Ticket")
st.header("Lista")
st.write("Ticket in attesa.")

# Tabella intera con selezione riga attiva
evento = st.dataframe(
    df,
    use_container_width=True,
    selection_mode="single-row",
    on_select="rerun",
)

# Controllo della riga selezionata
righe_selezionate = evento.selection.rows
if righe_selezionate:
  id_selezionato = df.index[righe_selezionate[0]]
  st.success(f"Ticket selezionato: ID {id_selezionato}")

  if st.button("Modifica ticket selezionato"):
    st.session_state["ticket_id"] = id_selezionato
    st.rerun()
