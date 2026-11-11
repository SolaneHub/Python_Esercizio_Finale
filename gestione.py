import pandas as pd
import streamlit as st

def EliminaTicket(df, id_selezionati):
  for id in id_selezionati:
    df = df.drop(index=id)
    df.reset_index().to_csv("dati.csv", index=False)

@st.dialog("Conferma elimina")
def PopupElimina(df, id_selezionati):
    st.write(f"Vuoi eliminare {id_selezionati.tolist()}?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Annulla"):
            st.rerun()
    with col2:
        if st.button("Sì"):
            EliminaTicket(df, id_selezionati)
            st.rerun()

#Nel caricamento del df, Cellulare va salvato come string per evitare problemi di incompatibilità
df = pd.read_csv("dati.csv", dtype={'Cellulare': 'str'})
df = df.set_index("ID")

#configurazione pagina
st.set_page_config(page_title="Home", layout="wide", initial_sidebar_state="collapsed")

st.title("Gestore Ticket")
st.header("Lista ticket in attesa")

if st.button("Crea Ticket"):
  st.switch_page("pages/crea_ticket.py")

# Tabella intera con selezione riga attiva
#"evento" è l'oggetto che contiene le informazioni di interazione con la tabella
evento = st.dataframe(
    df,
    width="stretch", #utilizza tutta la larghezza disponibile
    selection_mode="multi-row", #seleziona più righe
    on_select="rerun", #"rerun": quando selezioni una riga riesegue lo script e aggiorna l'evento
)

# Controlla se righe sono selezionate
selezioni = evento.selection.rows

# Se righe sono selezionate, compare pulsante modifica
if selezioni:
  #stampa ID selezionato
  id_selezionati = df.index[selezioni]
  st.success(f"Ticket selezionati: ID {id_selezionati.tolist()}")

  #passaggio riga da modificare tramite session_state
  riga_selezionata = df.loc[id_selezionati[0]]
  st.session_state["riga_selezionata"] = riga_selezionata

  #colonne per tasti. size per ognuno in []
  col1, col2, col3 = st.columns([1,2,5])

  #elimina
  with col1:
    if st.button("🗑"):
      PopupElimina(df, id_selezionati)
  #modifica
  with col2:
    if len(selezioni) == 1 and st.button("Modifica Ticket"):
      st.switch_page("pages/modifica_ticket.py")
  #spazio vuoto
  with col3:
    pass

