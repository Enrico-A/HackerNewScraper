import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


DB_NAME = "articles.db"


def main():
    with sqlite3.connect(DB_NAME) as connection:
        articles = pd.read_sql_query("SELECT title, score FROM articles", connection)

    top_articles = articles.sort_values(by="score", ascending=False).head(10)

    plt.figure(figsize=(12, 7))
    bars = plt.barh(top_articles["title"], top_articles["score"], color="steelblue")
    plt.xlabel("Punti")
    plt.ylabel("Titoli")
    plt.title("Top 10 Notizie su Hacker News")
    plt.gca().invert_yaxis()

    max_score = top_articles["score"].max()
    label_offset = max_score * 0.01 if max_score > 0 else 1

    for bar in bars:
        score = int(bar.get_width())
        plt.text(
            bar.get_width() + label_offset,
            bar.get_y() + bar.get_height() / 2,
            str(score),
            va="center",
        )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
