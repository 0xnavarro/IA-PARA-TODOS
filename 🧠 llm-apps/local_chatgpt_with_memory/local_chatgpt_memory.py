import streamlit as st
from mem0 import Memory
from litellm import completion

# Configuración para Memoria
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "local-chatgpt-memory",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768,
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1:latest",
            "temperature": 0,
            "max_tokens": 8000,
            "ollama_base_url": "http://localhost:11434",  # Asegúrate de que esta URL sea correcta
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            # Alternativamente, puedes usar "snowflake-arctic-embed:latest"
            "ollama_base_url": "http://localhost:11434",
        },
    },
    "version": "v1.1"
}

st.title("ChatGPT Local usando Llama 3.1 con Memoria Personal 🧠")
st.caption("¡Cada usuario obtiene su propio espacio de memoria personalizado!")

# Inicializar el estado de la sesión para el historial de chat y el ID de usuario anterior
if "messages" not in st.session_state:
    st.session_state.messages = []
if "previous_user_id" not in st.session_state:
    st.session_state.previous_user_id = None

# Barra lateral para autenticación de usuario
with st.sidebar:
    st.title("Configuración de Usuario")
    user_id = st.text_input("Ingresa tu Nombre de Usuario", key="user_id")
    
    # Verificar si el ID de usuario ha cambiado
    if user_id != st.session_state.previous_user_id:
        st.session_state.messages = []  # Limpiar historial de chat
        st.session_state.previous_user_id = user_id  # Actualizar ID de usuario anterior
    
    if user_id:
        st.success(f"Sesión iniciada como: {user_id}")
        
        # Inicializar Memoria con la configuración
        m = Memory.from_config(config)
        
        # Sección para ver la memoria
        st.header("Contexto de Memoria")
        if st.button("Ver Mi Memoria"):
            memories = m.get_all(user_id=user_id)
            if memories and "results" in memories:
                st.write(f"Historial de memoria para **{user_id}**:")
                for memory in memories["results"]:
                    if "memory" in memory:
                        st.write(f"- {memory['memory']}")

# Interfaz principal del chat
if user_id:  # Solo mostrar la interfaz de chat si el usuario ha "iniciado sesión"
    # Mostrar historial de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada del usuario
    if prompt := st.chat_input("¿Cuál es tu mensaje?"):
        # Agregar mensaje del usuario al historial de chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)

        # Agregar a la memoria
        m.add(prompt, user_id=user_id)
        
        # Obtener contexto de la memoria
        memories = m.get_all(user_id=user_id)
        context = ""
        if memories and "results" in memories:
            for memory in memories["results"]:
                if "memory" in memory:
                    context += f"- {memory['memory']}\n"

        # Generar respuesta del asistente
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Transmitir la respuesta
            try:
                response = completion(
                    model="ollama/llama3.1:latest",
                    messages=[
                        {"role": "system", "content": "Eres un asistente útil con acceso a conversaciones pasadas. Usa el contexto proporcionado para dar respuestas personalizadas."},
                        {"role": "user", "content": f"Contexto de conversaciones previas con {user_id}: {context}\nMensaje actual: {prompt}"}
                    ],
                    api_base="http://localhost:11434",
                    stream=True
                )
                
                # Procesar respuesta en streaming
                for chunk in response:
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.get('content', '')
                        if content:
                            full_response += content
                            message_placeholder.markdown(full_response + "▌")
                
                # Actualización final
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Error al generar la respuesta: {str(e)}")
                full_response = "Me disculpo, pero encontré un error al generar la respuesta."
                message_placeholder.markdown(full_response)

        # Agregar respuesta del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Agregar respuesta a la memoria
        m.add(f"Asistente: {full_response}", user_id=user_id)

else:
    st.info("👈 ¡Por favor ingresa tu nombre de usuario en la barra lateral para comenzar a chatear!")