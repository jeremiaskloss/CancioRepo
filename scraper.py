import re
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

BASE_URL = "https://www.cifraclub.com.br"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def search_songs(query):
    """Return a list of (title, url) from CifraClub search results."""
    if not query:
        return []
    q = quote(unidecode(query))
    url = f"{BASE_URL}/?q={q}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException as e:
        raise RuntimeError("No se pudo realizar la búsqueda.") from e
    if resp.status_code != 200:
        raise RuntimeError(
            f"No se pudo realizar la búsqueda (HTTP {resp.status_code})."
        )
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(BASE_URL, href)
        if re.match(r"https://www.cifraclub.com.br/[^/]+/[^/]+/?$", full_url):
            title = a.get_text(strip=True)
            if title and (title, full_url) not in results:
                results.append((title, full_url))
    return results

def get_song_chords(url):
    """Fetch chord and lyric text from a CifraClub song page."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException as e:
        raise RuntimeError("No se pudo obtener la canción.") from e
    if resp.status_code != 200:
        raise RuntimeError(
            f"No se pudo obtener la canción (HTTP {resp.status_code})."
        )
    soup = BeautifulSoup(resp.text, "html.parser")
    pre = soup.find("pre")
    if not pre:
        raise RuntimeError("Formato de canción no reconocido.")
    text = pre.get_text("\n", strip=False)
    return text.strip("\n")
