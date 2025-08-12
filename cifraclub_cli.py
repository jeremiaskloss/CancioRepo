#!/usr/bin/env python3
"""CLI para buscar canciones y acordes en CifraClub."""

import sys
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.cifraclub.com.br"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def buscar(query: str):
    """Busca canciones en CifraClub y devuelve una lista de tuplas (titulo, enlace)."""
    url = f"{BASE_URL}/?q={requests.utils.quote(query)}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    sopa = BeautifulSoup(resp.text, "html.parser")
    patron = re.compile(r"^/[\w\-]+/[\w\-]+/?$")
    resultados = []
    vistos = set()
    for a in sopa.find_all("a", href=patron):
        enlace = BASE_URL + a["href"]
        titulo = a.get_text(strip=True)
        if enlace not in vistos and titulo:
            resultados.append((titulo, enlace))
            vistos.add(enlace)
    return resultados

def obtener_acordes(url: str):
    """Obtiene el bloque de acordes de una canción."""
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    sopa = BeautifulSoup(resp.text, "html.parser")
    bloque = sopa.find("pre")
    if not bloque:
        # Algunas páginas usan divs; intentamos varias clases comunes
        for clase in ["cifra_centro", "tabela_cifra", "cifra"]:
            bloque = sopa.find("div", class_=clase)
            if bloque:
                break
    if not bloque:
        return "No se pudo encontrar la cifra."
    return bloque.get_text("\n", strip=False)

def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Buscar: ")
    try:
        resultados = buscar(query)
    except Exception as e:
        print(f"Error al buscar: {e}")
        return
    if not resultados:
        print("Sin resultados.")
        return
    for i, (titulo, _) in enumerate(resultados[:10], 1):
        print(f"{i}. {titulo}")
    try:
        idx = int(input("Elige una canción: ")) - 1
        titulo, enlace = resultados[idx]
    except Exception:
        print("Selección inválida.")
        return
    try:
        acordes = obtener_acordes(enlace)
    except Exception as e:
        print(f"Error al obtener acordes: {e}")
        return
    print(f"\n{titulo}\n{'-' * len(titulo)}\n")
    print(acordes)

if __name__ == "__main__":
    main()
