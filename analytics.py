import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


# Nome del database SQLite creato dallo scraper.
DB_NAME = "articles.db"


def main():
    """Legge gli articoli salvati e mostra un grafico con i 10 punteggi migliori."""
    # Apre una connessione temporanea al database e carica i dati in un DataFrame.
    with sqlite3.connect(DB_NAME) as connection:
        articles = pd.read_sql_query("SELECT title, score FROM articles", connection)

    # Ordina le notizie per punteggio decrescente e tiene solo le prime 10.
    top_articles = articles.sort_values(by="score", ascending=False).head(10)

    # Prepara un grafico a barre orizzontali, più leggibile con titoli lunghi.
    plt.figure(figsize=(12, 7))
    bars = plt.barh(top_articles["title"], top_articles["score"], color="steelblue")
    plt.xlabel("Punti")
    plt.ylabel("Titoli")
    plt.title("Top 10 Notizie su Hacker News")
    plt.gca().invert_yaxis()

    # Calcola un piccolo margine per posizionare le etichette fuori dalle barre.
    max_score = top_articles["score"].max()
    label_offset = max_score * 0.01 if max_score > 0 else 1

    # Scrive il punteggio accanto a ogni barra per rendere il grafico autoesplicativo.
    for bar in bars:
        score = int(bar.get_width())
        plt.text(
            bar.get_width() + label_offset,
            bar.get_y() + bar.get_height() / 2,
            str(score),
            va="center",
        )

    # Ottimizza gli spazi e mostra la finestra del grafico.
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Permette di lanciare il grafico direttamente con: python analytics.py
    main()
