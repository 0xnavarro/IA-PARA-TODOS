import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai.process import Process
from crewai_tools import SerperDevTool
import os

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Agente de Reuniones IA 📝", layout="wide")
st.title("Agente de Preparación de Reuniones IA 📝")

# Barra lateral para claves API
st.sidebar.header("Claves API")
anthropic_api_key = st.sidebar.text_input("Clave API de Anthropic", type="password")
serper_api_key = st.sidebar.text_input("Clave API de Serper", type="password")

# Verificar si todas las claves API están configuradas
if anthropic_api_key and serper_api_key:
    # # Establecer claves API como variables de entorno
    os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
    os.environ["SERPER_API_KEY"] = serper_api_key

    claude = LLM(model="claude-3-5-sonnet-20240620", temperature= 0.7, api_key=anthropic_api_key)
    search_tool = SerperDevTool()

    # Campos de entrada
    company_name = st.text_input("Ingresa el nombre de la empresa:")
    meeting_objective = st.text_input("Ingresa el objetivo de la reunión:")
    attendees = st.text_area("Ingresa los asistentes y sus roles (uno por línea):")
    meeting_duration = st.number_input("Ingresa la duración de la reunión (en minutos):", min_value=15, max_value=180, value=60, step=15)
    focus_areas = st.text_input("Ingresa cualquier área de enfoque o preocupación específica:")

    # Definir los agentes
    context_analyzer = Agent(
        role='Especialista en Contexto de Reuniones',
        goal='Analizar y resumir información clave de fondo para la reunión',
        backstory='Eres un experto en comprender rápidamente contextos empresariales complejos e identificar información crítica.',
        verbose=True,
        allow_delegation=False,
        llm=claude,
        tools=[search_tool]
    )

    industry_insights_generator = Agent(
        role='Experto en la Industria',
        goal='Proporcionar un análisis profundo de la industria e identificar tendencias clave',
        backstory='Eres un analista de la industria experimentado con un talento para detectar tendencias y oportunidades emergentes.',
        verbose=True,
        allow_delegation=False,
        llm=claude,
        tools=[search_tool]
    )

    strategy_formulator = Agent(
        role='Estratega de Reuniones',
        goal='Desarrollar una estrategia de reunión personalizada y una agenda detallada',
        backstory='Eres un maestro en la planificación de reuniones, conocido por crear estrategias y agendas altamente efectivas.',
        verbose=True,
        allow_delegation=False,
        llm=claude,
    )

    executive_briefing_creator = Agent(
        role='Especialista en Comunicación',
        goal='Sintetizar información en informes concisos e impactantes',
        backstory='Eres un experto comunicador, hábil en destilar información compleja en ideas claras y accionables.',
        verbose=True,
        allow_delegation=False,
        llm=claude,
    )

    # Definir las tareas
    context_analysis_task = Task(
        description=f"""
        Analiza el contexto para la reunión con {company_name}, considerando:
        1. El objetivo de la reunión: {meeting_objective}
        2. Los asistentes: {attendees}
        3. La duración de la reunión: {meeting_duration} minutos
        4. Áreas de enfoque o preocupaciones específicas: {focus_areas}

        Investiga a fondo {company_name}, incluyendo:
        1. Noticias recientes y comunicados de prensa
        2. Productos o servicios clave
        3. Principales competidores

        Proporciona un resumen completo de tus hallazgos, destacando la información más relevante para el contexto de la reunión.
        Formatea tu salida usando markdown con encabezados y subencabezados apropiados.
        """,
        agent=context_analyzer,
        expected_output="Un análisis detallado del contexto de la reunión y el trasfondo de la empresa, incluyendo desarrollos recientes, rendimiento financiero y relevancia para el objetivo de la reunión, formateado en markdown con encabezados y subencabezados."
    )

    industry_analysis_task = Task(
        description=f"""
        Basado en el análisis de contexto para {company_name} y el objetivo de la reunión: {meeting_objective}, proporciona un análisis profundo de la industria:
        1. Identifica tendencias y desarrollos clave en la industria
        2. Analiza el panorama competitivo
        3. Destaca oportunidades y amenazas potenciales
        4. Proporciona ideas sobre el posicionamiento en el mercado

        Asegúrate de que el análisis sea relevante para el objetivo de la reunión y los roles de los asistentes.
        Formatea tu salida usando markdown con encabezados y subencabezados apropiados.
        """,
        agent=industry_insights_generator,
        expected_output="Un informe de análisis de la industria completo, incluyendo tendencias, panorama competitivo, oportunidades, amenazas e ideas relevantes para el objetivo de la reunión, formateado en markdown con encabezados y subencabezados."
    )

    strategy_development_task = Task(
        description=f"""
        Usando el análisis de contexto y las ideas de la industria, desarrolla una estrategia de reunión personalizada y una agenda detallada para la reunión de {meeting_duration} minutos con {company_name}. Incluye:
        1. Una agenda con objetivos claros para cada sección
        2. Puntos clave de discusión para cada elemento de la agenda
        3. Oradores o líderes sugeridos para cada sección
        4. Temas de discusión y preguntas potenciales para impulsar la conversación
        5. Estrategias para abordar las áreas de enfoque y preocupaciones específicas: {focus_areas}

        Asegúrate de que la estrategia y la agenda se alineen con el objetivo de la reunión: {meeting_objective}
        Formatea tu salida usando markdown con encabezados y subencabezados apropiados.
        """,
        agent=strategy_formulator,
        expected_output="Una estrategia de reunión detallada y una agenda con objetivos, puntos clave de discusión y estrategias para abordar áreas de enfoque específicas, formateado en markdown con encabezados y subencabezados."
    )

    executive_brief_task = Task(
        description=f"""
        Sintetiza toda la información recopilada en un informe ejecutivo completo pero conciso para la reunión con {company_name}. Crea los siguientes componentes:

        1. Un resumen ejecutivo detallado de una página que incluya:
           - Declaración clara del objetivo de la reunión
           - Lista de asistentes clave y sus roles
           - Puntos de fondo críticos sobre {company_name} y contexto relevante de la industria
           - Los 3-5 objetivos estratégicos principales para la reunión, alineados con el objetivo
           - Breve descripción de la estructura de la reunión y temas clave a tratar

        2. Una lista detallada de puntos clave de discusión, cada uno respaldado por:
           - Datos o estadísticas relevantes
           - Ejemplos o estudios de caso específicos
           - Conexión con la situación actual o desafíos de la empresa

        3. Anticipa y prepárate para preguntas potenciales:
           - Lista de preguntas probables de los asistentes basadas en sus roles y el objetivo de la reunión
           - Elabora respuestas reflexivas y basadas en datos para cada pregunta
           - Incluye cualquier información de apoyo o contexto adicional que pueda ser necesario

        4. Recomendaciones estratégicas y próximos pasos:
           - Proporciona 3-5 recomendaciones accionables basadas en el análisis
           - Describe los próximos pasos claros para la implementación o seguimiento
           - Sugiere cronogramas o plazos para acciones clave
           - Identifica desafíos o obstáculos potenciales y propone estrategias de mitigación

        Asegúrate de que el informe sea completo pero conciso, altamente accionable y precisamente alineado con el objetivo de la reunión: {meeting_objective}. El documento debe estar estructurado para una fácil navegación y referencia rápida durante la reunión.
        Formatea tu salida usando markdown con encabezados y subencabezados apropiados.
        """,
        agent=executive_briefing_creator,
        expected_output="Un informe ejecutivo completo que incluya resumen, puntos clave de discusión, preparación de preguntas y respuestas, y recomendaciones estratégicas, formateado en markdown con encabezados principales (H1), encabezados de sección (H2) y subencabezados (H3) donde sea apropiado. Usa viñetas, listas numeradas y énfasis (negrita/itálica) para información clave."
    )

    # Crear el equipo
    meeting_prep_crew = Crew(
        agents=[context_analyzer, industry_insights_generator, strategy_formulator, executive_briefing_creator],
        tasks=[context_analysis_task, industry_analysis_task, strategy_development_task, executive_brief_task],
        verbose=True,
        process=Process.sequential
    )

    # Ejecutar el equipo cuando el usuario haga clic en el botón
    if st.button("Preparar Reunión"):
        with st.spinner("Los agentes de IA están preparando tu reunión..."):
            result = meeting_prep_crew.kickoff()        
        st.markdown(result)

    st.sidebar.markdown("""
    ## Cómo usar esta aplicación:
    1. Ingresa tus claves API en la barra lateral.
    2. Proporciona la información solicitada sobre la reunión.
    3. Haz clic en 'Preparar Reunión' para generar tu paquete completo de preparación para la reunión.

    Los agentes de IA trabajarán juntos para:
    - Analizar el contexto de la reunión y el trasfondo de la empresa
    - Proporcionar ideas y tendencias de la industria
    - Desarrollar una estrategia de reunión personalizada y una agenda
    - Crear un informe ejecutivo con puntos clave de discusión

    Este proceso puede tardar unos minutos. ¡Por favor, ten paciencia!
    """)
else:
    st.warning("Por favor, ingresa todas las claves API en la barra lateral antes de continuar.")