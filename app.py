import streamlit as st
from scraper import search_song, fetch_song

st.set_page_config(page_title="Análisis Armónico de Canciones", layout="centered")

st.title("🎵 Análisis Armónico de Canciones")

opcion = st.radio("Elegí una opción:", ["Subir audio (próximamente)", "Buscar canción"], index=1)

if opcion.startswith("Subir"):
    st.info("La subida de audio aún no está disponible.")
else:
    consulta = st.text_input("Ingresá nombre de canción o artista")
    if consulta:
        resultados = search_song(consulta)
        if not resultados:
            st.warning("No se encontraron coincidencias.")
        else:
            titulos = [r["title"] for r in resultados]
            elegido = st.selectbox("Resultados de búsqueda", titulos)
            url = resultados[titulos.index(elegido)]["url"]
            if st.button("Mostrar acordes y letra"):
                contenido = fetch_song(url)
                if not contenido:
                    st.error("No se pudo obtener el contenido de la canción.")
                else:
                    st.markdown(f"<pre>{contenido}</pre>", unsafe_allow_html=True)
                    st.download_button("Descargar como TXT", contenido, file_name="cancion.txt")
