import os
import logging
import streamlit as st
from raglite import RAGLiteConfig, insert_document, hybrid_search, retrieve_chunks, rerank_chunks, rag
from rerankers import Reranker
from typing import List
from pathlib import Path
import anthropic
import time
import warnings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", message=".*torch.classes.*")

RAG_SYSTEM_PROMPT = """
Eres un asistente amigable y conocedor que proporciona respuestas completas y perspicaces.
Responde la pregunta del usuario usando solo el contexto proporcionado a continuación.
Al responder, NO DEBES hacer referencia a la existencia del contexto, directa o indirectamente.
En su lugar, DEBES tratar el contexto como si su contenido fuera parte integral de tu memoria de trabajo.
""".strip()

def initialize_config(openai_key: str, anthropic_key: str, cohere_key: str, db_url: str) -> RAGLiteConfig:
    try:
        os.environ["OPENAI_API_KEY"] = openai_key
        os.environ["ANTHROPIC_API_KEY"] = anthropic_key
        os.environ["COHERE_API_KEY"] = cohere_key
        
        return RAGLiteConfig(
            db_url=db_url,
            llm="claude-3-opus-20240229",
            embedder="text-embedding-3-large",
            embedder_normalize=True,
            chunk_max_size=2000,
            embedder_sentence_window_size=2,
            reranker=Reranker("cohere", api_key=cohere_key, lang="en")
        )
    except Exception as e:
        raise ValueError(f"Error de configuración: {e}")

def process_document(file_path: str) -> bool:
    try:
        if not st.session_state.get('my_config'):
            raise ValueError("Configuración no inicializada")
        insert_document(Path(file_path), config=st.session_state.my_config)
        return True
    except Exception as e:
        logger.error(f"Error al procesar el documento: {str(e)}")
        return False

def perform_search(query: str) -> List[dict]:
    try:
        chunk_ids, scores = hybrid_search(query, num_results=10, config=st.session_state.my_config)
        if not chunk_ids:
            return []
        chunks = retrieve_chunks(chunk_ids, config=st.session_state.my_config)
        return rerank_chunks(query, chunks, config=st.session_state.my_config)
    except Exception as e:
        logger.error(f"Error en la búsqueda: {str(e)}")
        return []

def handle_fallback(query: str) -> str:
    try:
        client = anthropic.Anthropic(api_key=st.session_state.user_env["ANTHROPIC_API_KEY"])
        system_prompt = """Eres un asistente de IA útil. Cuando no sepas algo, 
        sé honesto al respecto. Proporciona respuestas claras, concisas y precisas. Si la pregunta 
        no está relacionada con ningún documento específico, usa tu conocimiento general para responder."""
        
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": query}],
            temperature=0.7
        )
        return message.content[0].text
    except Exception as e:
        logger.error(f"Error en el respaldo: {str(e)}")
        st.error(f"Error en el respaldo: {str(e)}")  # Mostrar error en la UI
        return "Me disculpo, pero encontré un error al procesar tu solicitud. Por favor, inténtalo de nuevo."

def main():
    st.set_page_config(page_title="Asistente RAG con Búsqueda Híbrida", layout="wide")
    
    for state_var in ['chat_history', 'documents_loaded', 'my_config', 'user_env']:
        if state_var not in st.session_state:
            st.session_state[state_var] = [] if state_var == 'chat_history' else False if state_var == 'documents_loaded' else None if state_var == 'my_config' else {}

    with st.sidebar:
        st.title("Configuración")
        openai_key = st.text_input("Clave API de OpenAI", value=st.session_state.get('openai_key', ''), type="password", placeholder="sk-...")
        anthropic_key = st.text_input("Clave API de Anthropic", value=st.session_state.get('anthropic_key', ''), type="password", placeholder="sk-ant-...")
        cohere_key = st.text_input("Clave API de Cohere", value=st.session_state.get('cohere_key', ''), type="password", placeholder="Ingresa la clave de Cohere")
        db_url = st.text_input("URL de la Base de Datos", value=st.session_state.get('db_url', 'sqlite:///raglite.sqlite'), placeholder="sqlite:///raglite.sqlite")
        
        if st.button("Guardar Configuración"):
            try:
                if not all([openai_key, anthropic_key, cohere_key, db_url]):
                    st.error("¡Todos los campos son requeridos!")
                    return
                
                for key, value in {'openai_key': openai_key, 'anthropic_key': anthropic_key, 'cohere_key': cohere_key, 'db_url': db_url}.items():
                    st.session_state[key] = value
                
                st.session_state.my_config = initialize_config(openai_key=openai_key, anthropic_key=anthropic_key, cohere_key=cohere_key, db_url=db_url)
                st.session_state.user_env = {"ANTHROPIC_API_KEY": anthropic_key}
                st.success("¡Configuración guardada exitosamente!")
            except Exception as e:
                st.error(f"Error de configuración: {str(e)}")

    st.title("👀 Aplicación RAG con Búsqueda Híbrida")

    if st.session_state.my_config:
        uploaded_files = st.file_uploader("Subir documentos PDF", type=["pdf"], accept_multiple_files=True, key="pdf_uploader")

        if uploaded_files:
            success = False
            for uploaded_file in uploaded_files:
                with st.spinner(f"Procesando {uploaded_file.name}..."):
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    if process_document(temp_path):
                        st.success(f"Procesado exitosamente: {uploaded_file.name}")
                        success = True
                    else:
                        st.error(f"Error al procesar: {uploaded_file.name}")
                    os.remove(temp_path)
            
            if success:
                st.session_state.documents_loaded = True
                st.success("¡Los documentos están listos! Ahora puedes hacer preguntas sobre ellos.")

    if st.session_state.documents_loaded:
        for msg in st.session_state.chat_history:
            with st.chat_message("user"): st.write(msg[0])
            with st.chat_message("assistant"): st.write(msg[1])

        user_input = st.chat_input("Haz una pregunta sobre los documentos...")
        if user_input:
            with st.chat_message("user"): st.write(user_input)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                try:
                    reranked_chunks = perform_search(query=user_input)
                    if not reranked_chunks or len(reranked_chunks) == 0:
                        logger.info("No se encontraron documentos relevantes. Recurriendo a Claude.")
                        st.info("No se encontraron documentos relevantes. Usando conocimiento general para responder.")
                        full_response = handle_fallback(user_input)
                    else:
                        formatted_messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": msg}
                                           for i, msg in enumerate([m for pair in st.session_state.chat_history for m in pair]) if msg]
                        
                        response_stream = rag(prompt=user_input, 
                                           system_prompt=RAG_SYSTEM_PROMPT,
                                           search=hybrid_search, 
                                           messages=formatted_messages,
                                           max_contexts=5, 
                                           config=st.session_state.my_config)
                        
                        full_response = ""
                        for chunk in response_stream:
                            full_response += chunk
                            message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    st.session_state.chat_history.append((user_input, full_response))
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.info("Por favor, configura tus claves API y sube documentos para comenzar." if not st.session_state.my_config else "Por favor, sube algunos documentos para comenzar.")

if __name__ == "__main__":
    main()