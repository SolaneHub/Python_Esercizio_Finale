import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import MultipleLocator
import altair as alt
import base64 #importo file in html

st.set_page_config(page_title="Statistica", layout="wide", initial_sidebar_state="collapsed")

#Caricamento immagini per HTML
def get_image_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
logo_base64 = get_image_base64("pages/assets/logo.png")

# STILE BARRA TITOLO
st.markdown("""
<style>
    /* Force Orbitron globally across all text, markdown, and headers */
    html, body, [class*="css"] {
        font-family: 'Orbitron', sans-serif !important;
    }
    /* Ensure headers also use the font */
    h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', sans-serif !important;
    }

    .stMainBlockContainer {
        padding-top: 0 !important;
    }

    .titlebar {
        position: relative;
        left: 50%;
        width: 100vw;
        transform: translateX(-50%);
        box-sizing: border-box;

        background-color: #1E3A5F;
        color: white;

        margin-top: 40px;
        margin-bottom: 30px;
    }

    /* Make the link take over the flex layout and strip default anchor underlines */
    .titlebar-link {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 20px 30px;
        color: white;
        text-decoration: none;
    }

    .titlebar-link {
        color: white;
        text-decoration: none;
    }

    .titlebar img {
        width: 50px;
        height: 50px;
        object-fit: contain;
    }

    .titlebar h1 {
        color: white;
        margin: 0;
        padding: 0;
        padding-top: 8px;
        font-size: 48px;
        text-decoration: none !important;
    }
</style>
""", unsafe_allow_html=True)

#BARRA TITOLO
st.markdown(f"""
<div class="titlebar">
    <a href="/" class="titlebar-link">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
        <h1>Help Desk Manager</h1>
    </a>
</div>
""", unsafe_allow_html=True)


st.title("Analisi gestione dati")
st.header("Conteggio ticket per utente")

try:
    df = pd.read_csv("dati.csv", dtype={"Cellulare": "str"})
    

    # Conversione date
    df["Data"] = pd.to_datetime(
        df["Data"],
        format="%Y-%m-%d",
        errors="coerce"
    )

    df = df.dropna(subset=["Data"])

    st.title("Andamento segnalazioni")

    periodo = st.selectbox(
        "Seleziona periodo",
        ["Mensile", "Annuale"]
    )

    match periodo:
        case "Mensile":
            anni = sorted(df["Data"].dt.year.unique())
            anno = st.selectbox("Anno", anni)

            filtered = df[df["Data"].dt.year == anno].copy()

            plot_data = (
                filtered
                .groupby(filtered["Data"].dt.month)
                .size()
                .reindex(range(1, 13), fill_value=0)
                .rename_axis("Mese")
                .reset_index(name="Totale")
            )

            mesi = {
                1: "Gennaio", 2: "Febbraio", 3: "Marzo",
                4: "Aprile", 5: "Maggio", 6: "Giugno",
                7: "Luglio", 8: "Agosto", 9: "Settembre",
                10: "Ottobre", 11: "Novembre", 12: "Dicembre"
            }

            plot_data["Periodo"] = plot_data["Mese"].map(mesi)
            ordine = list(mesi.values())

        case "Annuale":
            plot_data = (
                df.groupby(df["Data"].dt.year)
                .size()
                .reset_index(name="Totale")
            )

            plot_data.columns = ["Periodo", "Totale"]
            plot_data["Periodo"] = plot_data["Periodo"].astype(str)
            ordine = sorted(plot_data["Periodo"].tolist())

    # Grafico Altair
    chart = (
    alt.Chart(plot_data)
    .mark_line(
        color="#4F8BF9",
        strokeWidth=3,
        point=alt.OverlayMarkDef(
            filled=True,
            size=90,
            color="#4F8BF9"
        )
    )
    .encode(
        x=alt.X(
            "Periodo:N",
            sort=ordine,
            title="Periodo",
            axis=alt.Axis(labelAngle=0)
        ),
        y=alt.Y(
            "Totale:Q",
            title="Numero segnalazioni",
            scale=alt.Scale(domainMin=0)
        ),
        tooltip=[
            alt.Tooltip("Periodo:N"),
            alt.Tooltip("Totale:Q")
        ]
    )
    .properties(
        height=350
    )
)

    st.altair_chart(
        chart,
        use_container_width=True
    )

    # Debug: verifica dati
    with st.expander("Visualizza dati del grafico"):
        st.dataframe(plot_data)



    ###############################à

    df["Utente"] = (
        df["Nome"].fillna("").astype(str)
        + " "
        + df["Cognome"].fillna("").astype(str)
    )
    df["Utente"] = df["Utente"].str.strip()

    df_riepilogo = (
    df["Utente"]
    .value_counts()
    .reset_index()
    )  

    df_riepilogo.columns = ["Utente", "Numero Ticket"]

    df_riepilogo = df_riepilogo.sort_values(
        by=["Numero Ticket", "Utente"],
        ascending=[False, True]
    ).reset_index(drop=True)


    #RIEPILOGO
    st.markdown("### 📝 Riepilogo Ticket")
    st.dataframe(df_riepilogo, width='stretch', hide_index=True)



except FileNotFoundError:
    st.error(
        "⚠️ Il file 'dati.csv' non è stato trovato nella cartella del progetto."
    )



