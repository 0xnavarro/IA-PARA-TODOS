import streamlit as st
from openai import OpenAI

# Configurar la aplicación Streamlit
st.title("Clon de ChatGPT usando Llama-3 🦙")
st.caption("Chatea con Llama-3 alojado localmente usando LM Studio 💯")

# Apuntar al servidor local configurado usando LM Studio
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Inicializar el historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Aceptar entrada del usuario
if prompt := st.chat_input("¿Qué tal?"):
    # Agregar mensaje del usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Mostrar mensaje del usuario en el contenedor de mensajes de chat
    with st.chat_message("user"):
        st.markdown(prompt)
    # Generar respuesta
    response = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=st.session_state.messages, temperature=0.7
    )
    # Agregar respuesta del asistente al historial de chat
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
    # Mostrar respuesta del asistente en el contenedor de mensajes de chat
    with st.chat_message("assistant"):
        st.markdown(response.choices[0].message.content)
