import os
import sys

# Assicuriamo che la radice del progetto sia nel path di ricerca dei moduli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from datetime import datetime

from prefissi import get_prefissi_internazionali, separa_prefisso_e_numero

# =====================================================================
# 1. CONFIGURAZIONE INIZIALE DELLA PAGINA
# =====================================================================
# Impostiamo il titolo della scheda nel browser e il layout "wide" (largo)
# per sfruttare l'intera larghezza dello schermo a disposizione.
st.set_page_config(page_title="Modifica Ticket", layout="wide")

# Polyfill per consentire a Windows (Chrome ed Edge) di visualizzare correttamente
# le emoji delle bandiere nazionali, che altrimenti non sono supportate dal font di sistema Segoe UI Emoji.
st.markdown(
    """
    <style>
    @font-face {
      font-family: 'Twemoji Country Flags';
      unicode-range: U+1F1E6-1F1FF, U+1F3F4, U+E0062-E0063, U+E0065, U+E0067, U+E006C, U+E006E, U+E0073-E0074, U+E0077, U+E007F;
      src: url('https://cdn.jsdelivr.net/npm/country-flag-emoji-polyfill@0.1/dist/TwemojiCountryFlags.woff2') format('woff2');
      font-display: swap;
    }

    /* Applica il font delle bandiere a tutti i componenti inclusi i menu a tendina */
    *, html, body, [class*="css"], [data-baseweb="select"], [data-baseweb="popover"], [data-baseweb="menu"], li, div, span, input, select {
      font-family: 'Twemoji Country Flags', 'Source Sans Pro', sans-serif;
    }

    /* Blocca categoricamente qualsiasi rotazione o animazione sul pulsante help/tooltip (?) */
    button[aria-label*="Help"],
    button[aria-label*="Help"] svg,
    button[data-testid="stTooltipHoverTarget"],
    button[data-testid="stTooltipHoverTarget"] svg {
      transform: none !important;
      transition: none !important;
    }

    /* Freccia del selectbox: puntatore e transizione fluida */
    button[aria-label="Open"] {
      cursor: pointer !important;
    }
    button[aria-label="Open"] svg {
      transition: transform 0.25s ease-in-out !important;
      transform-origin: center center !important;
      pointer-events: none !important;
    }

    /* Rotazione della SOLA freccia (Open) quando il campo riceve focus, è attivo o si apre il menu */
    button[aria-label="Open"][aria-expanded="true"] svg,
    button[aria-label="Open"][data-pressed="true"] svg,
    :has(input[role="combobox"]:focus) button[aria-label="Open"] svg,
    :has(input[role="combobox"][data-focused="true"]) button[aria-label="Open"] svg,
    :has(input[role="combobox"][aria-expanded="true"]) button[aria-label="Open"] svg,
    div[data-testid="stSelectbox"]:focus-within button[aria-label="Open"] svg,
    div[data-testid="stSelectbox"]:has(input[data-focused="true"]) button[aria-label="Open"] svg,
    div[data-testid="stSelectbox"]:has(input[aria-expanded="true"]) button[aria-label="Open"] svg,
    input[role="combobox"]:focus ~ button[aria-label="Open"] svg,
    input[role="combobox"][data-focused="true"] ~ button[aria-label="Open"] svg,
    input[role="combobox"][aria-expanded="true"] ~ button[aria-label="Open"] svg {
      transform: rotate(180deg) !important;
    }

    /* Nasconde completamente il banner con le istruzioni native di Streamlit (Press Ctrl+Enter / 256/256) */
    div[data-testid="InputInstructions"] {
      display: none !important;
    }

    /* Blocca l'altezza della textarea impedendo il ridimensionamento manuale e fa spazio al contatore interno */
    div[data-testid="stTextArea"] textarea,
    .st-key-descrizione_ticket textarea {
      resize: none !important;
      height: 290px !important;
      max-height: 290px !important;
      min-height: 290px !important;
      padding-bottom: 28px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Garantisce che il click sulla freccia apra il menu e posiziona il contatore DENTRO al campo in basso a destra
components.html(
    """
    <script>
    const parentDoc = window.parent.document;

    // Gestione click sulla freccia del selectbox
    parentDoc.addEventListener('pointerdown', function(e) {
        const btn = e.target.closest('button[aria-label="Open"]');
        if (btn) {
            const box = btn.closest('[data-testid="stSelectbox"]');
            const inp = box ? box.querySelector('input[role="combobox"]') : null;
            if (inp) {
                inp.focus();
            }
        }
    }, true);

    parentDoc.addEventListener('click', function(e) {
        const btn = e.target.closest('button[aria-label="Open"]');
        if (btn) {
            const box = btn.closest('[data-testid="stSelectbox"]');
            const inp = box ? box.querySelector('input[role="combobox"]') : null;
            if (inp) {
                inp.focus();
                inp.click();
            }
        }
    }, true);

    // Contatore dinamico posizionato DENTRO alla textarea in basso a destra con gradiente progressivo
    function setupCharCounter() {
        const textarea = parentDoc.querySelector('.st-key-descrizione_ticket textarea') || parentDoc.querySelector('[data-testid="stTextArea"] textarea');
        if (!textarea) return;

        // Box contenitore diretto della textarea
        const textWrapper = textarea.parentElement;
        if (!textWrapper) return;

        // Rimuove eventuale vecchio contatore esterno
        const outerContainer = textarea.closest('[data-testid="stTextArea"]');
        if (outerContainer) {
            const oldExternalCounter = outerContainer.querySelector(':scope > #char-counter-feedback');
            if (oldExternalCounter) oldExternalCounter.remove();
        }

        textWrapper.style.position = 'relative';

        let counter = textWrapper.querySelector('#char-counter-feedback');
        if (!counter) {
            counter = parentDoc.createElement('div');
            counter.id = 'char-counter-feedback';
            counter.style.cssText = 'position: absolute; bottom: 8px; right: 12px; z-index: 5; pointer-events: none; font-size: 0.82rem; font-family: monospace, sans-serif; font-weight: 700; user-select: none; display: flex; align-items: center;';
            counter.innerHTML = '<span id="char-counter-num" style="transition: color 0.15s ease;">0</span><span style="color: #94a3b8; font-weight: 600;">&nbsp;/ 256</span>';
            textWrapper.appendChild(counter);
        }

        const numSpan = counter.querySelector('#char-counter-num');

        function updateCounter() {
            const max = 256;
            const len = textarea.value.length;
            const ratio = Math.min(len / max, 1);
            // Calcolo del colore: da 120° (verde) a 0° (rosso) in modo progressivo
            const hue = Math.round(120 * (1 - ratio));
            numSpan.textContent = len;
            numSpan.style.color = `hsl(${hue}, 92%, 40%)`;
        }

        if (!textarea.dataset.hasCounterListener) {
            textarea.addEventListener('input', updateCounter);
            textarea.addEventListener('keyup', updateCounter);
            textarea.addEventListener('paste', () => setTimeout(updateCounter, 30));
            textarea.dataset.hasCounterListener = 'true';
        }

        updateCounter();
    }

    setupCharCounter();
    setInterval(setupCharCounter, 600);
    </script>
    """,
    height=0,
    width=0,
)

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
    st.switch_page("gestione.py")
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
    # Campi anagrafici e di contatto in ordine: Nome, Cognome, Email, Numero di Telefono
    nuovo_nome = st.text_input("Nome:", value=str(riga["Nome"]))
    nuovo_cognome = st.text_input("Cognome:", value=str(riga["Cognome"]))
    nuova_email = st.text_input("Contatto e-mail:", value=str(riga["email"]))

    # Separiamo il prefisso e il numero dal contatto memorizzato
    prefisso_attuale, numero_pulito = separa_prefisso_e_numero(riga["Cellulare"])

    # Carichiamo la lista completa di tutti i prefissi mondiali ordinati in ordine numerico crescente
    lista_prefissi = get_prefissi_internazionali()

    # Identifichiamo l'indice predefinito corrispondente al prefisso salvato (preferenza a Italia se +39)
    idx_default = 0
    for idx, voce in enumerate(lista_prefissi):
      if voce.startswith(f"{prefisso_attuale} "):
        if prefisso_attuale == "+39" and "Italia" in voce:
          idx_default = idx
          break
        elif idx_default == 0:
          idx_default = idx

    # Creiamo due sotto-colonne per prefisso internazionale e numero cellulare
    col_prefisso, col_numero = st.columns([1.8, 2.2])
    with col_prefisso:
      prefisso_selezionato = st.selectbox(
          "Prefisso:",
          options=lista_prefissi,
          index=idx_default,
          help="Seleziona il prefisso internazionale con bandiera dello stato",
      )
    with col_numero:
      nuovo_cellulare = st.text_input(
          "Contatto cellulare:", value=numero_pulito
      )

  with col2:
    # A destra posizioniamo la descrizione del problema, allineata perfettamente al fondo di prefisso e cellulare
    nuova_descrizione = st.text_area(
        "Descrizione problema:",
        value=str(riga["Descrizione"]),
        height=290,
        max_chars=256,
        key="descrizione_ticket",
    )
    nuova_data = st.date_input(
    "Seleziona una data",
    value= datetime.strptime(riga["Data"], "%Y-%m-%d"),
    format="DD/MM/YYYY",
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
    # Estraiamo il codice prefisso (es. '+39' da '+39 🇮🇹 Italia') e ricombiniamo con il numero
    codice_prefisso = prefisso_selezionato.split()[0]
    num_pulito_str = str(nuovo_cellulare).strip()
    cellulare_completo = f"{codice_prefisso}{num_pulito_str}" if num_pulito_str else ""

    df.loc[id_selezionato, "Nome"] = nuovo_nome
    df.loc[id_selezionato, "Cognome"] = nuovo_cognome
    df.loc[id_selezionato, "Cellulare"] = cellulare_completo
    df.loc[id_selezionato, "email"] = nuova_email
    df.loc[id_selezionato, "Descrizione"] = nuova_descrizione
    df.loc[id_selezionato, "Data"] = nuova_data

    # C. Salvataggio su file:
    # `reset_index()` riporta l'indice (ID) a normale colonna tabellare prima di esportare in CSV.
    df.reset_index().to_csv("dati.csv", index=False)

    # D. Aggiornamento dello stato in memoria:
    # Aggiorniamo anche la riga salvata nel session_state con i nuovi valori appena scritti,
    # garantendo coerenza immediata se la pagina viene ricaricata o consultata di nuovo.
    st.session_state["riga_selezionata"] = df.loc[id_selezionato]

    st.success("Modifiche salvate con successo nel database!")
