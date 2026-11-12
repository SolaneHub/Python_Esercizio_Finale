# Help Desk Manager 🛠️

**Progetto Finale - Corso Python**

## 📖 Descrizione

**Help Desk Manager (HDM)** è una web application pensata per semplificare e centralizzare la gestione quotidiana di un laboratorio di assistenza tecnica e riparazione di dispositivi elettronici (computer, notebook, smartphone e periferiche).

L'idea alla base è semplice: sostituire i vecchi moduli cartacei e i fogli sparsi con una dashboard digitale intuitiva e reattiva. Il sistema accompagna il personale dall'accoglienza del cliente e presa in carico del dispositivo guasto, fino al tracciamento della lavorazione, alla modifica dei dati e all'analisi dell'andamento degli interventi tramite grafici e metriche riassuntive.

## 🎯 Obiettivi del progetto

Questo progetto è stato realizzato come lavoro finale di gruppo con i seguenti obiettivi:

* **Sviluppo End-to-End:** Progettare e sviluppare un'applicazione gestionale completa unendo logica di business e interfaccia grafica in Python.
* **Web App Multipagina:** Sfruttare le potenzialità di Streamlit per realizzare un'applicazione web moderna, usabile e reattiva.
* **Gestione Dati & Persistenza:** Manipolare e aggiornare i dati tramite Pandas, garantendo la consistenza dei tipi e la persistenza su file CSV locale.
* **User Experience Avanzata:** Progettare un'interfaccia efficiente da bancone con ricerca rapida, scorciatoie d'azione e selettore interattivo di prefissi internazionali (ITU-T) con bandiere.
* **Data Analytics:** Integrare visualizzazioni grafiche con Matplotlib e Altair per monitorare i volumi di lavoro e le tendenze.
* **Collaborazione Git:** Operare su repository Git condiviso tramite branching, pull request e code review.

## ✨ Funzionalità principali

* 📋 **Dashboard & Gestione Ticket (Home):** Tabella interattiva con ordinamento, KPI sintetici e scheda dettagliata del ticket selezionato.
* 🔍 **Ricerca Full-Text Istantanea:** Filtro rapido per ID, nominativo cliente, numero di telefono, email o descrizione del guasto.
* ➕ **Accettazione & Creazione Pratica:** Form guidato con generazione automatica di ID univoco e selezione della data.
* 🌍 **Gestione Recapiti Internazionali:** Selettore di prefisso telefonico mondiale (ITU-T) con ricerca rapida e validazione.
* ✏️ **Modifica & Eliminazione Sicura:** Aggiornamento in tempo reale dei dati delle pratiche e rimozione con conferma.
* 📊 **Analisi & Statistiche:** Visualizzazione grafica delle segnalazioni nel tempo e distribuzione dei ticket per cliente.

## 🛠️ Stack Tecnologico

| Componente | Tecnologia | 
| ----- | ----- | 
| **Web UI & Frontend** | Streamlit (Multi-page Architecture) | 
| **Logica & Data Processing** | Python 3, Pandas | 
| **Visualizzazione Dati** | Matplotlib, Altair | 
| **Persistenza Dati** | CSV (`dati.csv`) | 
| **Styling & Assets** | HTML/CSS Custom, Font Orbitron, Polyfill Twemoji | 

## ▶️ Come avviare il progetto in locale

```bash
# 1. Creare l'ambiente virtuale
python -m venv .venv

# 2. Attivare l'ambiente virtuale
# Su Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Su Linux / macOS:
source .venv/bin/activate

# 3. Installare le dipendenze
pip install -r requirements.txt

# 4. Avviare l'applicazione Streamlit
streamlit run gestione.py
```

L'applicazione sarà accessibile nel browser all'indirizzo `http://localhost:8501`.

## 📋 Ticket di prova

Il file `dati.csv` include già diversi interventi precaricati per il collaudo:

| ID | Cliente | Contatto telefonico | Problema riscontrato | Data | 
| :---: | :--- | :--- | :--- | :---: | 
| `7133` | Sofia Mancini | `+39 5413982250` | Batteria laptop scarica | 02/01/2024 | 
| `7132` | Irene Villa | `+39 9825198266` | PC molto lento | 07/01/2024 | 
| `7263` | Riccardo Conti | `+39 2326416987` | Problemi con Outlook | 24/01/2024 | 
| `7181` | Noemi Caruso | `+39 5099418475` | Disco esterno non riconosciuto | 29/01/2024 | 

## 📁 Struttura del repository

```text
Python_Esercizio_Finale/
├── gestione.py                # Entrypoint applicazione e Dashboard principale (Home)
├── list_view.py               # Vista logica elenco ticket
├── prefissi.py                # Helper per prefissi internazionali ITU-T e bandiere
├── pages/                     # Pagine secondarie Streamlit
│   ├── crea_ticket.py         # Modulo creazione nuova pratica
│   ├── modifica_ticket.py     # Modulo modifica pratica esistente
│   └── analisi_ticket.py      # Modulo statistiche e grafici
├── .streamlit/
│   └── config.toml            # Configurazione tema e palette colori
├── static/fonts/              # Font in utilizzo (Orbitron)
├── dati.csv                   # Dataset / Database locale
├── requirements.txt           # Elenco delle dipendenze Python
└── worklog.txt                # Diario di bordo delle attività svolte
```

## 🤝 Contributors

Le persone che hanno contribuito allo sviluppo di **Help Desk Manager**:

<div align="center">
  <table>
    <tr>
      <td align="center" width="200">
        <a href="https://github.com/daviyume">
          <img src="https://github.com/daviyume.png" width="100px" alt="Davide"/><br />
          <sub><b>Davide</b></sub>
        </a><br />
        <small>💻 Logica dati & Modifiche</small><br /><br />
        <a href="https://github.com/daviyume">
          <img src="https://img.shields.io/badge/GitHub-daviyume-181717?style=for-the-badge&logo=github" alt="Davide GitHub"/>
        </a>
      </td>
      <td align="center" width="200">
        <a href="https://github.com/SolaneHub">
          <img src="https://github.com/SolaneHub.png" width="100px" alt="Solane"/><br />
          <sub><b>Solane</b></sub>
        </a><br />
        <small>🎨 Architettura UI & Form</small><br /><br />
        <a href="https://github.com/SolaneHub">
          <img src="https://img.shields.io/badge/GitHub-SolaneHub-181717?style=for-the-badge&logo=github" alt="Solane GitHub"/>
        </a>
      </td>
      <td align="center" width="200">
        <a href="https://github.com/valescu31-jpg">
          <img src="https://github.com/valescu31-jpg.png" width="100px" alt="Valescu"/><br />
          <sub><b>Valescu</b></sub>
        </a><br />
        <small>📊 Data Analytics & Charts</small><br /><br />
        <a href="https://github.com/valescu31-jpg">
          <img src="https://img.shields.io/badge/GitHub-valescu31--jpg-181717?style=for-the-badge&logo=github" alt="Valescu GitHub"/>
        </a>
      </td>
    </tr>
  </table>
</div>

## 📄 Licenza

Questo progetto è distribuito sotto licenza **MIT License**.