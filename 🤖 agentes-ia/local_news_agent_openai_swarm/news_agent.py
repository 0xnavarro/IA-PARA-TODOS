import streamlit as st
from duckduckgo_search import DDGS
from swarm import Swarm, Agent
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
MODEL = "llama3.2:latest"
client = Swarm()

st.set_page_config(page_title="Procesador de Noticias IA", page_icon="📰")
st.title("📰 Agente de Noticias Inshorts")

def search_news(topic):
    """Buscar artículos de noticias usando DuckDuckGo"""
    with DDGS() as ddg:
        results = ddg.text(f"{topic} news {datetime.now().strftime('%Y-%m')}", max_results=3)
        if results:
            news_results = "\n\n".join([
                f"Título: {result['title']}\nURL: {result['href']}\nResumen: {result['body']}" 
                for result in results
            ])
            return news_results
        return f"No se encontraron noticias para {topic}."

# Crear agentes especializados
search_agent = Agent(
    name="Buscador de Noticias",
    instructions="""
    Eres un especialista en búsqueda de noticias. Tu tarea es:
    1. Buscar las noticias más relevantes y recientes sobre el tema dado
    2. Asegurar que los resultados sean de fuentes confiables
    3. Devolver los resultados de búsqueda en un formato estructurado
    """,
    functions=[search_news],
    model=MODEL
)

synthesis_agent = Agent(
    name="Sintetizador de Noticias",
    instructions="""
    Eres un experto en síntesis de noticias. Tu tarea es:
    1. Analizar los artículos de noticias proporcionados
    2. Identificar los temas clave y la información importante
    3. Combinar información de múltiples fuentes
    4. Crear una síntesis completa pero concisa
    5. Enfocarte en los hechos y mantener la objetividad periodística
    6. Escribir en un estilo claro y profesional
    Proporciona una síntesis de 2-3 párrafos de los puntos principales.
    """,
    model=MODEL
)

summary_agent = Agent(
    name="Resumidor de Noticias",
    instructions="""
    Eres un experto resumidor de noticias que combina la claridad del estilo AP y Reuters con la brevedad de la era digital.

    Tu tarea:
    1. Información Principal:
       - Comienza con el desarrollo más noticioso
       - Incluye actores clave y sus acciones
       - Agrega números/datos críticos si son relevantes
       - Explica por qué esto importa ahora
       - Menciona las implicaciones inmediatas

    2. Pautas de Estilo:
       - Usa verbos fuertes y activos
       - Sé específico, no general
       - Mantén la objetividad periodística
       - Haz que cada palabra cuente
       - Explica términos técnicos si es necesario

    Formato: Crea un solo párrafo de 250-400 palabras que informe y enganche.
    Patrón: [Noticia Principal] + [Detalles/Datos Clave] + [Por qué Importa/Qué Sigue]

    Enfócate en responder: ¿Qué sucedió? ¿Por qué es significativo? ¿Cuál es el impacto?

    IMPORTANTE: Proporciona SOLO el párrafo de resumen. No incluyas frases introductorias, 
    etiquetas o meta-texto como "Aquí hay un resumen" o "En estilo AP/Reuters."
    Comienza directamente con el contenido de la noticia.
    """,
    model=MODEL
)

def process_news(topic):
    """Ejecutar el flujo de procesamiento de noticias"""
    with st.status("Procesando noticias...", expanded=True) as status:
        # Búsqueda
        status.write("🔍 Buscando noticias...")
        search_response = client.run(
            agent=search_agent,
            messages=[{"role": "user", "content": f"Encuentra noticias recientes sobre {topic}"}]
        )
        raw_news = search_response.messages[-1]["content"]
        
        # Sintetizar
        status.write("🔄 Sintetizando información...")
        synthesis_response = client.run(
            agent=synthesis_agent,
            messages=[{"role": "user", "content": f"Sintetiza estos artículos de noticias:\n{raw_news}"}]
        )
        synthesized_news = synthesis_response.messages[-1]["content"]
        
        # Resumir
        status.write("📝 Creando resumen...")
        summary_response = client.run(
            agent=summary_agent,
            messages=[{"role": "user", "content": f"Resume esta síntesis:\n{synthesized_news}"}]
        )
        return raw_news, synthesized_news, summary_response.messages[-1]["content"]

# Interfaz de Usuario
topic = st.text_input("Ingresa el tema de la noticia:", value="inteligencia artificial")
if st.button("Procesar Noticias", type="primary"):
    if topic:
        try:
            raw_news, synthesized_news, final_summary = process_news(topic)
            st.header(f"📝 Resumen de Noticias: {topic}")
            st.markdown(final_summary)
        except Exception as e:
            st.error(f"Ocurrió un error: {str(e)}")
    else:
        st.error("¡Por favor ingresa un tema!")