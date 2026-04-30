# 📰 Hacker News Scraper

Un piccolo progetto didattico in Python per imparare a raccogliere dati dal web, salvarli in un database SQLite e visualizzarli con un grafico.

Lo scraper visita Hacker News, estrae titoli, link e punteggi delle notizie, salva tutto in `articles.db` e permette di esplorare i risultati sia da terminale sia tramite una semplice interfaccia grafica Tkinter.

## ✨ Cosa impari

- Fare richieste HTTP con `requests`
- Analizzare HTML con `BeautifulSoup`
- Salvare dati in SQLite
- Visualizzare dati con `pandas` e `matplotlib`
- Scrivere test automatici con `pytest`
- Separare un progetto Python in moduli chiari

## ✅ Prerequisiti

- Python 3.10 o superiore
- `pip`
- Connessione internet per scaricare le pagine di Hacker News

Su Windows è consigliato usare PowerShell o il terminale integrato di VS Code.

## 📦 Installazione

Clona o apri la cartella del progetto, poi crea un ambiente virtuale:

```powershell
py -m venv .venv
```

Attiva l'ambiente virtuale:

```powershell
.\.venv\Scripts\Activate.ps1
```

Installa le dipendenze:

```powershell
pip install -r requirements.txt
```

## 🚀 Come lanciare lo scraper

Per eseguire lo scraper da terminale:

```powershell
python scraper.py
```

Lo script visita fino a 3 pagine di Hacker News, stampa le notizie trovate e crea il file `articles.db` con i risultati.

Puoi anche usare la piccola app grafica:

```powershell
python app.py
```

Poi premi **Scrape Hacker News** per avviare la raccolta.

## 📊 Come vedere il grafico

Dopo aver eseguito lo scraper almeno una volta, genera il grafico con:

```powershell
python analytics.py
```

Il grafico mostra le 10 notizie con il punteggio più alto tra quelle salvate nel database.

Dalla GUI puoi ottenere lo stesso risultato premendo **Plot Scores**.

## 🧪 Come eseguire i test

Avvia i test automatici con:

```powershell
pytest
```

I test verificano il comportamento della funzione `clean_score`, che trasforma stringhe come `123 points` in numeri utilizzabili dal programma.

## 🗂️ Struttura del progetto

```text
HackerNewScraper/
├── analytics.py          # Legge il database e genera il grafico
├── app.py                # Interfaccia grafica Tkinter
├── database.py           # Creazione tabella e inserimento articoli
├── scraper.py            # Logica di scraping da Hacker News
├── pytest.ini            # Configurazione dei test
├── requirements.txt      # Dipendenze Python
├── tests/
│   └── test_scraper.py   # Test automatici
└── README.md             # Guida del progetto
```

## 🧭 Flusso di lavoro consigliato

1. Installa le dipendenze
2. Lancia `python scraper.py`
3. Apri il grafico con `python analytics.py`
4. Controlla che tutto funzioni con `pytest`

Buon scraping e buona esplorazione dei dati! ✨
