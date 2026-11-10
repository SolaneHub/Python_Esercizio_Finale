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
st.set_page_config(page_title="My Application", layout="wide", initial_sidebar_state="collapsed")

# Supporto rendering bandiere emoji per browser su Windows
st.markdown(
    """
    <style>
    @font-face {
      font-family: 'Twemoji Country Flags';
      unicode-range: U+1F1E6-1F1FF, U+1F3F4, U+E0062-E0063, U+E0065, U+E0067, U+E006C, U+E006E, U+E0073-E0074, U+E0077, U+E007F;
      src: url('https://cdn.jsdelivr.net/npm/country-flag-emoji-polyfill@0.1/dist/TwemojiCountryFlags.woff2') format('woff2');
      font-display: swap;
    }
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
    </style>
    """,
    unsafe_allow_html=True,
)

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
