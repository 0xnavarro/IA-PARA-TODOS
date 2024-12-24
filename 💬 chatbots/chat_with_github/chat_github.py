# Importar las bibliotecas requeridas
from embedchain.pipeline import Pipeline as App
from embedchain.loaders.github import GithubLoader
import streamlit as st
import os

loader = GithubLoader(
    config={
        "token":"Tu Token de GitHub",
        }
    )

# Crear aplicación Streamlit
st.title("Chat con Repositorio de GitHub 💬")
st.caption("Esta aplicación te permite chatear con un Repositorio de GitHub usando la API de OpenAI")

# Obtener la clave API de OpenAI del usuario
openai_access_token = st.text_input("Clave API de OpenAI", type="password")

# Si se proporciona la clave API de OpenAI, crear una instancia de App
if openai_access_token:
    os.environ["OPENAI_API_KEY"] = openai_access_token
    # Crear una instancia de Embedchain App
    app = App()
    # Obtener el repositorio de GitHub del usuario
    git_repo = st.text_input("Ingresa el Repositorio de GitHub", type="default")
    if git_repo:
        # Agregar el repositorio a la base de conocimientos
        app.add("repo:" + git_repo + " " + "type:repo", data_type="github", loader=loader)
        st.success(f"¡Se agregó {git_repo} a la base de conocimientos!")
        # Hacer una pregunta sobre el Repositorio de GitHub
        prompt = st.text_input("Haz cualquier pregunta sobre el Repositorio de GitHub")
        # Chatear con el Repositorio de GitHub
        if prompt:
            answer = app.chat(prompt)
            st.write(answer)