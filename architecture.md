# Architettura del Sistema: Help Desk Manager 🛠️

Questo documento descrive in modo chiaro e accessibile la struttura, il funzionamento e le regole principali dell'applicazione **Help Desk Manager (HDM)**.

---

## 1. 5-Minute Mental Model

L'applicazione gestisce le pratiche di laboratorio attraverso un flusso lineare e ordinato:

1. **Interfaccia Utente (Streamlit):** L'operatore visualizza i ticket nella schermata principale oppure compila i moduli per crearne di nuovi o modificarli. L'uso dei blocchi `st.form` evita ricaricamenti continui durante la digitazione, mentre un piccolo script JavaScript calcola i caratteri inseriti in tempo reale.
2. **Passaggio Dati tra le Pagine:** Quando si seleziona un ticket per la modifica, i suoi dati vengono salvati temporaneamente nella memoria della sessione (`st.session_state`). Se un utente prova ad aprire la pagina di modifica senza aver prima scelto un ticket, il sistema mostra un avviso e blocca la pagina per evitare errori.
3. **Elaborazione e Prefissi Telefonici:** Il modulo `prefissi.py` ripulisce i contatti e separa automaticamente il prefisso internazionale dal numero locale, associando la bandiera corretta.
4. **Salvataggio su File (CSV):** Prima di salvare una creazione, modifica o cancellazione, l'app ricarica sempre il file `dati.csv` da disco per avere i dati aggiornati, garantendo la coerenza dell'archivio.

Questo schema assicura che l'interfaccia risponda subito ai comandi dell'operatore, che le informazioni siano coerenti e che il file dei dati non venga sovrascritto accidentalmente.

---

## 2. Struttura dei Moduli (SSOT)

Tutti i componenti del progetto risiedono all'interno del repository con compiti ben definiti:

```text
Python_Esercizio_Finale/
├── gestione.py         # Schermata iniziale: tabella ticket, ricerca rapida, KPI ed eliminazione
├── prefissi.py         # Elenco prefissi mondiali con bandiere e funzioni di separazione
├── dati.csv            # Archivio dei dati in formato CSV (database locale del gestionale)
├── GUIDA_PROGETTO.md   # Obiettivi, requisiti e visione funzionale del software
├── README.md           # Presentazione del progetto, guida all'installazione e crediti
├── architecture.md     # Documento di architettura e funzionamento tecnico
├── worklog.txt         # Diario di bordo delle attività svolte durante lo sviluppo
├── requirements.txt    # Elenco delle librerie Python necessarie (Streamlit, Pandas, ecc.)
├── .streamlit/
│   └── config.toml     # Configurazione del tema scuro e del font Orbitron
├── pages/
│   ├── crea_ticket.py     # Modulo con form guidato per inserire una nuova pratica
│   ├── modifica_ticket.py # Modulo per aggiornare i dati di un ticket esistente
│   ├── analisi_ticket.py  # Modulo con grafici temporali e statistiche sui clienti
│   └── assets/
│       └── logo.png       # Logo grafico dell'applicazione visualizzato nella barra superiore
└── static/fonts/          # File dei font (Orbitron) usati per l'aspetto grafico dell'interfaccia
```

---

## 3. Regole e Funzionamento dello Stato

Per mantenere l'applicazione stabile e prevenire la perdita di dati, vengono seguite queste regole pratiche:

* **Navigazione Protetta:** La pagina `modifica_ticket.py` verifica sempre la presenza di `riga_selezionata` in `st.session_state`. Se il dato manca, la pagina si ferma subito senza generare errori nel browser.
* **Rilettura da Disco:** Prima di salvare qualsiasi modifica o cancellazione, l'app rilegge il file `dati.csv` fresco per evitare di sovrascrivere informazioni più recenti.
* **Telefoni Salvati come Testo:** La colonna `Cellulare` viene gestita strettamente come stringa (`str`) per non perdere il segno `+` del prefisso o gli zeri iniziali del numero.
* **Riconoscimento Intelligente del Prefisso:** La funzione di divisione analizza prima i prefissi più lunghi (es. `+1242`) e solo dopo quelli a cifra singola (es. `+1`), evitando assegnazioni errate di nazione.
* **Contatore Caratteri Immediato:** Un mini-script JavaScript interno alla pagina conta i 256 caratteri della descrizione sul browser dell'utente, cambiando colore da verde a rosso senza ricaricare la pagina Python.
* **Moduli Isolati (`st.form`):** Tutti i campi di inserimento si trovano dentro un form che invia i dati solo quando l'operatore preme il pulsante di conferma.
* **Generazione Automatica dell'ID:** In fase di creazione, il nuovo codice pratica viene calcolato prendendo il valore massimo esistente e aggiungendo 1 (`max(ID) + 1`).
* **Eliminazione Sicura:** La rimozione dei ticket richiede una conferma esplicita tramite una finestra a comparsa (`@st.dialog`), riducendo al minimo il rischio di cancellazioni per errore.

---

## 4. I 4 Contratti Fondamentali

Queste quattro convenzioni definiscono i vincoli di base dell'applicazione:

### 4.1. File Dati (`dati.csv`)
Tutti i ticket sono registrati in un unico file CSV salvato in formato UTF-8:

```csv
ID,Nome,Cognome,Descrizione,Cellulare,email,Data
7133,Sofia,Mancini,Batteria laptop scarica,395413982250,sofia.mancini10@example.com,2024-01-02
```

| Colonna | Tipo | Regola / Descrizione |
| :--- | :---: | :--- |
| **`ID`** | Numero | Identificativo unico calcolato in automatico aggiungendo 1 al valore massimo esistente. |
| **`Nome`** / **`Cognome`** | Testo | Dati del cliente, obbligatori e utilizzati per la ricerca rapida nella tabella. |
| **`Descrizione`** | Testo | Spiegazione del malfunzionamento dichiarato dal cliente (massimo 256 caratteri). |
| **`Cellulare`** | Testo | Numero con prefisso internazionale, salvato come testo continuo senza spazi. |
| **`email`** | Testo | Recapito email del cliente per notifiche e comunicazioni. |
| **`Data`** | Testo | Data di accettazione salvata nel formato `YYYY-MM-DD` e mostrata come `DD/MM/YYYY`. |

### 4.2. Memoria di Sessione (`st.session_state`)
* `riga_selezionata`: contiene i dati del ticket scelto nella home per passarli alla schermata di modifica.
* `nuova_riga`: memorizza l'ultimo ticket inserito per confermare l'avvenuto salvataggio.
* `filtro_ricerca_home`: memorizza la parola digitata nella barra di ricerca per mantenerla attiva.
* `selettore_ordinamento_home`: memorizza la modalità di ordinamento scelta dall'operatore.

### 4.3. Formato dei Prefissi (`prefissi.py`)
Ogni voce dell'elenco mondiale segue la struttura: `(Prefisso, Bandiera, Nome Paese)`, ad esempio `("+39", "🇮🇹", "Italia")`. La funzione `separa_prefisso_e_numero()` divide il prefisso dal recapito locale.

### 4.4. Stile Grafico e Tema (`.streamlit/config.toml`)
* **Colori:** Sfondo scuro (`#11172b`), contenitori secondari (`#233a52`) e pulsanti principali azzurri (`#007bc2`).
* **Carattere:** Font `Orbitron` applicato globalmente e polyfill Twemoji per visualizzare le bandiere anche su Windows.

---

## 5. Strategia di Controllo e Qualità

La correttezza del codice e dei dati viene controllata su tre livelli:

| Livello | Ambito | Controlli Effettuati | Metodo di Verifica |
| :--- | :--- | :--- | :--- |
| **1. Codice Pulito** | Qualità del codice Python | Rispetto delle linee guida PEP 8, assenza di variabili o import inutilizzati e tipi dichiarati. | `ruff check .` |
| **2. Integrità Dati** | Consistenza del file CSV | Nessun ID duplicato, date lette in sicurezza senza bloccare l'app e prefissi telefonici validi. | Controlli nel codice Pandas |
| **3. Prova Funzionale** | Funzionamento dell'app | Test dei percorsi: creazione ticket, modifica guidata, ricerca istantanea e rimozione con popup. | `streamlit run gestione.py` |

### Procedura di Verifica Rapida
Prima di registrare nuove modifiche nel repository:
1. Verificare che il codice rispetti la formattazione con lo strumento linter.
2. Accertarsi che il file `dati.csv` non contenga righe corrotte o valori di data non validi.
3. Avviare l'applicazione in locale ed eseguire una prova completa di aggiunta, modifica ed eliminazione.
