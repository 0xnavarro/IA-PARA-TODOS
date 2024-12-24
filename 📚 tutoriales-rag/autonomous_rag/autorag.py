import streamlit as st
import nest_asyncio
from io import BytesIO
from phi.assistant import Assistant
from phi.document.reader.pdf import PDFReader
from phi.llm.openai import OpenAIChat
from phi.knowledge import AssistantKnowledge
from phi.tools.duckduckgo import DuckDuckGo
from phi.embedder.openai import OpenAIEmbedder
from phi.vectordb.pgvector import PgVector2
from phi.storage.assistant.postgres import PgAssistantStorage

# Aplicar nest_asyncio para permitir bucles de eventos anidados
nest_asyncio.apply()

# Cadena de conexión a la base de datos PostgreSQL
DB_URL = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Función para configurar el Asistente, utilizando caché para eficiencia
@st.cache_resource
def setup_assistant(api_key: str) -> Assistant:
    llm = OpenAIChat(model="gpt-4o-mini", api_key=api_key)
    # Configurar el Asistente con almacenamiento, base de conocimientos y herramientas
    return Assistant(
        name="auto_rag_assistant",  # Nombre del Asistente
        llm=llm,  # Modelo de lenguaje a utilizar
        storage=PgAssistantStorage(table_name="auto_rag_storage", db_url=DB_URL),  # Almacenamiento persistente
        knowledge_base=AssistantKnowledge(
            vector_db=PgVector2(
                db_url=DB_URL,  # URL de la base de datos
                collection="auto_rag_docs",  # Nombre de la colección
                embedder=OpenAIEmbedder(model="text-embedding-ada-002", dimensions=1536, api_key=api_key),  # Configuración del embedder
            ),
            num_documents=3,  # Número de documentos a recuperar
        ),
        tools=[DuckDuckGo()],  # Herramienta de búsqueda web
        instructions=[
            "Busca primero en tu base de conocimientos.",
            "Si no encuentras la información, busca en internet.",
            "Proporciona respuestas claras y concisas.",
        ],
        show_tool_calls=True,  # Mostrar llamadas a herramientas
        search_knowledge=True,  # Habilitar búsqueda en base de conocimientos
        read_chat_history=True,  # Leer historial de chat
        markdown=True,  # Habilitar formato markdown
        debug_mode=True,  # Modo de depuración
    )

# Función para agregar un documento PDF a la base de conocimientos
def add_document(assistant: Assistant, file: BytesIO):
    reader = PDFReader()
    docs = reader.read(file)
    if docs:
        assistant.knowledge_base.load_documents(docs, upsert=True)
        st.success("¡Documento agregado exitosamente a la base de conocimientos!")
    else:
        st.error("Error al procesar el documento PDF.")

# Función para consultar al Asistente y obtener una respuesta
def query_assistant(assistant: Assistant, question: str) -> str:
    return "".join([delta for delta in assistant.run(question)])

# Función principal para la interfaz de Streamlit
def main():
    st.set_page_config(page_title="AutoRAG", layout="wide")
    st.title("🤖 Auto-RAG: RAG Autónomo con GPT-4o")

    # Configuración de la barra lateral
    api_key = st.sidebar.text_input("Ingresa tu Clave API de OpenAI 🔑", type="password")
    
    if not api_key:
        st.sidebar.warning("Por favor, ingresa tu Clave API de OpenAI para continuar.")
        st.stop()

    # Inicializar el asistente
    assistant = setup_assistant(api_key)
    
    # Subida de archivos
    uploaded_file = st.sidebar.file_uploader("📄 Subir documento PDF", type=["pdf"])
    
    if uploaded_file and st.sidebar.button("🛠️ Agregar a la Base de Conocimientos"):
        add_document(assistant, BytesIO(uploaded_file.read()))

    # Interfaz de chat
    question = st.text_input("💬 ¿Qué deseas preguntar?")
    
    if st.button("🔍 Buscar Respuesta"):
        if question.strip():
            with st.spinner("🤔 Analizando tu pregunta..."):
                answer = query_assistant(assistant, question)
                st.write("📝 **Respuesta:**", answer)
        else:
            st.error("Por favor, ingresa una pregunta válida.")

if __name__ == "__main__":
    main()
