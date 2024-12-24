import os

os.environ["OPENAI_API_KEY"] = "tu_clave_api_openai"
os.environ['TOGETHERAI_API_KEY'] = "tu_clave_api_togetherai"

import streamlit as st
from routellm.controller import Controller

# Inicializar cliente RouteLLM
client = Controller(
    routers=["mf"],
    strong_model="gpt-4o-mini",
    weak_model="together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
)

# Configurar aplicación Streamlit
st.title("Aplicación de Chat RouteLLM")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "model" in message:
            st.caption(f"Modelo usado: {message['model']}")

# Entrada de chat
if prompt := st.chat_input("¿Cuál es tu mensaje?"):
    # Agregar mensaje del usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Obtener respuesta de RouteLLM
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = client.chat.completions.create(
            model="router-mf-0.11593",
            messages=[{"role": "user", "content": prompt}]
        )
        message_content = response['choices'][0]['message']['content']
        model_name = response['model']
        
        # Mostrar respuesta del asistente
        message_placeholder.markdown(message_content)
        st.caption(f"Modelo usado: {model_name}")
    
    # Agregar respuesta del asistente al historial de chat
    st.session_state.messages.append({"role": "assistant", "content": message_content, "model": model_name})