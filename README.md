# CifraClub CLI

Interfaz de línea de comandos para buscar canciones y mostrar sus acordes desde [CifraClub](https://www.cifraclub.com.br) sin abrir el navegador.

## Requisitos

- Python 3.9+
- Dependencias del archivo `requirements.txt`

Instala dependencias con:

```bash
pip install -r requirements.txt
```

## Uso

```bash
python cifraclub_cli.py "legiao urbana" --limit 5
```

El programa mostrará los primeros resultados, su URL y permitirá elegir uno para imprimir la cifra en la terminal. Si no proporcionas términos de búsqueda, se solicitarán por consola.

## Pruebas

Ejecuta las pruebas unitarias con:

```bash
python -m pytest
```
