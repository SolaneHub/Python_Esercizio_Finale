import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_csv("dati.csv", dtype={'Cellulare': 'str'})
df = df.set_index("ID")

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

    ticket_per_utente = df["Utente"].value_counts()

    col1, col2 = st.columns([1, 1.2], gap="medium")

    with col1:
        st.markdown("### 📝 Riepilogo Ticket")
        df_riepilogo = ticket_per_utente.reset_index()
        df_riepilogo.columns = ["Utente / Cliente", "Numero Ticket"]
        st.dataframe(df_riepilogo, width='stretch', hide_index=True)

    with col2:
        st.markdown("### 📈 Grafico Distribuzione Ticket")

        # Configurazione grafico per Dark Mode / tema scuro
        fig, ax = plt.subplots(figsize=(6, 3.8), facecolor="none")
        ax.set_facecolor("none")

        bars = ax.bar(
            ticket_per_utente.index,
            ticket_per_utente.values,
            color="#4A90E2",
            edgecolor="#555555",
            linewidth=1,
            width=0.45,
        )

        ax.set_ylabel(
            "Numero di Ticket", fontsize=10, fontweight="bold", color="#CCCCCC"
        )
        ax.set_title(
            "Quantità di Ticket per Utente",
            fontsize=12,
            fontweight="bold",
            color="#FFFFFF",
            pad=12,
        )

        ax.tick_params(colors="#CCCCCC", labelsize=9)
        plt.xticks(rotation=25, ha="right")

        ax.grid(axis="y", linestyle="--", alpha=0.2, color="#FFFFFF")
        ax.set_axisbelow(True)

        #spine = bordo del grafico
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["left", "bottom"]:
            ax.spines[spine].set_color("#555555")

        # Etichette dei valori sopra ogni barra
        for bar in bars:
            yval = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                yval + 0.04,
                str(int(yval)),
                ha="center",
                va="bottom",
                color="#FFFFFF",
                fontweight="bold",
                fontsize=9.5,
            )

        plt.tight_layout()
        st.pyplot(fig, width='stretch')

except FileNotFoundError:
    st.error(
        "⚠️ Il file 'dati.csv' non è stato trovato nella cartella del progetto."
    )



