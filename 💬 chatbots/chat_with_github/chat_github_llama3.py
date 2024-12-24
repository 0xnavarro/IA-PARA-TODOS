# Importar las bibliotecas requeridas
import tempfile
from embedchain import App
from embedchain.loaders.github import GithubLoader
import streamlit as st
import os

GITHUB_TOKEN = os.getenv("Tu Token de GitHub")

def get_loader():
    loader = GithubLoader(
        config={
            "token": GITHUB_TOKEN
        }
    )
    return loader

if "loader" not in st.session_state:
    st.session_state['loader'] = get_loader()

loader = st.session_state.loader

# Definir la función embedchain_bot
def embedchain_bot(db_path):
    return App.from_config(
        config={
            "llm": {"provider": "ollama", "config": {"model": "llama3:instruct", "max_tokens": 250, "temperature": 0.5, "stream": True, "base_url": 'http://localhost:11434'}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "ollama", "config": {"model": "llama3:instruct", "base_url": 'http://localhost:11434'}},
        }
    )

def load_repo(git_repo):
    global app
    # Agregar el repositorio a la base de conocimientos
    print(f"¡Agregando {git_repo} a la base de conocimientos!")
    app.add("repo:" + git_repo + " " + "type:repo", data_type="github", loader=loader)
    st.success(f"¡Se agregó {git_repo} a la base de conocimientos!")


def make_db_path():
    ret = tempfile.mkdtemp(suffix="chroma")
    print(f"Base de datos Chroma creada en {ret}")    
    return ret

# Crear aplicación Streamlit
st.title("Chat con Repositorio de GitHub 💬")
st.caption("Esta aplicación te permite chatear con un Repositorio de GitHub usando Llama-3 ejecutándose con Ollama")

# Inicializar la aplicación Embedchain
if "app" not in st.session_state:
    st.session_state['app'] = embedchain_bot(make_db_path())

app = st.session_state.app

# Obtener el repositorio de GitHub del usuario
git_repo = st.text_input("Ingresa el Repositorio de GitHub", type="default")

if git_repo and ("repos" not in st.session_state or git_repo not in st.session_state.repos):
    if "repos" not in st.session_state:
        st.session_state["repos"] = [git_repo]
    else:
        st.session_state.repos.append(git_repo)
    load_repo(git_repo)


# Hacer una pregunta sobre el Repositorio de GitHub
prompt = st.text_input("Haz cualquier pregunta sobre el Repositorio de GitHub")
# Chatear con el Repositorio de GitHub
if prompt:
    answer = st.session_state.app.chat(prompt)
    st.write(answer)