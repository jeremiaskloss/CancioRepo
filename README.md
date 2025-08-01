# Music Analyzer 🎶

Herramienta para analizar características musicales de una canción.

Permite obtener tempo (BPM), tonalidad, energía, valence y danceability desde Spotify o analizando archivos MP3/WAV de forma local.

## Cómo usar

1. Desplegar en [Streamlit Cloud](https://streamlit.io/cloud) o correr `streamlit run app.py`.
2. Establecer variables de entorno `SPOTIPY_CLIENT_ID` y `SPOTIPY_CLIENT_SECRET` para usar la opción de Spotify.
3. Subir un archivo de audio o ingresar la URL/ID de un tema de Spotify.

## Despliegue en GitHub y Streamlit

1. Crea un repositorio en GitHub y sube estos archivos con `git init`, `git add .` y `git commit`.
2. Agrega el remoto con `git remote add origin <URL-repo>` y ejecuta `git push -u origin main`.
3. En Streamlit Cloud, selecciona el repositorio público y el archivo `app.py` para lanzar la aplicación.

---
Creado con ❤️ usando ChatGPT
