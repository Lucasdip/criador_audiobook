# app.py
import streamlit as st
from gtts import gTTS
import fitz

st.title("📖 PDF para Podcast 🎧")

pdf = st.file_uploader("Envie seu PDF", type="pdf")
idioma = st.selectbox("Idioma da narração", ["pt-br", "en"])

if pdf and st.button("Converter em áudio"):
    texto = ""
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    for pagina in doc:
        texto += pagina.get_text()
    
    if texto.strip():
        tts = gTTS(text=texto, lang=idioma)
        tts.save("podcast.mp3")
        st.success("Áudio gerado com sucesso!")
        audio_file = open("podcast.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
    else:
        st.error("Texto não encontrado no PDF.")
