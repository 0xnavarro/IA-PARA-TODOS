import streamlit as st
import os
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from phi.tools.yfinance import YFinanceTools
from phi.tools.serpapi_tools import SerpApiTools

st.set_page_config(page_title="Uso de Herramientas con Llama-3", page_icon="🦙")

# Asegurar que SERPAPI_API_KEY esté configurada
if 'SERPAPI_API_KEY' not in os.environ:
    st.error("Por favor, configura la variable de entorno SERPAPI_API_KEY.")
    st.stop()

def get_assistant(tools):
    return Assistant(
        name="llama3_assistant",
        llm=Ollama(model="llama3"),
        tools=tools,
        description="Eres un asistente útil que puede acceder a herramientas específicas basadas en la selección del usuario.",
        show_tool_calls=True,
        debug_mode=True,
        # Esta configuración agrega la fecha y hora actual a las instrucciones
        add_datetime_to_instructions=True,

    )

st.title("🦙 Uso de Herramientas con Llama-3 Local")
st.markdown("""
Esta aplicación demuestra el llamado a funciones con el modelo Llama3 local usando Ollama.
¡Selecciona las herramientas en la barra lateral y haz preguntas relevantes!
""")

# Barra lateral para selección de herramientas
st.sidebar.title("Selección de Herramientas")
use_yfinance = st.sidebar.checkbox("YFinance (Datos Bursátiles)", value=True)
use_serpapi = st.sidebar.checkbox("SerpAPI (Búsqueda Web)", value=True)

# Inicializar o actualizar el asistente basado en las herramientas seleccionadas
tools = []
if use_yfinance:
    tools.append(YFinanceTools(stock_price=True, company_info=True))
if use_serpapi:
    tools.append(SerpApiTools())

if "assistant" not in st.session_state or st.session_state.get("tools") != tools:
    st.session_state.assistant = get_assistant(tools)
    st.session_state.tools = tools
    st.session_state.messages = []  # Reiniciar mensajes cuando cambian las herramientas

# Mostrar estado actual de las herramientas
st.sidebar.markdown("### Herramientas Actuales:")
st.sidebar.markdown(f"- YFinance: {'Habilitado' if use_yfinance else 'Deshabilitado'}")
st.sidebar.markdown(f"- SerpAPI: {'Habilitado' if use_serpapi else 'Deshabilitado'}")

# Interfaz de chat
for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Haz una pregunta basada en las herramientas habilitadas"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()
        response = ""
        for chunk in st.session_state.assistant.run(prompt):
            response += chunk
            response_container.write(response + "▌")
        response_container.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Instrucciones en la barra lateral
st.sidebar.markdown("""
### Cómo usar:
1. Selecciona las herramientas que quieres usar en la barra lateral
2. Haz preguntas relacionadas con las herramientas habilitadas
3. El asistente usará solo las herramientas seleccionadas para responder

### Nota:
Asegúrate de haber configurado la variable de entorno SERPAPI_API_KEY para usar la herramienta SerpAPI.
""")

st.sidebar.markdown("""
### Preguntas de ejemplo:
- YFinance: "¿Cuál es el precio actual de AAPL?"
- SerpAPI: "¿Cuáles son los últimos desarrollos en IA?"
- Ambas: "Compara el precio de las acciones de TSLA con las noticias recientes sobre el rendimiento de Tesla"
""")
