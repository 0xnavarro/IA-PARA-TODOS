import streamlit as st
from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.anthropic import Claude
from phi.tools.newspaper4k import Newspaper4k
from phi.tools import Tool
import logging

logging.basicConfig(level=logging.DEBUG)

# Configuración de la aplicación Streamlit
st.title("Agente de Análisis de Tendencias de Startups IA 📈")
st.caption("¡Obtén el último análisis de tendencias y oportunidades de startups basado en tu tema de interés con un clic!")

topic = st.text_input("Ingresa el área de interés para tu Startup:")
anthropic_api_key = st.sidebar.text_input("Ingresa la Clave API de Anthropic", type="password")

if st.button("Generar Análisis"):
    if not anthropic_api_key:
        st.warning("Por favor, ingresa la clave API requerida.")
    else:
        with st.spinner("Procesando tu solicitud..."):
            try:
                # Inicializar modelo Anthropic
                anthropic_model = Claude(id ="claude-3-5-sonnet-20240620",api_key=anthropic_api_key)

                # Definir Agente Recolector de Noticias - La herramienta Duckduckgo_search permite a un Agente buscar información en la web.
                search_tool = DuckDuckGo(search=True, news=True, fixed_max_results=5)
                news_collector = Agent(
                    name="Recolector de Noticias",
                    role="Recopila artículos recientes sobre el tema dado",
                    tools=[search_tool],
                    model=anthropic_model,
                    instructions=["Recopilar los últimos artículos sobre el tema"],
                    show_tool_calls=True,
                    markdown=True,
                )

                # Definir Agente Escritor de Resúmenes
                news_tool = Newspaper4k(read_article=True, include_summary=True)
                summary_writer = Agent(
                    name="Escritor de Resúmenes",
                    role="Resume los artículos de noticias recopilados",
                    tools=[news_tool],
                    model=anthropic_model,
                    instructions=["Proporcionar resúmenes concisos de los artículos"],
                    show_tool_calls=True,
                    markdown=True,
                )

                # Definir Agente Analizador de Tendencias
                trend_analyzer = Agent(
                    name="Analizador de Tendencias",
                    role="Analiza tendencias de los resúmenes",
                    model=anthropic_model,
                    instructions=["Identificar tendencias emergentes y oportunidades de startups"],
                    show_tool_calls=True,
                    markdown=True,
                )

                # Configuración del equipo multi-agente de phidata:
                agent_team = Agent(
                    agents=[news_collector, summary_writer, trend_analyzer],
                    instructions=[
                        "Primero, busca en DuckDuckGo artículos recientes relacionados con el tema especificado por el usuario.",
                        "Luego, proporciona los enlaces de artículos recopilados al escritor de resúmenes.",
                        "Importante: debes asegurarte de que el escritor de resúmenes reciba todos los enlaces de artículos para leer.",
                        "Después, el escritor de resúmenes leerá los artículos y preparará resúmenes concisos de cada uno.",
                        "Después de resumir, los resúmenes se pasarán al analizador de tendencias.",
                        "Finalmente, el analizador de tendencias identificará tendencias emergentes y oportunidades potenciales de startups basadas en los resúmenes proporcionados en forma de Informe detallado para que cualquier emprendedor joven pueda obtener un valor increíble leyendo esto fácilmente"
                    ],
                    show_tool_calls=True,
                    markdown=True,
                )

                # Ejecutando el flujo de trabajo
                # Paso 1: Recolectar noticias
                news_response = news_collector.run(f"Recolectar noticias recientes sobre {topic}")
                articles = news_response.content

                # Paso 2: Resumir artículos
                summary_response = summary_writer.run(f"Resumir los siguientes artículos:\n{articles}")
                summaries = summary_response.content

                # Paso 3: Analizar tendencias
                trend_response = trend_analyzer.run(f"Analizar tendencias de los siguientes resúmenes:\n{summaries}")
                analysis = trend_response.content

                # Mostrar resultados - si en caso quieres usar esto más adelante, ¡puedes descomentar las siguientes 2 líneas para obtener los resúmenes también!
                # st.subheader("Resúmenes de Noticias")
                # # st.write(summaries)

                st.subheader("Análisis de Tendencias y Oportunidades Potenciales de Startups")
                st.write(analysis)

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
else:
    st.info("Ingresa el tema y las claves API, luego haz clic en 'Generar Análisis' para comenzar.")
