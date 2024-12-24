# Importar las bibliotecas requeridas
import streamlit as st
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.arxiv_toolkit import ArxivToolkit

# Configurar la aplicación Streamlit
st.title("Chat con Artículos de Investigación 🔎🤖")
st.caption("Esta aplicación te permite chatear con artículos de investigación de arXiv usando el modelo OpenAI GPT-4o.")

# Obtener la clave API de OpenAI del usuario
openai_access_token = st.text_input("Clave API de OpenAI", type="password")

# Si se proporciona la clave API de OpenAI, crear una instancia de Assistant
if openai_access_token:
    # Crear una instancia del Assistant
    assistant = Assistant(
    llm=OpenAIChat(
        model="gpt-4o",
        max_tokens=1024,
        temperature=0.9,
        api_key=openai_access_token) , tools=[ArxivToolkit()]
    )

    # Obtener la consulta de búsqueda del usuario
    query= st.text_input("Ingresa la Consulta de Búsqueda", type="default")
    
    if query:
        # Buscar en la web usando el Asistente IA
        response = assistant.run(query, stream=False)
        st.write(response)