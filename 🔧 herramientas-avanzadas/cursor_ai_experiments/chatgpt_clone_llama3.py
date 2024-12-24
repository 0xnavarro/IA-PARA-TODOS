import streamlit as st
from ollama import Client

# Inicializar cliente Ollama
client = Client()

# Configurar página de Streamlit
st.set_page_config(page_title="Clon Local de ChatGPT", page_icon="🤖", layout="wide")
st.title("🤖 Clon Local de ChatGPT")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿Qué tienes en mente?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta de IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat(model="llama3.1:latest", messages=st.session_state.messages, stream=True):
            full_response += response['message']['content']
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Agregar una barra lateral con información
st.sidebar.title("Acerca de")
st.sidebar.info("Este es un clon local de ChatGPT usando el modelo llama3.1:latest de Ollama y Streamlit.")
st.sidebar.markdown("---")
st.sidebar.markdown("Hecho con ❤️ por Tu Nombre")