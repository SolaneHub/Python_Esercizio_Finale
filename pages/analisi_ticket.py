import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import MultipleLocator

st.set_page_config(page_title="Statistica", layout="wide", initial_sidebar_state="collapsed")

st.title("Analisi gestione dati")
st.header("Conteggio ticket per utente")

try:
    df = pd.read_csv("dati.csv", dtype={"Cellulare": "str"})

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

    #GRAFICO A BARRE
    st.markdown("### 📈 Grafico Distribuzione Ticket")

    # Configurazione grafico per Dark Mode / tema scuro
    fig, ax = plt.subplots(figsize=(8, 6), facecolor="none")
    ax.set_facecolor("none")
    #dimensione label
    ax.tick_params(axis="both", labelsize=6, colors="#BBBBBB")
    #dimensione x, tick
    ax.set_xlim(left=0, right=5)
    ax.xaxis.set_major_locator(MultipleLocator(1))

    bars = ax.barh(
    df_riepilogo["Utente"],
    df_riepilogo["Numero Ticket"],
    color="#4A90E2",
    edgecolor="#4A90E2",
    height=0.1,
    )

    ax.set_ylabel(
        "Utente", fontsize=10, fontweight="bold", color="#CCCCCC"
    )
    ax.set_title(
        "Numero di Ticket",
        fontsize=12,
        fontweight="bold",
        color="#FFFFFF",
        pad=12,
    )

    ax.grid(axis="y", linestyle="--", alpha=0.2, color="#FFFFFF")
    ax.set_axisbelow(True)

    #spine = bordo del grafico
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#555555")

    plt.tight_layout()
    st.pyplot(fig, width='stretch')

    col1, col2 = st.columns([1,1])
    with col1:
        #RIEPILOGO
        st.markdown("### 📝 Riepilogo Ticket")
        st.dataframe(df_riepilogo, width='stretch', hide_index=True)
    with col2:
        pass


except FileNotFoundError:
    st.error(
        "⚠️ Il file 'dati.csv' non è stato trovato nella cartella del progetto."
    )



