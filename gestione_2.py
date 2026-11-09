import pandas as pd
import streamlit as st

df = pd.read_csv("dati.csv")
df = df.set_index("ID")

st.set_page_config(page_title="My Application", layout="wide")

st.title("Gestore Ticket")
st.header("Lista")
st.write("Ticket in attesa.")

# Tabella intera con selezione riga attiva

#"evento" è l'oggetto che contiene le informazioni di interazione con la tabella
evento = st.dataframe(
    df,
    use_container_width=True, #utilizza tutta la larghezza disponibile
    selection_mode="single-row", #seleziona una sola riga alla volta
    on_select="rerun", #"rerun": quando selezioni una riga riesegue lo script e aggiorna l'evento
)

# Controlla se righe sono selezionate
righe_selezionate = evento.selection.rows

# Se righe sono selezionate, compare pulsante modifica
if righe_selezionate:
  #stampa ID selezionato
  id_selezionato = df.index[righe_selezionate[0]]
  st.success(f"Ticket selezionato: ID {id_selezionato}")

  #pulsante
  if st.button("Modifica ticket selezionato"):
    st.session_state["ticket_id"] = id_selezionato
    st.switch_page("modifica_ticket.py")
    st.rerun()
