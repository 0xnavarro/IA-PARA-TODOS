# Importar las bibliotecas necesarias
import streamlit as st
from phi.assistant import Assistant
from phi.tools.hackernews import HackerNews
from phi.llm.ollama import Ollama

# Configurar la aplicación Streamlit
st.title("Investigador IA Multi-Agente usando Llama-3 🔍🤖")
st.caption("Esta aplicación te permite investigar las principales historias y usuarios en HackerNews y escribir blogs, informes y publicaciones sociales.")

# Crear instancias del Asistente
story_researcher = Assistant(
    name="Investigador de Historias de HackerNews",
    role="Investiga historias y usuarios de hackernews.",
    tools=[HackerNews()],
    llm=Ollama(model="llama3:instruct", max_tokens=1024)
)

user_researcher = Assistant(
    name="Investigador de Usuarios de HackerNews",
    role="Lee artículos desde URLs.",
    tools=[HackerNews()],
    llm=Ollama(model="llama3:instruct", max_tokens=1024)
)

hn_assistant = Assistant(
    name="Equipo de Hackernews",
    team=[story_researcher, user_researcher],
    llm=Ollama(model="llama3:instruct", max_tokens=1024)
)

# Campo de entrada para la consulta del informe
query = st.text_input("Ingresa tu consulta de informe")

if query:
    # Obtener la respuesta del asistente
    response = hn_assistant.run(query, stream=False)
    st.write(response)