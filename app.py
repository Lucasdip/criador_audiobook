import streamlit as st
from gtts import gTTS
import fitz  # PyMuPDF
import base64
import os

# Função para aplicar estilo macOS-like
def set_macos_theme_with_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    css = f"""
    <style>
    html, body, .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
        font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", sans-serif;
        color: #ffffff;
    }}
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stButton > button {{
        background-color: rgba(255, 255, 255, 0.85);
        color: #000000;
        border: 1px solid #d1d1d6;
        border-radius: 12px;
        padding: 8px;
    }}
    .stDownloadButton > button {{
        background-color: #007aff;
        color: white;
        font-weight: 500;
        border-radius: 12px;
        padding: 8px 20px;
    }}
    h1, h2, h3, label {{
        font-weight: 600;
        color: #1d1d1f;
        
    }}
    .stMarkdown {{
        font-size: 1rem;
        background-color: rgba(255, 255, 255, 0.7);
        padding: 10px;
        border-radius: 12px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Configuração do app
st.set_page_config(page_title="PDF para Áudio", layout="centered")
set_macos_theme_with_background("img1.jpg")


# Interface
st.title("📄 PDF para Áudio 🎧")
st.markdown("Transforme qualquer PDF em um arquivo de áudio com voz natural.")

uploaded_pdf = st.file_uploader("Envie seu PDF", type="pdf")
idioma = st.selectbox("Idioma da narração", ["pt-br", "en", "es", "fr"])
nome_audio = st.text_input("Nome do arquivo de áudio (sem .mp3)", value="nome_do_audio")

# Botão de conversão
if uploaded_pdf and st.button("Converter"):
    try:
        doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()

        if not texto.strip():
            st.error("O PDF está vazio.")
        else:
            st.info("Gerando o áudio...")

            tts = gTTS(text=texto, lang=idioma)
            caminho_mp3 = f"{nome_audio.strip() or 'audio'}.mp3"
            tts.save(caminho_mp3)

            st.audio(caminho_mp3)
            with open(caminho_mp3, "rb") as f:
                st.download_button("Baixar Áudio", data=f, file_name=caminho_mp3, mime="audio/mp3")

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
