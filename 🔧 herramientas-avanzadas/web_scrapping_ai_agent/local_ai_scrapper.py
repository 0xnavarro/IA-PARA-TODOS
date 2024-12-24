# Importar las bibliotecas requeridas
import streamlit as st
from scrapegraphai.graphs import SmartScraperGraph

# Configurar la aplicación Streamlit
st.title("Agente IA de Web Scraping 🕵️‍♂️")
st.caption("Esta aplicación te permite hacer scraping de un sitio web usando Llama 3.2")

# Configurar la configuración para el SmartScraperGraph
graph_config = {
    "llm": {
        "model": "ollama/llama3.2",
        "temperature": 0,
        "format": "json",  # Ollama necesita que el formato se especifique explícitamente
        "base_url": "http://localhost:11434",  # establecer URL de Ollama
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "base_url": "http://localhost:11434",  # establecer URL de Ollama
    },
    "verbose": True,
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