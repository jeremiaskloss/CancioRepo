#!/usr/bin/env python3
"""CLI para buscar canciones y acordes en CifraClub."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from typing import Iterable, List, Sequence

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.cifraclub.com.br"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# --- Modelos ---------------------------------------------------------------


@dataclass
class Song:
    """Representa un resultado de búsqueda."""

    title: str
    url: str


# --- Cliente HTTP ---------------------------------------------------------


class CifraClubClient:
    """Cliente ligero para interactuar con CifraClub."""

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()
        self.session.headers.update(HEADERS)

    def search(self, query: str) -> List[Song]:
        """Busca canciones y devuelve una lista de Song ordenada por aparición."""
        url = f"{BASE_URL}/?q={requests.utils.quote(query)}"
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return list(parse_search_results(response.text))

    def chords(self, url: str) -> str:
        """Obtiene el bloque de acordes de una canción."""
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        chords = parse_chords(response.text)
        if not chords:
            return "No se pudo encontrar la cifra."
        return chords


# --- Parseo HTML ----------------------------------------------------------


RESULT_HREF = re.compile(r"^/[\w\-]+/[\w\-]+/$")


def parse_search_results(html: str) -> Iterable[Song]:
    """Extrae enlaces de resultados desde el HTML de búsqueda."""
    soup = BeautifulSoup(html, "html.parser")

    anchors = soup.select("a[href]")
    seen: set[str] = set()

    for anchor in anchors:
        href = anchor.get("href", "")
        if not RESULT_HREF.match(href):
            continue
        url = BASE_URL + href
        title = anchor.get_text(strip=True)
        if not title or url in seen:
            continue
        seen.add(url)
        yield Song(title=title, url=url)


def parse_chords(html: str) -> str:
    """Intenta extraer el bloque de acordes conservando saltos de línea."""
    soup = BeautifulSoup(html, "html.parser")

    # Estrategia 1: bloque pre formateado (el más común)
    pre_candidates = soup.find_all("pre")
    for pre in pre_candidates:
        text = pre.get_text("\n", strip=False)
        if text.strip():
            return text

    # Estrategia 2: contenedores de div utilizados en algunas variaciones
    for class_name in ["cifra_centro", "tabela_cifra", "cifra", "js-lyrics"]:
        div = soup.find("div", class_=class_name)
        if div:
            text = div.get_text("\n", strip=False)
            if text.strip():
                return text
    return ""


# --- CLI ------------------------------------------------------------------


def render_results(results: Sequence[Song], limit: int) -> None:
    if not results:
        print("Sin resultados.")
        return
    for idx, song in enumerate(results[:limit], start=1):
        print(f"{idx}. {song.title} ({song.url})")


def prompt_choice(results: Sequence[Song], limit: int) -> Song | None:
    if not results:
        return None
    try:
        raw = input("Elige una canción [1-{0}]: ".format(min(limit, len(results))))
        pos = int(raw) - 1
    except ValueError:
        print("Selección inválida.")
        return None
    if pos < 0 or pos >= min(limit, len(results)):
        print("Selección fuera de rango.")
        return None
    return results[pos]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="Términos de búsqueda")
    parser.add_argument("--limit", type=int, default=10, help="Máximo de resultados a mostrar")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    query = " ".join(args.query) if args.query else input("Buscar: ")
    client = CifraClubClient()

    try:
        results = client.search(query)
    except requests.HTTPError as exc:
        print(f"Error HTTP al buscar: {exc}")
        return 1
    except requests.RequestException as exc:
        print(f"Error de red al buscar: {exc}")
        return 1

    render_results(results, args.limit)
    choice = prompt_choice(results, args.limit)
    if not choice:
        return 1

    try:
        chords = client.chords(choice.url)
    except requests.HTTPError as exc:
        print(f"Error HTTP al obtener acordes: {exc}")
        return 1
    except requests.RequestException as exc:
        print(f"Error de red al obtener acordes: {exc}")
        return 1

    print(f"\n{choice.title}\n{'-' * len(choice.title)}\n")
    print(chords)
    return 0


if __name__ == "__main__":
    sys.exit(main())
