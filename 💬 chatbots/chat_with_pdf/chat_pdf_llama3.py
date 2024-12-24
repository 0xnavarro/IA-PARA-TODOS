# Importar bibliotecas necesarias
import os
import tempfile
import streamlit as st
from embedchain import App

# Definir la función embedchain_bot
def embedchain_bot(db_path):
    return App.from_config(
        config={
            "llm": {"provider": "ollama", "config": {"model": "llama3:instruct", "max_tokens": 250, "temperature": 0.5, "stream": True, "base_url": 'http://localhost:11434'}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "ollama", "config": {"model": "llama3:instruct", "base_url": 'http://localhost:11434'}},
        }
    )

st.title("Chat con PDF")
st.caption("¡Esta aplicación te permite chatear con un PDF usando Llama3 ejecutándose localmente con Ollama!")

# Crear un directorio temporal para almacenar el archivo PDF
db_path = tempfile.mkdtemp()
# Crear una instancia de la aplicación embedchain
app = embedchain_bot(db_path)

# Subir un archivo PDF
pdf_file = st.file_uploader("Sube un archivo PDF", type="pdf")

# Si se sube un archivo PDF, agregarlo a la base de conocimientos
if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(pdf_file.getvalue())
        app.add(f.name, data_type="pdf_file")
    os.remove(f.name)
    st.success(f"¡Se agregó {pdf_file.name} a la base de conocimientos!")

# Hacer una pregunta sobre el PDF
prompt = st.text_input("Haz una pregunta sobre el PDF")
# Mostrar la respuesta
if prompt:
    answer = app.chat(prompt)
    st.write(answer)