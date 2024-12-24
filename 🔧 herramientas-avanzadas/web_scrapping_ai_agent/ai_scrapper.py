# Importar las bibliotecas requeridas
import streamlit as st
from scrapegraphai.graphs import SmartScraperGraph

# Configurar la aplicación Streamlit
st.title("Agente IA de Web Scraping 🕵️‍♂️")
st.caption("Esta aplicación te permite hacer scraping de un sitio web usando la API de OpenAI")

# Obtener la clave API de OpenAI del usuario
openai_access_token = st.text_input("Clave API de OpenAI", type="password")

if openai_access_token:
    model = st.radio(
        "Selecciona el modelo",
        ["gpt-3.5-turbo", "gpt-4"],
        index=0,
    )    
    graph_config = {
        "llm": {
            "api_key": openai_access_token,
            "model": model,
        },
    }
    # Obtener la URL del sitio web para hacer scraping
    url = st.text_input("Ingresa la URL del sitio web que deseas analizar")
    # Obtener el prompt del usuario
    user_prompt = st.text_input("¿Qué quieres que el agente IA extraiga del sitio web?")
    
    # Crear un objeto SmartScraperGraph
    smart_scraper_graph = SmartScraperGraph(
        prompt=user_prompt,
        source=url,
        config=graph_config
    )
    # Hacer scraping del sitio web
    if st.button("Analizar"):
        result = smart_scraper_graph.run()
        st.write(result)