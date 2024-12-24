import tempfile
import streamlit as st
from embedchain import App

# Definir la función embedchain_bot
def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {"provider": "openai", "config": {"model": "gpt-4-turbo", "temperature": 0.5, "api_key": api_key}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},
        }
    )

# Crear aplicación Streamlit
st.title("Chat con tu Bandeja de Gmail 📧")
st.caption("Esta aplicación te permite chatear con tu bandeja de Gmail usando la API de OpenAI")

# Obtener la clave API de OpenAI del usuario
openai_access_token = st.text_input("Ingresa tu Clave API de OpenAI", type="password")

# Establecer el filtro de Gmail estáticamente
gmail_filter = "to: me label:inbox"

# Agregar los datos de Gmail a la base de conocimientos si se proporciona la clave API de OpenAI
if openai_access_token:
    # Crear un directorio temporal para almacenar la base de datos
    db_path = tempfile.mkdtemp()
    # Crear una instancia de Embedchain App
    app = embedchain_bot(db_path, openai_access_token)
    app.add(gmail_filter, data_type="gmail")
    st.success(f"¡Se agregaron los correos de la Bandeja de entrada a la base de conocimientos!")

    # Hacer una pregunta sobre los correos
    prompt = st.text_input("Haz cualquier pregunta sobre tus correos")

    # Chatear con los correos
    if prompt:
        answer = app.query(prompt)
        st.write(answer)