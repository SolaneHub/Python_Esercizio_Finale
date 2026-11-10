import pandas as pd
import streamlit as st

st.set_page_config(page_title="app", layout="wide", initial_sidebar_state="collapsed")

st.title("Modifica Ticket")

#accesso a variabile sessione con st.session_state[]
st.write(st.session_state["ID"])

st.write("Nome: ")
st.write("Cognome: ")
st.write("Descrizione problema: ")
st.write("Contatto cellulare: ")
st.write("Contatto e-mail: ")