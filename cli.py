"""Simple command line interface for CifraClub search and chord retrieval."""

from __future__ import annotations

from cifraclub import search_songs, fetch_song


def main() -> None:
    query = input("Buscar canción: ").strip()
    if not query:
        print("Consulta vacía.")
        return

    results = search_songs(query)
    if not results:
        print("No se encontraron resultados.")
        return

    for idx, item in enumerate(results, 1):
        print(f"{idx}. {item['title']}")

    try:
        choice = int(input("Elige número de canción: ").strip())
        song = results[choice - 1]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return

    chords = fetch_song(song["url"])
    if chords is None:
        print("No se pudo obtener la canción.")
        return

    print("\n" + chords)


if __name__ == "__main__":
    main()
