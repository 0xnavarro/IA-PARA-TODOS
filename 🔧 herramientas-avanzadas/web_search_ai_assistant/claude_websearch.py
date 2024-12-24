# Importar las bibliotecas requeridas
import streamlit as st
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm.anthropic import Claude

# Configurar la aplicación Streamlit
st.title("Claude Sonnet + Búsqueda Web con IA 🤖")
st.caption("Esta aplicación te permite buscar en la web usando Claude Sonnet 3.5")

# Obtener la clave API de Anthropic del usuario
anthropic_api_key = st.text_input("Clave API de Claude de Anthropic", type="password")

# Si se proporciona la clave API de Anthropic, crear una instancia de Assistant
if anthropic_api_key:
    assistant = Assistant(
    llm=Claude(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0.9,
        api_key=anthropic_api_key) , tools=[DuckDuckGo()], show_tool_calls=True
    )
    # Obtener la consulta de búsqueda del usuario
    query= st.text_input("Ingresa la Consulta de Búsqueda", type="default")
    
    if query:
        # Buscar en la web usando el Asistente IA
        response = assistant.run(query, stream=False)
        st.write(response)