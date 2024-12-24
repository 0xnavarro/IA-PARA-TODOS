import streamlit as st
from litellm import completion

# Configurar la aplicación Streamlit
st.title("Playground de Chat Multi-LLM")

# Obtener las claves API del usuario
openai_api_key = st.text_input("Ingresa tu Clave API de OpenAI:", type="password")
anthropic_api_key = st.text_input("Ingresa tu Clave API de Anthropic:", type="password")
cohere_api_key = st.text_input("Ingresa tu Clave API de Cohere:", type="password")

# Verificar si se proporcionaron todas las claves API
if openai_api_key and anthropic_api_key and cohere_api_key:

    # Crear una entrada de texto para los mensajes del usuario
    user_input = st.text_input("Ingresa tu mensaje:")

    if st.button("Enviar a todos los LLMs"):
        if user_input:
            messages = [{"role": "user", "content": user_input}]
            
            # Crear tres columnas para mostrar lado a lado
            col1, col2, col3 = st.columns(3)
            
            # Respuesta de GPT-4o
            with col1:
                st.subheader("GPT-4o")
                try:
                    gpt_response = completion(model="gpt-4o", messages=messages, api_key=openai_api_key)
                    st.write(gpt_response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error con GPT-4o: {str(e)}")
            
            # Respuesta de Claude-3-sonnet
            with col2:
                st.subheader("Claude 3.5 Sonnet")
                try:
                    claude_response = completion(model="claude-3-5-sonnet-20240620", messages=messages, api_key=anthropic_api_key)
                    st.write(claude_response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error con Claude 3.5 Sonnet: {str(e)}")
            
            # Respuesta de Cohere
            with col3:
                st.subheader("Cohere")
                try:
                    cohere_response = completion(model="command-r-plus", messages=messages, api_key=cohere_api_key)
                    st.write(cohere_response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error con Cohere: {str(e)}")
            
            # Comparar respuestas
            st.subheader("Comparación de Respuestas")
            st.write("Puedes ver cómo los tres modelos respondieron de manera diferente a la misma entrada.")
            st.write("Esto demuestra la capacidad de usar múltiples LLMs en una sola aplicación.")
        else:
            st.warning("Por favor ingresa un mensaje.")
else:
    st.warning("Por favor ingresa todas las claves API para usar el chat.")

# Agregar información sobre la aplicación
st.sidebar.title("Acerca de esta aplicación")

st.sidebar.write(
    "Esta aplicación demuestra el uso de múltiples Modelos de Lenguaje (LLMs) "
    "en una sola aplicación usando la biblioteca LiteLLM."
)

st.sidebar.subheader("Características principales:")
st.sidebar.markdown(
    """
    - Utiliza tres LLMs diferentes:
        - GPT-4o de OpenAI
        - Claude 3.5 Sonnet de Anthropic
        - Command R Plus de Cohere
    - Envía la misma entrada del usuario a todos los modelos
    - Muestra las respuestas lado a lado para una fácil comparación
    - Demuestra la capacidad de usar múltiples LLMs en una aplicación
    """
)

st.sidebar.write(
    "¡Pruébalo para ver cómo diferentes modelos de IA responden al mismo prompt!"
)
