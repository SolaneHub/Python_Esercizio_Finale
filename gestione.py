import pandas as pd
import streamlit as st

#Nel caricamento del df, Cellulare va salvato come string per evitare problemi di incompatibilità
df = pd.read_csv("dati.csv", dtype={'Cellulare': 'str'})
df = df.set_index("ID")

#configurazione pagina
st.set_page_config(page_title="My Application", layout="wide", initial_sidebar_state="collapsed")

st.title("Gestore Ticket")
st.header("Lista")
st.write("Ticket in attesa.")

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
  st.success(f"Ticket selezionati: ID {id_selezionati}")

  #passaggio variabili per la form tramite riga
  
  riga_selezionata = df.loc[id_selezionati[0]]
  st.session_state["riga_selezionata"] = riga_selezionata

  #colonne per tasti. size in x/6
  col1, col2 = st.columns(2)

  #elimina
  with col1:
    if st.button("🗑"):
      pass

  #modifica
  with col2:
    if len(selezioni) == 1:
      if st.button("Modifica Ticket"):
        st.switch_page("pages/modifica_ticket.py")
  

#test righe selezionate
st.write("ID selezionate: ", evento.selection.rows)
  
