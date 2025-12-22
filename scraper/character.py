import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.tibia.com/community/?subtopic=characters&name="


def get_character(name: str):
    url = BASE_URL + name.replace(" ", "%20")
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="TableContent")
    if not tables:
        return None

    data = {}
    rows = tables[0].find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 2:
            key = cols[0].text.strip().lower()
            value = cols[1].text.strip()
            data[key] = value

    # Campos essenciais
    if "level" not in data or "world" not in data:
        return None

    return {
        "name": name,
        "level": int(data.get("level", 0)),
        "world": data.get("world"),
        "voc": data.get("vocation"),
        "guild": data.get("guild membership", "No Guild"),
    }
