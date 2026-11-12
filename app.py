import streamlit as st

# Configurazione applicazione
st.set_page_config(
    page_title="Home - Gestore Ticket",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="pages/assets/logo.png"
)

# Logo
st.logo(
    image="pages/assets/logo.png",
    icon_image="pages/assets/logo.png",
    size="large"
)

# Definizione pagine
pagina_gestione = st.Page(
    "gestione.py",
    title="Gestione",
    icon=":material/dashboard:",
    default=True
)

pagina_analisi = st.Page(
    "pages/analisi_ticket.py",
    title="Analisi Ticket",
    icon=":material/analytics:"
)

pagina_crea = st.Page(
    "pages/crea_ticket.py",
    title="Crea Ticket",
    icon=":material/add_circle:"
)

pagina_modifica = st.Page(
    "pages/modifica_ticket.py",
    title="Modifica Ticket",
    icon=":material/edit_note:"
)

# Gestione navigazione
pagina = st.navigation([
    pagina_gestione,
    pagina_analisi,
    pagina_crea,
    pagina_modifica
])

# Avvio pagina selezionata
pagina.run()
