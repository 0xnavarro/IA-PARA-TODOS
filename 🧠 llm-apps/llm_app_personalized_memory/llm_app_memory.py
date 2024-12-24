import os
import streamlit as st
from mem0 import Memory
from openai import OpenAI

st.title("Aplicación LLM con Memoria 🧠")
st.caption("Aplicación LLM con capa de memoria personalizada que recuerda las elecciones e intereses de cada usuario")

openai_api_key = st.text_input("Ingresa tu Clave API de OpenAI", type="password")
os.environ["OPENAI_API_KEY"] = openai_api_key

if openai_api_key:
    # Inicializar cliente OpenAI
    client = OpenAI(api_key=openai_api_key)

    # Inicializar Mem0 con Qdrant
    config = {
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "llm_app_memory",
                "host": "localhost",
                "port": 6333,
            }
        },
    }

    memory = Memory.from_config(config)

    user_id = st.text_input("Ingresa tu Nombre de Usuario")

    prompt = st.text_input("Pregunta a ChatGPT")

    if st.button('Chatear con LLM'):
        with st.spinner('Buscando...'):
            relevant_memories = memory.search(query=prompt, user_id=user_id)
            # Preparar contexto con memorias relevantes
            context = "Información relevante del pasado:\n"

            for mem in relevant_memories:
                context += f"- {mem['text']}\n"
                
            # Preparar el prompt completo
            full_prompt = f"{context}\nHumano: {prompt}\nIA:"

            # Obtener respuesta de GPT-4
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres un asistente útil con acceso a conversaciones pasadas."},
                    {"role": "user", "content": full_prompt}
                ]
            )
            
            answer = response.choices[0].message.content

            st.write("Respuesta: ", answer)

            # Agregar respuesta de IA a la memoria
            memory.add(answer, user_id=user_id)


    # Opción en la barra lateral para mostrar la memoria
    st.sidebar.title("Información de Memoria")
    if st.button("Ver Mi Memoria"):
            memories = memory.get_all(user_id=user_id)
            if memories and "results" in memories:
                st.write(f"Historial de memoria para **{user_id}**:")
                for mem in memories["results"]:
                    if "memory" in mem:
                        st.write(f"- {mem['memory']}")
            else:
                st.sidebar.info("No se encontró historial de aprendizaje para este ID de usuario.")