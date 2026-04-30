import sqlite3


# Nome del file SQLite in cui vengono salvati gli articoli estratti.
DB_NAME = "articles.db"


def init_db():
    """Inizializza il database ricreando la tabella degli articoli."""
    # La connessione in un context manager salva automaticamente le modifiche a fine blocco.
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        # Per un progetto didattico ripartiamo da zero a ogni esecuzione dello scraper.
        cursor.execute("DROP TABLE IF EXISTS articles")
        # Tabella minimale: titolo, URL e punteggio letto da Hacker News.
        cursor.execute(
            """
            CREATE TABLE articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT,
                score INTEGER
            )
            """
        )


def insert_article(title, url, score):
    """Inserisce un singolo articolo nella tabella articles."""
    # I placeholder '?' proteggono la query da SQL injection e problemi di escaping.
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO articles (title, url, score) VALUES (?, ?, ?)",
            (title, url, score),
        )
