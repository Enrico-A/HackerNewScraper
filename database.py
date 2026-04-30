import sqlite3


DB_NAME = "articles.db"


def init_db():
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS articles")
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
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO articles (title, url, score) VALUES (?, ?, ?)",
            (title, url, score),
        )
