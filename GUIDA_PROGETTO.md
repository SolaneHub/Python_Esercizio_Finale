# Descrizione del Progetto: Gestionale per Centro Assistenza Informatica

## 1. Visione Generale e Scopo del Software

L'obiettivo del progetto è la realizzazione di un software gestionale pensato su misura per le esigenze quotidiane di un piccolo negozio o laboratorio di assistenza tecnica e riparazione di dispositivi elettronici (computer desktop, notebook, smartphone, tablet e periferiche).

Il programma ha lo scopo di centralizzare, organizzare e velocizzare tutte le attività del negozio, eliminando la gestione cartacea o l'uso di fogli sparsi. Accompagna il negoziante e i tecnici lungo tutto l'arco di vita del servizio: dal momento in cui il cliente entra in negozio per consegnare il dispositivo guasto, passando per la diagnosi, l'approvvigionamento dei pezzi di ricambio e la riparazione, fino al saldo finale e alla riconsegna.

---

## 2. I Moduli Funzionali del Progetto

### Modulo 1: Gestione Clienti
Questo modulo costituisce l'anagrafica del negozio e permette di mantenere un contatto puntuale e organizzato con ogni cliente.

* **Registrazione e Modifica**: Possibilità di inserire nuovi clienti e di aggiornare in ogni momento i loro dati di contatto (nome, cognome, numero di telefono principale, eventuale secondo recapito ed email per comunicazioni e notifiche).
* **Ricerca Rapida**: Sistema di ricerca flessibile per rintracciare un cliente in pochi istanti al momento dell'accoglienza al bancone, cercando per nome, per cognome o anche solo per una parte del numero di telefono.
* **Storico degli Interventi**: Ogni scheda cliente raccoglie e mostra l'elenco completo di tutti i dispositivi portati in riparazione nel tempo, permettendo al tecnico di conoscere i precedenti guasti o le abitudini del cliente.

---

### Modulo 2: Gestione Riparazioni (Pratiche)
Il cuore operativo dell'attività, dove ogni intervento viene trasformato in una pratica formale e tracciabile.

* **Identificativo Univoco**: Ogni riparazione riceve un codice identificativo univoco (codice pratica), utile per identificare il dispositivo fisicamente in laboratorio e per consentire al cliente di richiedere informazioni sullo stato di avanzamento.
* **Informazioni della Pratica**:
  * Associazione al cliente registrato.
  * Tipologia di dispositivo, marca e modello esatto.
  * Descrizione accurata del malfunzionamento dichiarato dal cliente ed eventuali annotazioni sulle condizioni estetiche iniziali del dispositivo.
  * Data di accettazione e data prevista per la consegna.
  * Tecnico assegnato alla lavorazione.
  * Preventivo iniziale comunicato al cliente e costo finale consuntivato (suddiviso tra costo dei componenti e costo della manodopera).
* **Ciclo di Vita e Stati della Pratica**:
  La pratica attraversa fasi ben definite e aggiornabili durante il lavoro:
  * **Nuova / Aperta**: Il dispositivo è appena stato preso in carico al bancone ed è in attesa di diagnosi.
  * **In lavorazione / In corso**: Il tecnico sta effettuando le verifiche, i test o l'intervento di riparazione.
  * **In attesa di ricambi / Sospesa**: La riparazione è momentaneamente ferma in attesa dell'arrivo di pezzi ordinati o in attesa di conferma del preventivo da parte del cliente.
  * **Completata / Terminata**: Il lavoro tecnico e il collaudo sono terminati con successo; il dispositivo è pronto e si attende il cliente per il ritiro.
  * **Consegnata / Chiusa**: Il dispositivo è stato riconsegnato al proprietario, il pagamento è stato saldato e la pratica viene archiviata.

---

### Modulo 3: Gestione Magazzino e Ricambi
Questo modulo garantisce il controllo preciso delle scorte di ricambi e materiali di consumo (display, batterie, memorie RAM, dischi SSD, alimentatori, paste termiche, cavi).

* **Catalogo Componenti**: Registrazione di ogni articolo con codice prodotto, descrizione estesa, quantità attualmente disponibile in scaffale, prezzo di acquisto (costo sostenuto dal negozio) e prezzo di vendita al cliente finale.
* **Scarico Automatico dei Ricambi**: Nel momento in cui un componente viene impiegato e registrato all'interno di una pratica di riparazione, il sistema aggiorna istantaneamente la giacenza di magazzino, scalando i pezzi utilizzati senza necessità di aggiornamenti manuali.
* **Controllo Scorte e Avvisi Sottoscorta**: Ogni prodotto dispone di una soglia minima di sicurezza personalizzata. Quando la quantità disponibile scende al di sotto o al pari di questa soglia, il sistema genera un avviso visivo che segnala la necessità di un nuovo ordine al fornitore.

---

### Modulo 4: Pagamenti, Cassa e Reportistica
La sezione dedicata al monitoraggio economico dell'attività e all'analisi dell'andamento del negozio.

* **Registrazione Pagamenti**: Possibilità di registrare i movimenti finanziari per ciascuna riparazione, gestendo con precisione sia gli acconti (es. anticipi richiesti per ordinare ricambi costosi) sia i saldi finali al momento del ritiro, con evidenza immediata dell'eventuale importo ancora da riscuotere.
* **Indicatori di Performance (Report)**:
  * **Incasso Totale**: Visualizzazione immediata della liquidità incassata nell'arco della giornata o in un periodo specifico.
  * **Riparazioni Aperte**: Quadro riassuntivo di tutti i dispositivi attualmente presenti in laboratorio, utile per individuare ritardi o colli di bottiglia.
  * **Ricavi Mensili**: Calcolo del volume d'affari mensile e della marginalità (differenza tra prezzo di vendita dei ricambi/manodopera e costo di acquisto).
* **Esportazione in Formato CSV**: Funzionalità di esportazione dei dati delle riparazioni, degli incassi e delle scorte in file tabellari CSV, facilmente apribili e consultabili con programmi di foglio di calcolo per fini contabili o di archiviazione.

---

## 3. Risultato Atteso

Al termine della realizzazione, il software offrirà un ambiente centralizzato, intuitivo e ordinato in grado di:
1. Ridurre a zero il rischio di smarrimento o confusione tra i dispositivi in laboratorio.
2. Mantenere le giacenze di magazzino costantemente allineate all'attività reale.
3. Fornire al cliente un servizio trasparente e professionale, con preventivi chiari e tracciamento dello stato del lavoro.
4. Dare al titolare una visione finanziaria chiara e in tempo reale sui guadagni, sui crediti residui e sul carico di lavoro dei tecnici.
