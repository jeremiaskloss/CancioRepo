import streamlit as st
import os
import numpy as np
import librosa
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import musicbrainzngs

st.set_page_config(page_title="Music Analyzer", layout="centered")
st.title("🎶 Music Analyzer")
musicbrainzngs.set_useragent("MusicAnalyzer", "1.0")

source = st.sidebar.selectbox("Select input source", ["Spotify Track", "MusicBrainz Recording", "Upload Audio File"])

if source == "Spotify Track":
    spotify_url = st.text_input("Enter Spotify track URL or ID")
    client_id = os.environ.get("SPOTIPY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
    if spotify_url and client_id and client_secret:
        try:
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            track_id = spotify_url.split("/")[-1].split("?")[0]
            info = sp.track(track_id)
            features = sp.audio_features(track_id)[0]
            st.subheader(f"{info['name']} - {info['artists'][0]['name']}")
            st.write(f"Tempo: {features['tempo']} BPM")
            key = features.get('key')
            mode = features.get('mode')
            key_names = ['C','C#','D','Eb','E','F','F#','G','G#','A','Bb','B']
            if key is not None:
                scale = "major" if mode == 1 else "minor"
                st.write(f"Key: {key_names[key]} {scale}")
            st.write(f"Energy: {features['energy']}")
            st.write(f"Valence: {features['valence']}")
            st.write(f"Danceability: {features['danceability']}")
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.info("Provide track URL/ID and set Spotify credentials in environment variables.")
elif source == "MusicBrainz Recording":
    mbid = st.text_input("Enter MusicBrainz recording ID")
    if mbid:
        try:
            rec = musicbrainzngs.get_recording_by_id(mbid, includes=["artists", "releases"])
            info = rec["recording"]
            title = info.get("title", "")
            artist = info.get("artist-credit", [{}])[0].get("artist", {}).get("name", "")
            release = info.get("releases", [{}])[0].get("title", "N/A") if info.get("releases") else "N/A"
            st.subheader(f"{title} - {artist}")
            st.write(f"Release: {release}")
            if "length" in info:
                length_sec = int(info["length"]) / 1000.0
                st.write(f"Length: {length_sec:.2f} sec")
        except Exception as e:
            st.error(f"Error fetching data: {e}")
else:
    uploaded = st.file_uploader("Upload MP3/WAV", type=["mp3","wav"])
    if uploaded is not None:
        with st.spinner('Analyzing...'):
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name
            y, sr = librosa.load(tmp_path)
            tempo = librosa.beat.tempo(y=y, sr=sr)[0]
            chroma = librosa.feature.chroma_cens(y=y, sr=sr)
            chroma_mean = chroma.mean(axis=1)
            note_index = chroma_mean.argmax()
            key_names = ['C','C#','D','Eb','E','F','F#','G','G#','A','Bb','B']
            st.write(f"Tempo: {tempo:.2f} BPM")
            st.write(f"Likely key: {key_names[note_index]}")
            os.remove(tmp_path)
