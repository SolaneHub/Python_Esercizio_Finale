import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import MultipleLocator
import altair as alt

st.set_page_config(page_title="Statistica", layout="wide", initial_sidebar_state="collapsed")

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



