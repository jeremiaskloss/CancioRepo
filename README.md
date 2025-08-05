# Análisis Armónico de Canciones 🎶

Aplicación en Streamlit que busca canciones en [CifraClub](https://www.cifraclub.com.br/),
obteniendo letra y acordes con el formato original (acordes alineados sobre la letra).

## Cómo usar

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar la app:
   ```bash
   streamlit run app.py
   ```
3. Ingresá el nombre de la canción, elegí el resultado correcto y consultá la letra con acordes. La aplicación muestra toda la información disponible del resultado (p. ej., título y URL) antes de desplegar los acordes.

Las búsquedas normalizan el texto (p. ej., eliminando acentos) para mejorar la compatibilidad con CifraClub.

La opción para subir audio aún no está disponible.

El código de scraping se encuentra en `scraper.py`.
