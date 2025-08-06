"""Utilities for searching and fetching songs with chords from CifraClub."""

from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from typing import List, Dict

BASE_URL = "https://www.cifraclub.com.br"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def search_songs(query: str) -> List[Dict[str, str]]:
    """Search songs on CifraClub and return a list of dicts with title and url.

    Each dict contains ``title`` and ``url`` keys. When the search fails an empty
    list is returned.
    """
    q = unidecode(query).strip()
    if not q:
        return []
    try:
        resp = requests.get(f"{BASE_URL}/busca/", params={"q": q}, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results: List[Dict[str, str]] = []
    for link in soup.select("a.gs-title"):
        title = link.get_text(strip=True)
        href = link.get("href", "")
        if not href:
            continue
        if href.startswith("/"):
            href = BASE_URL + href
        results.append({"title": title, "url": href})
    return results


def fetch_song(url: str) -> str | None:
    """Return chord sheet text from a CifraClub song URL preserving formatting."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    container = soup.find("pre")
    if not container:
        container = soup.find("div", class_="cifra_cnt")
    if not container:
        container = soup.find(attrs={"class": lambda c: c and "cifra" in c})
    if not container:
        return None
    return container.get_text("\n", strip=False)
