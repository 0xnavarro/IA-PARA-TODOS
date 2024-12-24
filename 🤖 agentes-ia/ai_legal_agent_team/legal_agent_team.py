import streamlit as st
from phi.agent import Agent
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.qdrant import Qdrant
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.openai import OpenAIChat
from phi.embedder.openai import OpenAIEmbedder
import tempfile
import os

# Inicializar las variables de estado de la sesión
def init_session_state():
    """Inicializar variables de estado de la sesión"""
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = None
    if 'qdrant_api_key' not in st.session_state:
        st.session_state.qdrant_api_key = None
    if 'qdrant_url' not in st.session_state:
        st.session_state.qdrant_url = None
    if 'vector_db' not in st.session_state:
        st.session_state.vector_db = None
    if 'legal_team' not in st.session_state:
        st.session_state.legal_team = None
    if 'knowledge_base' not in st.session_state:
        st.session_state.knowledge_base = None

def init_qdrant():
    """Inicializar base de datos vectorial Qdrant"""
    if not st.session_state.qdrant_api_key:
        raise ValueError("Clave API de Qdrant no proporcionada")
    if not st.session_state.qdrant_url:
        raise ValueError("URL de Qdrant no proporcionada")
        
    return Qdrant(          
        collection="legal_knowledge",
        url=st.session_state.qdrant_url,
        api_key=st.session_state.qdrant_api_key,
        https=True,
        timeout=None,
        distance="cosine"
    )

def process_document(uploaded_file, vector_db: Qdrant):
    """Procesar documento, crear embeddings y almacenar en la base de datos vectorial Qdrant"""
    if not st.session_state.openai_api_key:
        raise ValueError("Clave API de OpenAI no proporcionada")
        
    os.environ['OPENAI_API_KEY'] = st.session_state.openai_api_key
    
    with tempfile.TemporaryDirectory() as temp_dir:
      
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
       
            embedder = OpenAIEmbedder(
                model="text-embedding-3-small",
                api_key=st.session_state.openai_api_key
            )
            
            # Crear base de conocimientos con configuración explícita de Qdrant
            knowledge_base = PDFKnowledgeBase(
                path=temp_dir, 
                vector_db=vector_db, 
                reader=PDFReader(chunk=True),
                embedder=embedder,
                recreate_vector_db=True  
            )
            knowledge_base.load()     
            return knowledge_base      
        except Exception as e:
            raise Exception(f"Error al procesar el documento: {str(e)}")

def main():
    st.set_page_config(page_title="Analizador de Documentos Legales", layout="wide")
    init_session_state()

    st.title("Equipo de Agentes Legales IA 👨‍⚖️")

    with st.sidebar:
        st.header("🔑 Configuración de API")
   
        openai_key = st.text_input(
            "Clave API de OpenAI",
            type="password",
            value=st.session_state.openai_api_key if st.session_state.openai_api_key else "",
            help="Ingresa tu clave API de OpenAI"
        )
        if openai_key:
            st.session_state.openai_api_key = openai_key

        qdrant_key = st.text_input(
            "Clave API de Qdrant",
            type="password",
            value=st.session_state.qdrant_api_key if st.session_state.qdrant_api_key else "",
            help="Ingresa tu clave API de Qdrant"
        )
        if qdrant_key:
            st.session_state.qdrant_api_key = qdrant_key

        qdrant_url = st.text_input(
            "URL de Qdrant",
            value=st.session_state.qdrant_url if st.session_state.qdrant_url else "https://f499085c-b4bf-4bda-a9a5-227f62a9ca20.us-west-2-0.aws.cloud.qdrant.io:6333",
            help="Ingresa la URL de tu instancia de Qdrant"
        )
        if qdrant_url:
            st.session_state.qdrant_url = qdrant_url

        if all([st.session_state.qdrant_api_key, st.session_state.qdrant_url]):
            try:
                if not st.session_state.vector_db:
                    st.session_state.vector_db = init_qdrant()
                    st.success("¡Conexión exitosa con Qdrant!")
            except Exception as e:
                st.error(f"Error al conectar con Qdrant: {str(e)}")

        st.divider()

        if all([st.session_state.openai_api_key, st.session_state.vector_db]):
            st.header("📄 Carga de Documento")
            uploaded_file = st.file_uploader("Cargar Documento Legal", type=['pdf'])
            
            if uploaded_file:
                with st.spinner("Procesando documento..."):
                    try:
                        knowledge_base = process_document(uploaded_file, st.session_state.vector_db)
                        st.session_state.knowledge_base = knowledge_base
                        
                        # Inicializar agentes
                        legal_researcher = Agent(
                            name="Investigador Legal",
                            role="Especialista en investigación legal",
                            model=OpenAIChat(model="gpt-4o"),
                            tools=[DuckDuckGo()],
                            knowledge=st.session_state.knowledge_base,
                            search_knowledge=True,
                            instructions=[
                                "Encontrar y citar casos legales y precedentes relevantes",
                                "Proporcionar resúmenes detallados de investigación con fuentes",
                                "Hacer referencia a secciones específicas del documento cargado",
                                "Siempre buscar en la base de conocimientos información relevante"
                            ],
                            show_tool_calls=True,
                            markdown=True
                        )

                        contract_analyst = Agent(
                            name="Analista de Contratos",
                            role="Especialista en análisis de contratos",
                            model=OpenAIChat(model="gpt-4o"),
                            knowledge=knowledge_base,
                            search_knowledge=True,
                            instructions=[
                                "Revisar contratos exhaustivamente",
                                "Identificar términos clave y problemas potenciales",
                                "Hacer referencia a cláusulas específicas del documento"
                            ],
                            markdown=True
                        )

                        legal_strategist = Agent(
                            name="Estratega Legal",
                            role="Especialista en estrategia legal",
                            model=OpenAIChat(model="gpt-4o"),
                            knowledge=knowledge_base,
                            search_knowledge=True,
                            instructions=[
                                "Desarrollar estrategias legales integrales",
                                "Proporcionar recomendaciones accionables",
                                "Considerar tanto riesgos como oportunidades"
                            ],
                            markdown=True
                        )

                        # Equipo Legal
                        st.session_state.legal_team = Agent(
                            name="Líder del Equipo Legal",
                            role="Coordinador del equipo legal",
                            model=OpenAIChat(model="gpt-4o"),
                            team=[legal_researcher, contract_analyst, legal_strategist],
                            knowledge=st.session_state.knowledge_base,
                            search_knowledge=True,
                            instructions=[
                                "Coordinar análisis entre miembros del equipo",
                                "Proporcionar respuestas integrales",
                                "Asegurar que todas las recomendaciones estén debidamente fundamentadas",
                                "Hacer referencia a partes específicas del documento cargado",
                                "Siempre buscar en la base de conocimientos antes de delegar tareas"
                            ],
                            show_tool_calls=True,
                            markdown=True
                        )
                        
                        st.success("✅ ¡Documento procesado y equipo inicializado!")
                            
                    except Exception as e:
                        st.error(f"Error al procesar el documento: {str(e)}")

            st.divider()
            st.header("🔍 Opciones de Análisis")
            analysis_type = st.selectbox(
                "Seleccionar Tipo de Análisis",
                [
                    "Revisión de Contrato",
                    "Investigación Legal",
                    "Evaluación de Riesgos",
                    "Verificación de Cumplimiento",
                    "Consulta Personalizada"
                ]
            )
        else:
            st.warning("Por favor, configura todas las credenciales API para continuar")

    # Área de contenido principal
    if not all([st.session_state.openai_api_key, st.session_state.vector_db]):
        st.info("👈 Por favor, configura tus credenciales API en la barra lateral para comenzar")
    elif not uploaded_file:
        st.info("👈 Por favor, carga un documento legal para comenzar el análisis")
    elif st.session_state.legal_team:
        # Crear un diccionario para los íconos de tipo de análisis
        analysis_icons = {
            "Revisión de Contrato": "📑",
            "Investigación Legal": "🔍",
            "Evaluación de Riesgos": "⚠️",
            "Verificación de Cumplimiento": "✅",
            "Consulta Personalizada": "💭"
        }

        # Encabezado dinámico con ícono
        st.header(f"{analysis_icons[analysis_type]} Análisis de {analysis_type}")
  
        analysis_configs = {
            "Revisión de Contrato": {
                "query": "Revisa este contrato e identifica términos clave, obligaciones y problemas potenciales.",
                "agents": ["Analista de Contratos"],
                "description": "Análisis detallado del contrato enfocado en términos y obligaciones"
            },
            "Investigación Legal": {
                "query": "Investiga casos y precedentes relevantes relacionados con este documento.",
                "agents": ["Investigador Legal"],
                "description": "Investigación sobre casos legales y precedentes relevantes"
            },
            "Evaluación de Riesgos": {
                "query": "Analiza los riesgos legales y responsabilidades potenciales en este documento.",
                "agents": ["Analista de Contratos", "Estratega Legal"],
                "description": "Análisis combinado de riesgos y evaluación estratégica"
            },
            "Verificación de Cumplimiento": {
                "query": "Verifica el cumplimiento legal y regulatorio de este documento.",
                "agents": ["Investigador Legal", "Estratega Legal", "Analista de Contratos"],
                "description": "Evaluación integral del cumplimiento normativo"
            }
        }

        st.info(f"📋 {analysis_configs[analysis_type]['description']}")
        st.write(f"🤖 Agentes de IA Legales Activos: {', '.join(analysis_configs[analysis_type]['agents'])}")  #dictionary!!

        # Replace the existing user_query section with this:
        if analysis_type == "Consulta Personalizada":
            user_query = st.text_area(
                "Ingrese su consulta específica:",
                help="Agregue cualquier pregunta o punto que desee analizar"
            )
        else:
            user_query = None  # Set to None for non-custom queries


        if st.button("Analizar"):
            if analysis_type == "Consulta Personalizada" and not user_query:
                st.warning("Por favor, ingrese una consulta")
            else:
                with st.spinner("Analizando documento..."):
                    try:
                        # Ensure OpenAI API key is set
                        os.environ['OPENAI_API_KEY'] = st.session_state.openai_api_key
                        
                        # Combine predefined and user queries
                        if analysis_type != "Consulta Personalizada":
                            combined_query = f"""
                            Usando el documento cargado como referencia:
                            
                            Tarea Principal de Análisis: {analysis_configs[analysis_type]['query']}
                            Áreas de Enfoque: {', '.join(analysis_configs[analysis_type]['agents'])}
                            
                            Por favor, busque en la base de conocimientos y proporcione referencias específicas del documento.
                            """
                        else:
                            combined_query = f"""
                            Usando el documento cargado como referencia:
                            
                            {user_query}
                            
                            Por favor, busque en la base de conocimientos y proporcione referencias específicas del documento.
                            Áreas de Enfoque: {', '.join(analysis_configs[analysis_type]['agents'])}
                            """

                        response = st.session_state.legal_team.run(combined_query)
                        
                        # Display results in tabs
                        tabs = st.tabs(["Análisis", "Puntos Clave", "Recomendaciones"])
                        
                        with tabs[0]:
                            st.markdown("### Análisis Detallado")
                            if response.content:
                                st.markdown(response.content)
                            else:
                                for message in response.messages:
                                    if message.role == 'assistant' and message.content:
                                        st.markdown(message.content)
                        
                        with tabs[1]:
                            st.markdown("### Puntos Clave")
                            key_points_response = st.session_state.legal_team.run(
                                f"""Based on this previous analysis:    
                                {response.content}
                                
                                Por favor, resuma los puntos clave en puntos de lista.
                                Enfoque en insights de: {', '.join(analysis_configs[analysis_type]['agents'])}"""
                            )
                            if key_points_response.content:
                                st.markdown(key_points_response.content)
                            else:
                                for message in key_points_response.messages:
                                    if message.role == 'assistant' and message.content:
                                        st.markdown(message.content)
                        
                        with tabs[2]:
                            st.markdown("### Recomendaciones")
                            recommendations_response = st.session_state.legal_team.run(
                                f"""Based on this previous analysis:
                                {response.content}
                                
                                ¿Cuáles son tus recomendaciones clave basadas en el análisis, la mejor acción de curso?
                                Proporcione recomendaciones específicas de: {', '.join(analysis_configs[analysis_type]['agents'])}"""
                            )
                            if recommendations_response.content:
                                st.markdown(recommendations_response.content)
                            else:
                                for message in recommendations_response.messages:
                                    if message.role == 'assistant' and message.content:
                                        st.markdown(message.content)

                    except Exception as e:
                        st.error(f"Error durante el análisis: {str(e)}")
    else:
        st.info("Por favor, carga un documento legal para comenzar el análisis")

if __name__ == "__main__":
    main() 