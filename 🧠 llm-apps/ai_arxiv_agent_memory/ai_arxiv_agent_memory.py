import streamlit as st
import os
from mem0 import Memory
from multion.client import MultiOn
from openai import OpenAI

st.title("Agente de Investigación IA con Memoria 📚")

api_keys = {k: st.text_input(f"Clave API de {k.capitalize()}", type="password") for k in ['openai', 'multion']}

if all(api_keys.values()):
    os.environ['OPENAI_API_KEY'] = api_keys['openai']
    # Inicializar Mem0 con Qdrant
    config = {
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "model": "gpt-4o-mini",
                "host": "localhost",
                "port": 6333,
            }
        },
    }
    memory, multion, openai_client = Memory.from_config(config), MultiOn(api_key=api_keys['multion']), OpenAI(api_key=api_keys['openai'])

    user_id = st.sidebar.text_input("Ingresa tu Nombre de Usuario")
    #user_interests = st.text_area("Intereses de investigación y antecedentes")

    search_query = st.text_input("Consulta de búsqueda de artículos de investigación")

    def process_with_gpt4(result):
        prompt = f"""
        Basado en el siguiente resultado de búsqueda de arXiv, proporciona una salida estructurada en markdown que sea legible para los usuarios. 
        Cada artículo debe tener un título, autores, resumen y enlace.
        Resultado de Búsqueda: {result}
        Formato de Salida: Tabla con las siguientes columnas: [{{"title": "Título del Artículo", "authors": "Nombres de Autores", "abstract": "Resumen breve", "link": "Enlace arXiv"}}, ...]
        """
        response = openai_client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.2)
        return response.choices[0].message.content

    if st.button('Buscar Artículos'):
        with st.spinner('Buscando y Procesando...'):
            relevant_memories = memory.search(search_query, user_id=user_id, limit=3)
            prompt = f"Buscar artículos en arXiv: {search_query}\nAntecedentes del usuario: {' '.join(mem['text'] for mem in relevant_memories)}"
            result = process_with_gpt4(multion.browse(cmd=prompt, url="https://arxiv.org/"))
            st.markdown(result)

    if st.sidebar.button("Ver Memoria"):
        st.sidebar.write("\n".join([f"- {mem['text']}" for mem in memory.get_all(user_id=user_id)]))

else:
    st.warning("Por favor ingresa tus claves API para usar esta aplicación.")