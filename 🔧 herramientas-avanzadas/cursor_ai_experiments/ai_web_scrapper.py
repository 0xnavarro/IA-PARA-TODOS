import streamlit as st
from scrapegraphai.graphs import SmartScraperGraph

# Título de la aplicación Streamlit
st.title("Scraper Web con IA")

# Campos de entrada para el prompt del usuario y URL fuente
prompt = st.text_input("Ingresa la información que deseas extraer:")
source_url = st.text_input("Ingresa la URL fuente:")

# Campo de entrada para la clave API de OpenAI
api_key = st.text_input("Ingresa tu clave API de OpenAI:", type="password")

# Configuración para el pipeline de scraping
graph_config = {
    "llm": {
        "api_key": api_key,
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": False,
}

# Botón para iniciar el proceso de scraping
if st.button("Extraer"):
    if prompt and source_url and api_key:
        # Crear la instancia de SmartScraperGraph
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source_url,
            config=graph_config
        )

        # Ejecutar el pipeline
        result = smart_scraper_graph.run()

        # Mostrar el resultado
        st.write(result)
    else:
        st.error("Por favor, proporciona todos los campos requeridos.")

# Instrucciones para el usuario
st.markdown("""
### Instrucciones
1. Ingresa la información que deseas extraer en el primer campo.
2. Ingresa la URL fuente de donde quieres extraer la información.
3. Ingresa tu clave API de OpenAI.
4. Haz clic en el botón "Extraer" para iniciar el proceso de scraping.
""")