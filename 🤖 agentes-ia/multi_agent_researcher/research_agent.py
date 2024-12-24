# Importar las bibliotecas necesarias
import streamlit as st
from phi.assistant import Assistant
from phi.tools.hackernews import HackerNews
from phi.llm.openai import OpenAIChat

# Configurar la aplicación Streamlit
st.title("Investigador IA Multi-Agente 🔍🤖")
st.caption("Esta aplicación te permite investigar las principales historias y usuarios en HackerNews y escribir blogs, informes y publicaciones sociales.")

# Obtener la clave API de OpenAI del usuario
openai_api_key = st.text_input("Clave API de OpenAI", type="password")

if openai_api_key:
    # Crear instancias del Asistente
    story_researcher = Assistant(
        name="Investigador de Historias de HackerNews",
        role="Investiga historias y usuarios de hackernews.",
        tools=[HackerNews()],
    )

    user_researcher = Assistant(
        name="Investigador de Usuarios de HackerNews",
        role="Lee artículos desde URLs.",
        tools=[HackerNews()],
    )

    hn_assistant = Assistant(
        name="Equipo de Hackernews",
        team=[story_researcher, user_researcher],
        llm=OpenAIChat(
            model="gpt-4o",
            max_tokens=1024,
            temperature=0.5,
            api_key=openai_api_key
        )
    )

    # Campo de entrada para la consulta del informe
    query = st.text_input("Ingresa tu consulta de informe")

    if query:
        # Obtener la respuesta del asistente
        response = hn_assistant.run(query, stream=False)
        st.write(response)