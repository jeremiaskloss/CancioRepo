import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador Armónico de Canciones", layout="centered")

st.title("🎵 Buscador Armónico de Canciones")
st.write("Filtrá por acorde para ver qué canciones podés tocar.")

@st.cache_data
def cargar_datos():
    return pd.read_csv("analisis_armonico.csv")

df = cargar_datos()
acordes_unicos = sorted(set(sum([ac.split(" - ") for ac in df["Acordes"]], [])))

acorde_seleccionado = st.selectbox("🎸 Elegí un acorde:", acordes_unicos)

resultados = df[df["Acordes"].str.contains(acorde_seleccionado)]
st.write(f"Se encontraron {len(resultados)} canciones con el acorde **{acorde_seleccionado}**:")
for _, row in resultados.iterrows():
    st.markdown(f"- [{row['Título']} - {row['Artista']}]({row['URL']})")
