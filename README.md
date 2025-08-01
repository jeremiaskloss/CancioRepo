# Music Analyzer 🎶

Herramienta para analizar características musicales de una canción.

Permite obtener tempo (BPM), tonalidad, energía, valence y danceability desde Spotify o analizando archivos MP3/WAV de forma local.

## Cómo usar

1. Desplegar en [Streamlit Cloud](https://streamlit.io/cloud) o correr `streamlit run app.py`.
2. Establecer variables de entorno `SPOTIPY_CLIENT_ID` y `SPOTIPY_CLIENT_SECRET` si vas a analizar canciones de Spotify.
3. Seleccionar la fuente en la barra lateral: Spotify, MusicBrainz o archivo de audio local.
4. Introduce la URL/ID de la canción o sube el archivo a analizar.
5. Para la opción MusicBrainz, ingresa el ID de grabación (MBID) y se mostrarán sus metadatos.

## Despliegue en GitHub y Streamlit

1. Crea un repositorio en GitHub.
2. Desde tu terminal ejecuta:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <URL-repo>
git push -u origin main
```

3. En Streamlit Cloud, selecciona el repositorio público y el archivo `app.py` para lanzar la aplicación.

---
Creado con ❤️ usando ChatGPT
