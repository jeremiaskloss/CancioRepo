import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

BASE_URL = "https://www.cifraclub.com.br"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def search_song(query: str):
    """Search songs on CifraClub and return list of dicts with title and url."""
    q = unidecode(query).strip()
    if not q:
        return []
    try:
        response = requests.get(f"{BASE_URL}/busca/", params={"q": q}, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for link in soup.select("a.gs-title"):
        title = link.get_text(strip=True)
        href = link.get("href", "")
        if not href:
            continue
        if href.startswith("/"):
            href = BASE_URL + href
        results.append({"title": title, "url": href})
    return results


def fetch_song(url: str):
    """Return chord sheet from a CifraClub song url preserving formatting."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    pre = soup.find("pre")
    if not pre:
        return None
    return pre.get_text("\n", strip=False)
