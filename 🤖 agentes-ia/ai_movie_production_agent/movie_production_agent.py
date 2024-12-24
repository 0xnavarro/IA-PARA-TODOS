# Importar las bibliotecas necesarias
import streamlit as st
from phi.assistant import Assistant
from phi.tools.serpapi_tools import SerpApiTools
from phi.llm.anthropic import Claude
from textwrap import dedent

# Configurar la aplicación Streamlit
st.title("Agente de Producción de Películas IA 🎬")
st.caption("Da vida a tus ideas cinematográficas con los equipos de escritura de guiones y casting de agentes IA")

# Obtener la clave API de Anthropic del usuario
anthropic_api_key = st.text_input("Ingresa la Clave API de Anthropic para acceder a Claude Sonnet 3.5", type="password")
# Obtener la clave API de SerpAPI del usuario
serp_api_key = st.text_input("Ingresa la Clave API de SerpAPI para la funcionalidad de búsqueda", type="password")

if anthropic_api_key and serp_api_key:
    script_writer = Assistant(
        name="Guionista",
        llm=Claude(model="claude-3-5-sonnet-20240620", api_key=anthropic_api_key),
        description=dedent(
            """\
        Eres un experto en escritura de guiones. Dada una idea de película y género,
        desarrolla un esquema de guion atractivo con descripciones de personajes y puntos clave de la trama.
        """
        ),
        instructions=[
            "Escribe un esquema de guion con 3-5 personajes principales y puntos clave de la trama.",
            "Esquematiza la estructura de tres actos y sugiere 2-3 giros.",
            "Asegúrate de que el guion se alinee con el género especificado y el público objetivo.",
        ],
    )

    casting_director = Assistant(
        name="Director de Casting",
        llm=Claude(model="claude-3-5-sonnet-20240620", api_key=anthropic_api_key),
        description=dedent(
            """\
        Eres un talentoso director de casting. Dado un esquema de guion y descripciones de personajes,
        sugiere actores adecuados para los roles principales, considerando sus actuaciones pasadas y disponibilidad actual.
        """
        ),
        instructions=[
            "Sugiere 2-3 actores para cada rol principal.",
            "Verifica el estado actual de los actores usando `search_google`.",
            "Proporciona una breve explicación para cada sugerencia de casting.",
            "Considera la diversidad y representación en tus elecciones de casting.",
        ],
        tools=[SerpApiTools(api_key=serp_api_key)],
    )

    movie_producer = Assistant(
        name="Productor de Películas",
        llm=Claude(model="claude-3-5-sonnet-20240620", api_key=anthropic_api_key),
        team=[script_writer, casting_director],
        description="Productor de películas experimentado supervisando guion y casting.",
        instructions=[
            "Pide al Guionista un esquema de guion basado en la idea de película.",
            "Pasa el esquema al Director de Casting para sugerencias de casting.",
            "Resume el esquema de guion y las sugerencias de casting.",
            "Proporciona una visión general concisa del concepto de la película.",
        ],
        markdown=True,
    )

    # Campo de entrada para la consulta del informe
    movie_idea = st.text_area("Describe tu idea de película en unas pocas oraciones:")
    genre = st.selectbox("Selecciona el género de la película:",
                         ["Acción", "Comedia", "Drama", "Ciencia Ficción", "Terror", "Romance", "Suspenso"])
    target_audience = st.selectbox("Selecciona el público objetivo:",
                                   ["General", "Niños", "Adolescentes", "Adultos", "Maduro"])
    estimated_runtime = st.slider("Duración estimada (en minutos):", 60, 180, 120)

    # Procesar el concepto de la película
    if st.button("Desarrollar Concepto de Película"):
        with st.spinner("Desarrollando concepto de película..."):
            input_text = (
                f"Idea de película: {movie_idea}, Género: {genre}, "
                f"Público objetivo: {target_audience}, Duración estimada: {estimated_runtime} minutos"
            )
            # Obtener la respuesta del asistente
            response = movie_producer.run(input_text, stream=False)
            st.write(response)