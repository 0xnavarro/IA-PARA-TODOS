# Importar las bibliotecas requeridas
import tempfile
import streamlit as st
from embedchain import App

# Definir la función embedchain_bot
def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {"provider": "openai", "config": {"model": "gpt-4o", "temperature": 0.5, "api_key": api_key}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},
        }
    )

# Crear aplicación Streamlit
st.title("Chat con Video de YouTube 📺")
st.caption("Esta aplicación te permite chatear con un video de YouTube usando la API de OpenAI")

# Obtener la clave API de OpenAI del usuario
openai_access_token = st.text_input("Clave API de OpenAI", type="password")

# Si se proporciona la clave API de OpenAI, crear una instancia de App
if openai_access_token:
    # Crear un directorio temporal para almacenar la base de datos
    db_path = tempfile.mkdtemp()
    # Crear una instancia de Embedchain App
    app = embedchain_bot(db_path, openai_access_token)
    # Obtener la URL del video de YouTube del usuario
    video_url = st.text_input("Ingresa la URL del Video de YouTube", type="default")
    # Agregar el video a la base de conocimientos
    if video_url:
        app.add(video_url, data_type="youtube_video")
        st.success(f"¡Se agregó {video_url} a la base de conocimientos!")
        # Hacer una pregunta sobre el video
        prompt = st.text_input("Haz cualquier pregunta sobre el Video de YouTube")
        # Chatear con el video
        if prompt:
            answer = app.chat(prompt)
            st.write(answer)

        