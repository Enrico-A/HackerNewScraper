import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from database import init_db, insert_article


BASE_URL = "https://news.ycombinator.com/"
MAX_PAGES = 3
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def clean_score(score_string):
    numbers = re.findall(r"\d+", score_string)
    return int("".join(numbers)) if numbers else 0


class HackerNewsScraper:
    def __init__(self, base_url=BASE_URL, max_pages=MAX_PAGES, headers=None):
        self.base_url = base_url
        self.max_pages = max_pages
        self.headers = headers or HEADERS

    def run(self):
        url = self.base_url
        init_db()

        for page in range(1, self.max_pages + 1):
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code != 200:
                print(f"Errore pagina {page}: status code {response.status_code}")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            stories = soup.select(".athing")[:10]

            print(f"Pagina {page}")

            for index, story in enumerate(stories, start=1):
                title_tag = story.select_one(".titleline > a")
                subtext = story.find_next_sibling("tr")
                score_tag = subtext.select_one(".score") if subtext else None

                if title_tag is None:
                    continue

                title = title_tag.get_text(strip=True)
                link = urljoin(self.base_url, title_tag.get("href", ""))
                points = clean_score(score_tag.get_text(strip=True) if score_tag else "")
                insert_article(title, link, points)

                print(f"{index}. {title}")
                print(f"   Punti: {points}")
                print(f"   Link: {link}")

            more_link = soup.select_one(".morelink")
            if page == self.max_pages or more_link is None:
                break

            url = urljoin(self.base_url, more_link.get("href", ""))
            time.sleep(3)


if __name__ == "__main__":
    scraper = HackerNewsScraper()
    scraper.run()
