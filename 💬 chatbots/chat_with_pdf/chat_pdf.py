import os
import tempfile
import streamlit as st
from embedchain import App

def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {"provider": "openai", "config": {"api_key": api_key}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},
        }
    )

st.title("Chat con PDF")

openai_access_token = st.text_input("Clave API de OpenAI", type="password")

if openai_access_token:
    db_path = tempfile.mkdtemp()
    app = embedchain_bot(db_path, openai_access_token)

    pdf_file = st.file_uploader("Sube un archivo PDF", type="pdf")

    if pdf_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(pdf_file.getvalue())
            app.add(f.name, data_type="pdf_file")
        os.remove(f.name)
        st.success(f"¡Se agregó {pdf_file.name} a la base de conocimientos!")

    prompt = st.text_input("Haz una pregunta sobre el PDF")

    if prompt:
        answer = app.chat(prompt)
        st.write(answer)

        