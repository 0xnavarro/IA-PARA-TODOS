# Importar las bibliotecas requeridas
from textwrap import dedent
from phi.assistant import Assistant
from phi.tools.serpapi_tools import SerpApiTools
from phi.tools.newspaper4k import Newspaper4k as NewspaperToolkit
import streamlit as st
from phi.llm.openai import OpenAIChat

# Configurar la aplicación Streamlit
st.title("Agente Periodista IA 🗞️")
st.caption("Genera artículos de alta calidad con el Periodista IA investigando, escribiendo y editando artículos de calidad de forma automática usando GPT-4o")

# Obtener la clave API de OpenAI del usuario
openai_api_key = st.text_input("Ingresa la Clave API de OpenAI para acceder a GPT-4o", type="password")

# Obtener la clave API de SerpAPI del usuario
serp_api_key = st.text_input("Ingresa la Clave API de SerpAPI para la funcionalidad de búsqueda", type="password")

if openai_api_key and serp_api_key:
    searcher = Assistant(
        name="Buscador",
        role="Busca las mejores URLs basadas en un tema",
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        description=dedent(
            """\
        Eres un periodista de clase mundial para el New York Times. Dado un tema, genera una lista de 3 términos de búsqueda
        para escribir un artículo sobre ese tema. Luego busca en la web cada término, analiza los resultados
        y devuelve las 10 URLs más relevantes.
        """
        ),
        instructions=[
            "Dado un tema, primero genera una lista de 3 términos de búsqueda relacionados con ese tema.",
            "Para cada término de búsqueda, usa `search_google` y analiza los resultados."
            "De los resultados de todas las búsquedas, devuelve las 10 URLs más relevantes para el tema.",
            "Recuerda: estás escribiendo para el New York Times, por lo que la calidad de las fuentes es importante.",
        ],
        tools=[SerpApiTools(api_key=serp_api_key)],
        add_datetime_to_instructions=True,
    )
    writer = Assistant(
        name="Escritor",
        role="Recupera texto de URLs y escribe un artículo de alta calidad",
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        description=dedent(
            """\
        Eres un escritor senior para el New York Times. Dado un tema y una lista de URLs,
        tu objetivo es escribir un artículo de alta calidad digno del NYT sobre el tema.
        """
        ),
        instructions=[
            "Dado un tema y una lista de URLs, primero lee el artículo usando `get_article_text`."
            "Luego escribe un artículo de alta calidad digno del NYT sobre el tema."
            "El artículo debe estar bien estructurado, ser informativo y atractivo",
            "Asegúrate de que la longitud sea al menos tan larga como una historia de portada del NYT -- como mínimo, 15 párrafos.",
            "Asegúrate de proporcionar una opinión matizada y equilibrada, citando hechos cuando sea posible.",
            "Recuerda: estás escribiendo para el New York Times, por lo que la calidad del artículo es importante.",
            "Enfócate en la claridad, coherencia y calidad general.",
            "Nunca inventes hechos ni plagies. Siempre proporciona la atribución adecuada.",
        ],
        tools=[NewspaperToolkit()],
        add_datetime_to_instructions=True,
        add_chat_history_to_prompt=True,
        num_history_messages=3,
    )

    editor = Assistant(
        name="Editor",
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        team=[searcher, writer],
        description="Eres un editor senior del NYT. Dado un tema, tu objetivo es escribir un artículo digno del NYT.",
        instructions=[
            "Dado un tema, pide al periodista de búsqueda que busque las URLs más relevantes para ese tema.",
            "Luego pasa una descripción del tema y las URLs al escritor para obtener un borrador del artículo.",
            "Edita, revisa y refina el artículo para asegurar que cumpla con los altos estándares del New York Times.",
            "El artículo debe ser extremadamente articulado y bien escrito. "
            "Enfócate en la claridad, coherencia y calidad general.",
            "Asegúrate de que el artículo sea atractivo e informativo.",
            "Recuerda: eres el guardián final antes de que se publique el artículo.",
        ],
        add_datetime_to_instructions=True,
        markdown=True,
    )

    # Campo de entrada para la consulta del informe
    query = st.text_input("¿Sobre qué tema quieres que el periodista IA escriba un artículo?")

    if query:
        with st.spinner("Procesando..."):
            # Obtener la respuesta del asistente
            response = editor.run(query, stream=False)
            st.write(response)