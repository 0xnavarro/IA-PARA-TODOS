import streamlit as st
from embedchain import App
import tempfile

# Definir la función embedchain_bot
def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {"provider": "openai", "config": {"model": "gpt-4-turbo", "temperature": 0.5, "api_key": api_key}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},
        }
    )

st.title("Chat con Boletín de Substack 📝")
st.caption("Esta aplicación te permite chatear con un boletín de Substack usando la API de OpenAI")

# Obtener la clave API de OpenAI del usuario
openai_access_token = st.text_input("Clave API de OpenAI", type="password")

if openai_access_token:
    # Crear un directorio temporal para almacenar la base de datos
    db_path = tempfile.mkdtemp()
    # Crear una instancia de Embedchain App
    app = embedchain_bot(db_path, openai_access_token)

    # Obtener la URL del blog de Substack del usuario
    substack_url = st.text_input("Ingresa la URL del Boletín de Substack", type="default")

    if substack_url:
        # Agregar el blog de Substack a la base de conocimientos
        app.add(substack_url, data_type='substack')
        st.success(f"¡Se agregó {substack_url} a la base de conocimientos!")

        # Hacer una pregunta sobre el blog de Substack
        query = st.text_input("¡Haz cualquier pregunta sobre el boletín de Substack!")

        # Consultar el blog de Substack
        if query:
            result = app.query(query)
            st.write(result)
