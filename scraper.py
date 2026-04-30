import requests
from bs4 import BeautifulSoup


url = "https://news.ycombinator.com/"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers, timeout=10)

if response.status_code != 200:
    print(f"Errore: status code {response.status_code}")
else:
    soup = BeautifulSoup(response.text, "html.parser")
    stories = soup.select(".athing")[:10]

    for index, story in enumerate(stories, start=1):
        title_tag = story.select_one(".titleline > a")

        if title_tag is None:
            continue

        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")

        print(f"{index}. {title}")
        print(f"   Link: {link}")
