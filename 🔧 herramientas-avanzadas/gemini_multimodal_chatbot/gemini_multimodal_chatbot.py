import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configurar la aplicación Streamlit
st.set_page_config(page_title="Chatbot Multimodal con Gemini Flash", layout="wide")
st.title("Chatbot Multimodal con Gemini Flash ⚡️")
st.caption("Chatea con el modelo Gemini Flash de Google usando entrada de imagen y texto para obtener resultados ultrarrápidos. 🌟")

# Obtener la clave API de Google del usuario
api_key = st.text_input("Ingresa la Clave API de Google", type="password")

# Configurar el modelo Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

if api_key:
    # Inicializar el historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Barra lateral para subir imágenes
    with st.sidebar:
        st.title("Chatear con Imágenes")
        uploaded_file = st.file_uploader("Sube una imagen...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Imagen Subida', use_column_width=True)

    # Diseño principal
    chat_placeholder = st.container()

    with chat_placeholder:
        # Mostrar el historial de chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Área de entrada del usuario en la parte inferior
    prompt = st.chat_input("¿Qué quieres saber?")

    if prompt:
        inputs = [prompt]
        
        # Agregar mensaje del usuario al historial de chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Mostrar mensaje del usuario en el contenedor de mensajes de chat
        with chat_placeholder:
            with st.chat_message("user"):
                st.markdown(prompt)
        
        if uploaded_file:
            inputs.append(image)

        with st.spinner('Generando respuesta...'):
            # Generar respuesta
            response = model.generate_content(inputs)
    
        # Mostrar respuesta del asistente en el contenedor de mensajes de chat
        with chat_placeholder:
            with st.chat_message("assistant"):
                st.markdown(response.text)

    if uploaded_file and not prompt:
        st.warning("Por favor, ingresa una consulta de texto para acompañar la imagen.")