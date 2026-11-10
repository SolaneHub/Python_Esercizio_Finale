import pandas as pd
import streamlit as st

# =====================================================================
# 1. CONFIGURAZIONE INIZIALE DELLA PAGINA
# =====================================================================
# Impostiamo il titolo della scheda nel browser e il layout "wide" (largo)
# per sfruttare l'intera larghezza dello schermo a disposizione.
st.set_page_config(page_title="Modifica Ticket", layout="wide")

st.title("Modifica Ticket")

# =====================================================================
# 2. CONTROLLO DI SICUREZZA E VALIDAZIONE DELLO STATO (SESSION STATE)
# =====================================================================
# Logica di protezione: verifichiamo se l'utente è arrivato qui dopo aver
# selezionato correttamente un ticket nella pagina principale (main.py).
# Se la chiave "riga_selezionata" non esiste, significa che la pagina
# è stata aperta direttamente via URL. Interrompiamo l'esecuzione per evitare crash.
if "riga_selezionata" not in st.session_state:
  st.warning(
      "Nessun ticket selezionato. Torna alla home e seleziona una riga."
  )
  if st.button("Torna alla Home"):
    st.switch_page("main.py")
  st.stop()  # Ferma lo script qui impedendo l'esecuzione del resto della pagina

# =====================================================================
# 3. ESTRAZIONE DEI DATI DALLO SESSION STATE
# =====================================================================
# Preleviamo l'intera riga del DataFrame (un oggetto di tipo pandas.Series)
# salvata in precedenza nel dizionario globale st.session_state.
riga = st.session_state["riga_selezionata"]

# Sfruttiamo la proprietà .name dell'oggetto Series, che in Pandas corrisponde
# esattamente all'indice della riga (nel nostro caso, l'ID univoco del ticket).
# Questo evita di dover cercare l'ID manualmente tramite indici numerici instabili.
id_selezionato = riga.name

st.info(f"Stai modificando il ticket con ID: **{id_selezionato}**")

# =====================================================================
# 4. CREAZIONE DEL FORM UNIVOCO (ST.FORM)
# =====================================================================
# Utilizziamo st.form per raggruppare tutti i campi di input in un blocco logico.
# Logica dietro le quinte: Streamlit, per natura, riesegue l'intero script a ogni interazione.
# L'uso di st.form blocca questo comportamento continuo, permettendo all'utente
# di digitare in tutti i campi senza ricaricamenti di pagina indesiderati fino al click sul pulsante finale.
with st.form("form_modifica_ticket"):
  st.subheader("Dati del Ticket")

  # Dividiamo l'interfaccia in due colonne parallele per un layout ordinato ed ergonomico
  col1, col2 = st.columns(2)

  with col1:
    # Pre-popoliamo i campi di input passando il parametro `value`.
    # Convertiamo sempre in stringa (`str(...)`) per evitare errori di tipo se il DataFrame contiene NaN o numeri.
    nuovo_nome = st.text_input("Nome:", value=str(riga["Nome"]))
    nuovo_cognome = st.text_input("Cognome:", value=str(riga["Cognome"]))
    nuovo_cellulare = st.text_input(
        "Contatto cellulare:", value=str(riga["Cellulare"])
    )

  with col2:
    nuova_email = st.text_input(
        "Contatto e-mail:", value=str(riga["email"])
    )
    # st.text_area viene usato al posto di text_input per gestire descrizioni lunghe multilinea
    nuova_descrizione = st.text_area(
        "Descrizione problema:", value=str(riga["Descrizione"])
    )

  # =====================================================================
  # 5. GESTIONE DELL'INVIO (SUBMIT) E AGGIORNAMENTO PERSISTENTE (CSV)
  # =====================================================================
  # Il pulsante di invio del form attiva il blocco condizionale sottostante
  # esclusivamente quando l'utente decide di confermare cliccando su "Salva Modifiche".
  submit_modifica = st.form_submit_button(
      "Salva Modifiche", width='stretch'
  )

  if submit_modifica:
    # A. Ricarichiamo il database CSV fresco dal disco per evitare conflitti o dati obsoleti
    df = pd.read_csv("dati.csv", dtype={'Cellulare': 'str'}) #Cellulare salvato come string per compatibilità
    df = df.set_index("ID")

    # B. Aggiorniamo le celle mirate del DataFrame sfruttando l'ID come chiave di ricerca riga (.loc)
    df.loc[id_selezionato, "Nome"] = nuovo_nome
    df.loc[id_selezionato, "Cognome"] = nuovo_cognome
    df.loc[id_selezionato, "Cellulare"] = str(nuovo_cellulare) # un'altra conversione str per evitare incompatibilità
    df.loc[id_selezionato, "email"] = nuova_email
    df.loc[id_selezionato, "Descrizione"] = nuova_descrizione

    # C. Salvataggio su file:
    # `reset_index()` riporta l'indice (ID) a normale colonna tabellare prima di esportare in CSV.
    df.reset_index().to_csv("dati.csv", index=False)

    # D. Aggiornamento dello stato in memoria:
    # Aggiorniamo anche la riga salvata nel session_state con i nuovi valori appena scritti,
    # garantendo coerenza immediata se la pagina viene ricaricata o consultata di nuovo.
    st.session_state["riga_selezionata"] = df.loc[id_selezionato]

    st.success("Modifiche salvate con successo nel databasee!")
    