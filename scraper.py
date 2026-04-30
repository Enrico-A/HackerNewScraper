import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from database import init_db, insert_article


# URL di partenza della homepage di Hacker News.
BASE_URL = "https://news.ycombinator.com/"

# Numero massimo di pagine da visitare durante una singola esecuzione.
MAX_PAGES = 3

# Header HTTP usato per dichiarare una richiesta simile a quella di un browser reale.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def clean_score(score_string):
    """Estrae il valore numerico da una stringa come '123 points'."""
    # Hacker News può omettere il punteggio: in quel caso restituiamo 0.
    numbers = re.findall(r"\d+", score_string)
    return int("".join(numbers)) if numbers else 0


class HackerNewsScraper:
    """Scraper semplice per scaricare titoli, link e punteggi da Hacker News."""

    def __init__(self, base_url=BASE_URL, max_pages=MAX_PAGES, headers=None):
        # Parametri configurabili: utili sia per l'uso reale sia per eventuali test.
        self.base_url = base_url
        self.max_pages = max_pages
        self.headers = headers or HEADERS

    def run(self):
        """Visita le pagine di Hacker News e salva gli articoli nel database."""
        # Parte dalla homepage e prepara il database per una nuova raccolta dati.
        url = self.base_url
        init_db()

        # Scorre le pagine fino al limite configurato o fino alla mancanza del link "More".
        for page in range(1, self.max_pages + 1):
            # Timeout esplicito per evitare che la richiesta resti appesa troppo a lungo.
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code != 200:
                # In caso di errore HTTP interrompe lo scraping in modo leggibile.
                print(f"Errore pagina {page}: status code {response.status_code}")
                break

            # BeautifulSoup trasforma l'HTML in un albero interrogabile con selettori CSS.
            soup = BeautifulSoup(response.text, "html.parser")
            # Ogni riga con classe "athing" rappresenta una storia; qui prendiamo le prime 10.
            stories = soup.select(".athing")[:10]

            print(f"Pagina {page}")

            for index, story in enumerate(stories, start=1):
                # Il titolo e il link vivono nella riga principale della storia.
                title_tag = story.select_one(".titleline > a")
                # Il punteggio si trova nella riga successiva, chiamata subtext nel markup.
                subtext = story.find_next_sibling("tr")
                score_tag = subtext.select_one(".score") if subtext else None

                if title_tag is None:
                    # Salta eventuali righe incomplete o diverse dal formato atteso.
                    continue

                # Normalizza testo, link relativo/assoluto e punteggio numerico.
                title = title_tag.get_text(strip=True)
                link = urljoin(self.base_url, title_tag.get("href", ""))
                points = clean_score(score_tag.get_text(strip=True) if score_tag else "")
                insert_article(title, link, points)

                # Output didattico in console per vedere cosa viene raccolto pagina per pagina.
                print(f"{index}. {title}")
                print(f"   Punti: {points}")
                print(f"   Link: {link}")

            # Cerca il link alla pagina successiva di Hacker News.
            more_link = soup.select_one(".morelink")
            if page == self.max_pages or more_link is None:
                # Si ferma al limite richiesto o se Hacker News non offre altre pagine.
                break

            # Costruisce l'URL della pagina successiva e aspetta per non martellare il sito.
            url = urljoin(self.base_url, more_link.get("href", ""))
            time.sleep(3)


if __name__ == "__main__":
    # Permette di lanciare lo scraper direttamente con: python scraper.py
    scraper = HackerNewsScraper()
    scraper.run()
