from textwrap import dedent
from phi.assistant import Assistant
from phi.tools.serpapi_tools import SerpApiTools
import streamlit as st
from phi.llm.openai import OpenAIChat

# Configurar la aplicación Streamlit
st.title("Planificador de Finanzas Personales IA 💰")
st.caption("Gestiona tus finanzas con el Planificador de Finanzas Personales IA creando presupuestos personalizados, planes de inversión y estrategias de ahorro usando GPT-4o")

# Obtener la clave API de OpenAI del usuario
openai_api_key = st.text_input("Ingresa la Clave API de OpenAI para acceder a GPT-4o", type="password")

# Obtener la clave API de SerpAPI del usuario
serp_api_key = st.text_input("Ingresa la Clave API de SerpAPI para la funcionalidad de búsqueda", type="password")

if openai_api_key and serp_api_key:
    researcher = Assistant(
        name="Investigador",
        role="Busca asesoramiento financiero, oportunidades de inversión y estrategias de ahorro basadas en las preferencias del usuario",
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        description=dedent(
            """\
        Eres un investigador financiero de clase mundial. Dadas las metas financieras de un usuario y su situación financiera actual,
        genera una lista de términos de búsqueda para encontrar asesoramiento financiero relevante, oportunidades de inversión y estrategias de ahorro.
        Luego busca en la web cada término, analiza los resultados y devuelve los 10 resultados más relevantes.
        """
        ),
        instructions=[
            "Dadas las metas financieras de un usuario y su situación financiera actual, primero genera una lista de 3 términos de búsqueda relacionados con esas metas.",
            "Para cada término de búsqueda, usa `search_google` y analiza los resultados.",
            "De los resultados de todas las búsquedas, devuelve los 10 resultados más relevantes para las preferencias del usuario.",
            "Recuerda: la calidad de los resultados es importante.",
        ],
        tools=[SerpApiTools(api_key=serp_api_key)],
        add_datetime_to_instructions=True,
    )
    planner = Assistant(
        name="Planificador",
        role="Genera un plan financiero personalizado basado en las preferencias del usuario y los resultados de la investigación",
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        description=dedent(
            """\
        Eres un planificador financiero senior. Dadas las metas financieras de un usuario, su situación financiera actual y una lista de resultados de investigación,
        tu objetivo es generar un plan financiero personalizado que cumpla con las necesidades y preferencias del usuario.
        """
        ),
        instructions=[
            "Dadas las metas financieras de un usuario, su situación financiera actual y una lista de resultados de investigación, genera un plan financiero personalizado que incluya presupuestos sugeridos, planes de inversión y estrategias de ahorro.",
            "Asegúrate de que el plan esté bien estructurado, sea informativo y atractivo.",
            "Asegúrate de proporcionar un plan matizado y equilibrado, citando hechos cuando sea posible.",
            "Recuerda: la calidad del plan es importante.",
            "Enfócate en la claridad, coherencia y calidad general.",
            "Nunca inventes hechos ni plagies. Siempre proporciona la atribución adecuada.",
        ],
        add_datetime_to_instructions=True,
        add_chat_history_to_prompt=True,
        num_history_messages=3,
    )

    # Campos de entrada para las metas financieras del usuario y su situación financiera actual
    financial_goals = st.text_input("¿Cuáles son tus metas financieras?")
    current_situation = st.text_area("Describe tu situación financiera actual")

    if st.button("Generar Plan Financiero"):
        with st.spinner("Procesando..."):
            # Obtener la respuesta del asistente
            response = planner.run(f"Metas financieras: {financial_goals}, Situación actual: {current_situation}", stream=False)
            st.write(response)
