"""Helpers to search and fetch songs from CifraClub.

Search queries are normalized with ``unidecode`` to improve match
reliability regardless of accents or special characters.
"""

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

BASE_URL = "https://www.cifraclub.com.br"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def search_song(query: str):
    """Search songs on CifraClub.

    The query string is normalized with ``unidecode`` to remove accents
    before sending the request. Returns a list of dicts with ``title`` and
    ``url`` keys for each result.
    """
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
    """Fetch chord sheet from a CifraClub song page.

    Tries several selectors in order to locate the chord/lyric block:

    1. ``<pre>``
    2. ``<div class="cifra_cnt">``
    3. any element whose ``class`` contains ``"cifra"``

    Returns the extracted text with chords aligned above lyrics, or
    ``None`` if the request fails or none of the selectors are found.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Most songs use a ``<pre>`` block, but others rely on ``<div class="cifra_cnt">``
    # or custom elements. Try several selectors before giving up so a wider range
    # of layouts can be parsed.
    container = soup.find("pre")
    if not container:
        container = soup.find("div", class_="cifra_cnt")
    if not container:
        # Fall back to any element whose class includes "cifra"
        container = soup.find(attrs={"class": lambda c: c and "cifra" in c})
    if not container:
        return None

    return container.get_text("\n", strip=False)
