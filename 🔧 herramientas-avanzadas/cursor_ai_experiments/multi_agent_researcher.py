import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os

# Inicializar el modelo GPT-4
gpt4_model = None

def create_article_crew(topic):
    # Crear agentes
    researcher = Agent(
        role='Investigador',
        goal='Realizar una investigación exhaustiva sobre el tema dado',
        backstory='Eres un investigador experto con un ojo agudo para los detalles',
        verbose=True,
        allow_delegation=False,
        llm=gpt4_model
    )

    writer = Agent(
        role='Escritor',
        goal='Escribir un artículo detallado y atractivo basado en la investigación, usando el formato markdown adecuado',
        backstory='Eres un escritor hábil con experiencia en crear contenido informativo y formatearlo bellamente en markdown',
        verbose=True,
        allow_delegation=False,
        llm=gpt4_model
    )

    editor = Agent(
        role='Editor',
        goal='Revisar y refinar el artículo para mejorar la claridad, precisión, atractivo y formato markdown adecuado',
        backstory='Eres un editor experimentado con un ojo agudo para el contenido de calidad y excelente estructura markdown',
        verbose=True,
        allow_delegation=False,
        llm=gpt4_model
    )

    # Crear tareas
    research_task = Task(
        description=f"Realizar una investigación exhaustiva sobre el tema: {topic}. Recopilar información clave, estadísticas y opiniones de expertos.",
        agent=researcher,
        expected_output="Un informe de investigación completo sobre el tema dado, incluyendo información clave, estadísticas y opiniones de expertos."
    )

    writing_task = Task(
        description="""Usando la investigación proporcionada, escribe un artículo detallado y atractivo. 
        Asegura una estructura adecuada, fluidez y claridad. Formatea el artículo usando markdown, incluyendo:
        1. Un título principal (H1)
        2. Encabezados de sección (H2)
        3. Encabezados de subsección donde sea apropiado (H3)
        4. Puntos o listas numeradas donde sea relevante
        5. Énfasis en puntos clave usando texto en negrita o cursiva
        Asegúrate de que el contenido esté bien organizado y sea fácil de leer.""",
        agent=writer,
        expected_output="Un artículo bien estructurado, detallado y atractivo basado en la investigación proporcionada, formateado en markdown con encabezados y subencabezados adecuados."
    )

    editing_task = Task(
        description="""Revisar el artículo para mejorar la claridad, precisión, atractivo y formato markdown adecuado. 
        Asegúrate de que:
        1. El formato markdown sea correcto y consistente
        2. Los encabezados y subencabezados se usen apropiadamente
        3. El flujo del contenido sea lógico y atractivo
        4. Los puntos clave estén enfatizados correctamente
        Realiza las ediciones y mejoras necesarias tanto en el contenido como en el formato.""",
        agent=editor,
        expected_output="Una versión final y pulida del artículo con mejor claridad, precisión, atractivo y formato markdown adecuado."
    )

    # Crear el equipo
    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        verbose=2,
        process=Process.sequential
    )

    return crew

# Aplicación Streamlit
st.set_page_config(page_title="Investigador IA Multi-Agente", page_icon="📝")

# CSS personalizado para mejor apariencia
st.markdown("""
    <style>
    .stApp {
        max-width: 1800px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
    }
    .st-bw {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📝 Investigador IA Multi-Agente")

# Barra lateral para entrada de clave API
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Ingresa tu Clave API de OpenAI:", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        gpt4_model = ChatOpenAI(model_name="gpt-4o-mini")
        st.success("¡Clave API configurada exitosamente!")
    else:
        st.info("Por favor, ingresa tu Clave API de OpenAI para continuar.")

# Contenido principal
st.markdown("¡Genera artículos detallados sobre cualquier tema usando agentes de IA!")

topic = st.text_input("Ingresa el tema para el artículo:", placeholder="ej., El Impacto de la Inteligencia Artificial en la Salud")

if st.button("Generar Artículo"):
    if not api_key:
        st.error("Por favor, ingresa tu Clave API de OpenAI en la barra lateral.")
    elif not topic:
        st.warning("Por favor, ingresa un tema para el artículo.")
    else:
        with st.spinner("🤖 Los agentes de IA están trabajando en tu artículo..."):
            crew = create_article_crew(topic)
            result = crew.kickoff()
            st.markdown(result)

st.markdown("---")
st.markdown("Desarrollado con CrewAI y OpenAI :heart:")