"""Entrypoint e interfaccia Home per il Centro Assistenza Informatica."""

from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

# Polyfill per il supporto delle emoji delle bandiere e rotazione frecce
FLAG_EMOJI_CSS = """
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
button[aria-label*="Help"],
button[aria-label*="Help"] svg,
button[data-testid="stTooltipHoverTarget"],
button[data-testid="stTooltipHoverTarget"] svg {
  transform: none !important;
  transition: none !important;
}
button[aria-label="Open"] {
  cursor: pointer !important;
}
button[aria-label="Open"] svg {
  transition: transform 0.25s ease-in-out !important;
  transform-origin: center center !important;
  pointer-events: none !important;
}
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
"""


def EliminaTicket(df: pd.DataFrame, id_selezionati: list[Any]) -> None:
    """Elimina i ticket selezionati e aggiorna dati.csv."""
    for id_val in id_selezionati:
        if id_val in df.index:
            df = df.drop(index=id_val)
    df.reset_index().to_csv("dati.csv", index=False)


@st.dialog("Conferma eliminazione ticket")
def PopupElimina(df: pd.DataFrame, id_selezionati: list[Any]) -> None:
    """Mostra il popup di conferma eliminazione per i ticket selezionati."""
    n_ticket = len(id_selezionati)
    if n_ticket == 1:
        st.warning(
            f"Sei sicuro di voler eliminare il ticket **ID #{id_selezionati[0]}**?"
        )
    else:
        st.warning(
            f"Sei sicuro di voler eliminare i **{n_ticket} ticket** selezionati?\n\n"
            f"ID interessati: `{', '.join(map(str, id_selezionati))}`"
        )
    st.caption(
        "⚠️ Questa azione è irreversibile. I dati verranno rimossi definitivamente."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Annulla", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("Sì, Elimina", type="primary", use_container_width=True):
            EliminaTicket(df, id_selezionati)
            st.session_state.pop("riga_selezionata", None)
            st.rerun()


def _formatta_data_italiana(data_str: Any) -> str:
    """Formatta una data YYYY-MM-DD in formato italiano DD/MM/YYYY."""
    if not data_str or pd.isna(data_str):
        return "N/D"
    val = str(data_str).strip()
    parti = val.split("-")
    if len(parti) == 3 and len(parti[0]) == 4:
        return f"{parti[2]}/{parti[1]}/{parti[0]}"
    return val


def main() -> None:
    """Funzione principale per il rendering della Home."""
    st.set_page_config(
        page_title="Home - Gestore Ticket",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(FLAG_EMOJI_CSS, unsafe_allow_html=True)

    # Caricamento del dataset
    dati_path = Path("dati.csv")
    if dati_path.exists():
        df = pd.read_csv(dati_path, dtype={"Cellulare": "str"})
        if "ID" in df.columns:
            df = df.set_index("ID")
    else:
        df = pd.DataFrame(
            columns=["Nome", "Cognome", "Descrizione", "Cellulare", "email", "Data"]
        )
        df.index.name = "ID"

    # 1. Header Hero con azioni principali allineate
    col_title, col_actions = st.columns([3, 1.3], vertical_alignment="center")
    with col_title:
        st.title("📋 Gestore Ticket")
        st.caption("Centro Assistenza Informatica • Monitoraggio e gestione pratiche")

    with col_actions:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button(
                "➕ Nuovo",
                type="primary",
                use_container_width=True,
                help="Crea un nuovo ticket di assistenza",
            ):
                st.switch_page("pages/crea_ticket.py")
        with btn_col2:
            if st.button(
                "📊 Report",
                use_container_width=True,
                help="Visualizza statistiche e grafici",
            ):
                st.switch_page("pages/analisi_ticket.py")

    if df.empty:
        st.info("Nessun ticket presente nel database. Clicca su 'Nuovo' per iniziare!")
        return

    # 2. Toolbar compatta per Ricerca e Ordinamento
    with st.container(border=True):
        col_search, col_sort, col_reset = st.columns(
            [4.5, 3.5, 2], vertical_alignment="center"
        )
        with col_search:
            cerca = st.text_input(
                "Cerca nei ticket",
                placeholder="🔍 Cerca cliente, telefono, email, guasto o ID...",
                label_visibility="collapsed",
                key="filtro_ricerca_home",
            )
        with col_sort:
            ordinamento = st.selectbox(
                "Ordinamento",
                options=[
                    "ID Decrescente (Nuovi prima)",
                    "ID Crescente (Meno recenti)",
                    "Data (Più recente prima)",
                    "Data (Meno recente prima)",
                    "Cliente (A-Z)",
                ],
                label_visibility="collapsed",
                key="selettore_ordinamento_home",
            )

    # 3. Filtraggio e Ordinamento del DataFrame
    df_visualizzato = df.copy()
    cerca_pulito = cerca.strip() if cerca else ""

    if cerca_pulito:
        nome_completo = (
            df_visualizzato["Nome"].fillna("")
            + " "
            + df_visualizzato["Cognome"].fillna("")
        )
        maschera = (
            df_visualizzato["Nome"].str.contains(
                cerca_pulito, case=False, na=False, regex=False
            )
            | df_visualizzato["Cognome"].str.contains(
                cerca_pulito, case=False, na=False, regex=False
            )
            | nome_completo.str.contains(
                cerca_pulito, case=False, na=False, regex=False
            )
            | df_visualizzato["Cellulare"].str.contains(
                cerca_pulito, case=False, na=False, regex=False
            )
            | df_visualizzato["email"].str.contains(
                cerca_pulito, case=False, na=False, regex=False
            )
            | df_visualizzato["Descrizione"].str.contains(
                cerca_pulito, case=False, na=False, regex=False
            )
            | df_visualizzato.index.astype(str).str.contains(
                cerca_pulito, case=False, na=False, regex=False
            )
        )
        df_visualizzato = df_visualizzato[maschera]

    if ordinamento == "ID Decrescente (Nuovi prima)":
        df_visualizzato = df_visualizzato.sort_index(ascending=False)
    elif ordinamento == "ID Crescente (Meno recenti)":
        df_visualizzato = df_visualizzato.sort_index(ascending=True)
    elif ordinamento == "Data (Più recente prima)":
        df_visualizzato = df_visualizzato.sort_values(by="Data", ascending=False)
    elif ordinamento == "Data (Meno recente prima)":
        df_visualizzato = df_visualizzato.sort_values(by="Data", ascending=True)
    elif ordinamento == "Cliente (A-Z)":
        df_visualizzato = df_visualizzato.sort_values(
            by=["Cognome", "Nome"], ascending=True
        )

    with col_reset:
        totale_totali = len(df)
        totale_filtrati = len(df_visualizzato)
        if cerca_pulito:
            st.markdown(
                f"<div style='text-align: right; color: #8899a6; font-size: 0.85rem;'>"
                f"Trovati: <b>{totale_filtrati}</b>/{totale_totali}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='text-align: right; color: #8899a6; font-size: 0.85rem;'>"
                f"Totale: <b>{totale_totali}</b> pratiche</div>",
                unsafe_allow_html=True,
            )

    # 4. Schede KPI di riepilogo
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.metric(
            label="Totale Ticket",
            value=len(df),
            help="Numero complessivo di pratiche registrate nel database",
            border=True,
        )
    with kpi_col2:
        clienti_unici = (
            df[["Nome", "Cognome"]].drop_duplicates().shape[0] if not df.empty else 0
        )
        st.metric(
            label="Clienti Unici",
            value=clienti_unici,
            help="Numero di clienti distinti serviti dal laboratorio",
            border=True,
        )
    with kpi_col3:
        ultimo_id = int(df.index.max()) if not df.empty else None
        ultima_data_str = (
            df.loc[ultimo_id, "Data"]
            if (ultimo_id is not None and ultimo_id in df.index)
            else "N/D"
        )
        st.metric(
            label="Ultimo Ticket",
            value=f"#{ultimo_id}" if ultimo_id else "N/D",
            delta=_formatta_data_italiana(ultima_data_str) if ultimo_id else None,
            help="Ultimo ticket registrato nel gestionale",
            border=True,
        )

    # Container per la barra delle azioni contestuali (sopra la tabella)
    top_action_placeholder = st.container()

    if df_visualizzato.empty:
        with kpi_col4:
            st.metric(
                label="Selezione",
                value="Nessuna",
                help="Nessun ticket selezionato",
                border=True,
            )
        st.warning(f"Nessun ticket trovato con i criteri di ricerca: '{cerca_pulito}'")
        return

    # 5. Configurazione delle colonne e visualizzazione tabella interattiva
    column_config = {
        "ID": st.column_config.NumberColumn(
            "ID",
            format="%d",
            help="Identificativo univoco pratica",
            width="small",
        ),
        "Nome": st.column_config.TextColumn(
            "Nome",
            help="Nome cliente",
            width="medium",
        ),
        "Cognome": st.column_config.TextColumn(
            "Cognome",
            help="Cognome cliente",
            width="medium",
        ),
        "Descrizione": st.column_config.TextColumn(
            "Descrizione Guasto",
            help="Descrizione del malfunzionamento riscontrato",
            width="large",
        ),
        "Cellulare": st.column_config.TextColumn(
            "Telefono",
            help="Recapito telefonico con prefisso internazionale",
            width="medium",
        ),
        "email": st.column_config.TextColumn(
            "Email",
            help="Indirizzo email di contatto",
            width="medium",
        ),
        "Data": st.column_config.DateColumn(
            "Data",
            format="DD/MM/YYYY",
            help="Data di accettazione del ticket",
            width="small",
        ),
    }

    evento = st.dataframe(
        df_visualizzato,
        width="stretch",
        height=400,
        selection_mode="multi-row",
        on_select="rerun",
        column_config=column_config,
        key="home_tickets_table",
    )

    selezioni = evento.selection.rows
    n_selezionati = len(selezioni)

    with kpi_col4:
        st.metric(
            label="Selezione",
            value=(
                f"{n_selezionati} attiv{'o' if n_selezionati == 1 else 'i'}"
                if n_selezionati > 0
                else "Nessuna"
            ),
            delta="Pronto per azioni" if n_selezionati > 0 else "Clicca una riga",
            help="Numero di ticket correntemente selezionati per modifiche o eliminazione",
            border=True,
        )

    # 6. Azioni contestuali quando ci sono righe selezionate
    if selezioni:
        id_selezionati = df_visualizzato.index[selezioni].tolist()
        riga_selezionata = df_visualizzato.loc[id_selezionati[0]]
        st.session_state["riga_selezionata"] = riga_selezionata

        # Barra di azione superiore (immediatamente visibile sopra la tabella)
        with top_action_placeholder, st.container(border=True):
            if n_selezionati == 1:
                col_info, col_mod, col_del = st.columns(
                    [5.5, 2.2, 2.3], vertical_alignment="center"
                )
                with col_info:
                    nome_cli = (
                        f"{riga_selezionata['Nome']} {riga_selezionata['Cognome']}"
                    )
                    data_cli = _formatta_data_italiana(riga_selezionata.get("Data", ""))
                    st.markdown(
                        f"🎯 **Ticket #{id_selezionati[0]}** — "
                        f"**{nome_cli}** &nbsp;•&nbsp; 📅 `{data_cli}`"
                    )
                with col_mod:
                    if st.button(
                        "✏️ Modifica Ticket",
                        type="primary",
                        use_container_width=True,
                        key="top_btn_modifica",
                    ):
                        st.switch_page("pages/modifica_ticket.py")
                with col_del:
                    if st.button(
                        "🗑️ Elimina Ticket",
                        use_container_width=True,
                        key="top_btn_elimina",
                    ):
                        PopupElimina(df, id_selezionati)
            else:
                col_info, col_del = st.columns([7, 3], vertical_alignment="center")
                with col_info:
                    elenco_id = ", ".join(map(str, id_selezionati))
                    st.markdown(
                        f"📌 **{n_selezionati} Ticket selezionati:** "
                        f"ID `{elenco_id}` "
                        f"<span style='color: #8899a6; font-size: 0.85rem;'>"
                        f"(seleziona una sola riga per abilitare la modifica)</span>",
                        unsafe_allow_html=True,
                    )
                with col_del:
                    if st.button(
                        f"🗑️ Elimina {n_selezionati} Ticket",
                        type="primary",
                        use_container_width=True,
                        key="top_btn_elimina_multi",
                    ):
                        PopupElimina(df, id_selezionati)

        # Scheda Dettagli Rapidi sotto la tabella (quando è selezionato un singolo ticket)
        if n_selezionati == 1:
            with st.container(border=True):
                col_d_title, col_d_btns = st.columns(
                    [3, 1.2], vertical_alignment="center"
                )
                with col_d_title:
                    st.markdown(f"### 📋 Scheda Rapida: Ticket #{id_selezionati[0]}")
                with col_d_btns:
                    sub_col1, sub_col2 = st.columns(2)
                    with sub_col1:
                        if st.button(
                            "✏️ Modifica",
                            use_container_width=True,
                            key="bottom_btn_modifica",
                        ):
                            st.switch_page("pages/modifica_ticket.py")
                    with sub_col2:
                        if st.button(
                            "🗑️ Elimina",
                            use_container_width=True,
                            key="bottom_btn_elimina",
                        ):
                            PopupElimina(df, id_selezionati)

                d_col1, d_col2, d_col3 = st.columns(3)
                with d_col1:
                    cli_nome = riga_selezionata["Nome"]
                    cli_cogn = riga_selezionata["Cognome"]
                    st.markdown(f"**👤 Cliente:** {cli_nome} {cli_cogn}")
                with d_col2:
                    tel = riga_selezionata.get("Cellulare", "")
                    st.markdown(f"**📞 Telefono:** `{tel if tel else 'N/D'}`")
                with d_col3:
                    em = riga_selezionata.get("email", "")
                    dt_fmt = _formatta_data_italiana(riga_selezionata.get("Data", ""))
                    st.markdown(
                        f"**✉️ Email:** `{em if em else 'N/D'}` &nbsp;|&nbsp; "
                        f"**📅 Data:** `{dt_fmt}`"
                    )

                st.markdown("**📝 Descrizione del Guasto:**")
                desc = riga_selezionata.get("Descrizione", "")
                st.info(
                    desc
                    if desc
                    else "Nessuna descrizione specificata per questo ticket."
                )


if __name__ == "__main__":
    main()
