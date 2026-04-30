import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://news.ycombinator.com/"
MAX_PAGES = 3
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def clean_score(score_string):
    numbers = re.findall(r"\d+", score_string)
    return int("".join(numbers)) if numbers else 0


url = BASE_URL

for page in range(1, MAX_PAGES + 1):
    response = requests.get(url, headers=headers, timeout=10)

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
        link = title_tag.get("href", "")
        points = clean_score(score_tag.get_text(strip=True) if score_tag else "")

        print(f"{index}. {title}")
        print(f"   Punti: {points}")
        print(f"   Link: {link}")

    more_link = soup.select_one(".morelink")
    if page == MAX_PAGES or more_link is None:
        break

    url = urljoin(BASE_URL, more_link.get("href", ""))
    time.sleep(3)
