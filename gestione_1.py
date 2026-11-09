import pandas as pd
import streamlit as st

df = pd.read_csv("dati.csv")
df = df.set_index("ID")

st.set_page_config(page_title="My Application", layout="wide")

st.title("Gestore Ticket")
st.header("Lista")
st.write("Ticket in attesa.")

# Proporzioni fisse per le colonne: ID, Nome, Cognome, Descrizione, Cellulare, email, Azione
col_widths = [1, 2, 2, 4, 2, 3, 1.5]

# 1. Intestazione disegnata una sola volta fuori dal ciclo
header_cols = st.columns(col_widths)
headers = [
    "ID",
    "Nome",
    "Cognome",
    "Descrizione",
    "Cellulare",
    "email",
    "Azione",
]
for col, header in zip(header_cols, headers):
  col.markdown(f"**{header}**")

st.divider()

# 2. Righe con le stesse proporzioni e allineamento verticale centrato
for index, row in df.iterrows():
  cols = st.columns(col_widths, vertical_alignment="center")

  cols[0].write(str(index))
  cols[1].write(str(row["Nome"]))
  cols[2].write(str(row["Cognome"]))
  cols[3].write(str(row["Descrizione"]))
  cols[4].write(str(row["Cellulare"]))
  cols[5].write(str(row["email"]))

  if cols[6].button("Modifica", key=f"modifica_{index}"):
    st.session_state["ticket_id"] = index
    st.rerun()
