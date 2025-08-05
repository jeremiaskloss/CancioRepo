import streamlit as st
from scraper import search_songs, get_song_chords

st.set_page_config(page_title="Análisis Armónico de Canciones", layout="centered")
st.title("🎵 Análisis Armónico de Canciones")

option = st.radio("Selecciona una opción", ["Subir audio (próximamente)", "Buscar canción"])

if option == "Subir audio (próximamente)":
    st.info("Esta funcionalidad estará disponible próximamente.")
else:
    query = st.text_input("Ingresa el nombre de la canción o artista")
    if query:
        with st.spinner("Buscando..."):
            try:
                results = search_songs(query)
            except Exception as e:
                results = []
                st.error(f"Ocurrió un error al buscar: {e}")
        if results:
            options = {title: url for title, url in results}
            choice = st.selectbox("Resultados de búsqueda", list(options.keys()))
            if choice:
                song_url = options[choice]
                with st.spinner("Descargando letra y acordes..."):
                    try:
                        text = get_song_chords(song_url)
                        st.text_area("Letra con acordes", text, height=400)
                        st.download_button("Descargar como .txt", data=text, file_name="cancion.txt")
                    except Exception as e:
                        st.error(f"No fue posible obtener la canción: {e}")
        else:
            st.warning("No se encontraron resultados.")
