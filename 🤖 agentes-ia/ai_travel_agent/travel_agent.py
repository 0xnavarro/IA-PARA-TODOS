from textwrap import dedent
from phi.assistant import Assistant
from phi.tools.serpapi_tools import SerpApiTools
import streamlit as st
from phi.llm.openai import OpenAIChat

# Configurar la aplicación Streamlit
st.title("Planificador de Viajes IA ✈️")
st.caption("Planifica tu próxima aventura con el Planificador de Viajes IA investigando y planificando un itinerario personalizado de forma automática usando GPT-4o")

# Obtener la clave API de OpenAI del usuario
openai_api_key = st.text_input("Ingresa la Clave API de OpenAI para acceder a GPT-4o", type="password")

# Obtener la clave API de SerpAPI del usuario
serp_api_key = st.text_input("Ingresa la Clave API de SerpAPI para la funcionalidad de búsqueda", type="password")

if openai_api_key and serp_api_key:
    researcher = Assistant(
        name="Investigador",
        role="Busca destinos de viaje, actividades y alojamientos basados en las preferencias del usuario",
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        description=dedent(
            """\
        Eres un investigador de viajes de clase mundial. Dado un destino de viaje y el número de días que el usuario quiere viajar,
        genera una lista de términos de búsqueda para encontrar actividades y alojamientos de viaje relevantes.
        Luego busca en la web cada término, analiza los resultados y devuelve los 10 resultados más relevantes.
        """
        ),
        instructions=[
            "Dado un destino de viaje y el número de días que el usuario quiere viajar, primero genera una lista de 3 términos de búsqueda relacionados con ese destino y el número de días.",
            "Para cada término de búsqueda, usa `search_google` y analiza los resultados."
            "De los resultados de todas las búsquedas, devuelve los 10 resultados más relevantes para las preferencias del usuario.",
            "Recuerda: la calidad de los resultados es importante.",
        ],
        tools=[SerpApiTools(api_key=serp_api_key)],
        add_datetime_to_instructions=True,
    )
    planner = Assistant(
        name="Planificador",
        role="Genera un borrador de itinerario basado en las preferencias del usuario y los resultados de la investigación",
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        description=dedent(
            """\
        Eres un planificador de viajes senior. Dado un destino de viaje, el número de días que el usuario quiere viajar y una lista de resultados de investigación,
        tu objetivo es generar un borrador de itinerario que cumpla con las necesidades y preferencias del usuario.
        """
        ),
        instructions=[
            "Dado un destino de viaje, el número de días que el usuario quiere viajar y una lista de resultados de investigación, genera un borrador de itinerario que incluya actividades y alojamientos sugeridos.",
            "Asegúrate de que el itinerario esté bien estructurado, sea informativo y atractivo.",
            "Asegúrate de proporcionar un itinerario matizado y equilibrado, citando hechos cuando sea posible.",
            "Recuerda: la calidad del itinerario es importante.",
            "Enfócate en la claridad, coherencia y calidad general.",
            "Nunca inventes hechos ni plagies. Siempre proporciona la atribución adecuada.",
        ],
        add_datetime_to_instructions=True,
        add_chat_history_to_prompt=True,
        num_history_messages=3,
    )

    # Campos de entrada para el destino del usuario y el número de días que quiere viajar
    destination = st.text_input("¿A dónde quieres ir?")
    num_days = st.number_input("¿Cuántos días quieres viajar?", min_value=1, max_value=30, value=7)

    if st.button("Generar Itinerario"):
        with st.spinner("Procesando..."):
            # Obtener la respuesta del asistente
            response = planner.run(f"{destination} por {num_days} días", stream=False)
            st.write(response)