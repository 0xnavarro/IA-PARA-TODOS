# Importar las bibliotecas requeridas
import streamlit as st
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from phi.tools.arxiv_toolkit import ArxivToolkit

# Configurar la aplicación Streamlit
st.title("Chat con Artículos de Investigación 🔎🤖")
st.caption("Esta aplicación te permite chatear con artículos de investigación de arXiv usando Llama-3 ejecutándose localmente.")

# Crear una instancia del Assistant
assistant = Assistant(
llm=Ollama(
    model="llama3:instruct") , tools=[ArxivToolkit()], show_tool_calls=True
)

# Obtener la consulta de búsqueda del usuario
query= st.text_input("Ingresa la Consulta de Búsqueda", type="default")

if query:
    # Buscar en la web usando el Asistente IA
    response = assistant.run(query, stream=False)
    st.write(response)