import streamlit as st
from mem0 import Memory
from openai import OpenAI
import os
from litellm import completion

st.title("Aplicación Multi-LLM con Memoria Compartida 🧠")
st.caption("Aplicación LLM con una capa de memoria personalizada que recuerda las elecciones e intereses de cada usuario a través de múltiples usuarios y LLMs")

openai_api_key = st.text_input("Ingresa tu Clave API de OpenAI", type="password")
anthropic_api_key = st.text_input("Ingresa tu Clave API de Anthropic", type="password")

if openai_api_key and anthropic_api_key:
    os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key

    # Inicializar Mem0 con Qdrant
    config = {
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "host": "localhost",
                "port": 6333,
            }
        },
    }

    memory = Memory.from_config(config)

    user_id = st.sidebar.text_input("Ingresa tu Nombre de Usuario")
    llm_choice = st.sidebar.radio("Selecciona LLM", ('OpenAI GPT-4o', 'Claude Sonnet 3.5'))

    if llm_choice == 'OpenAI GPT-4o':
        client = OpenAI(api_key=openai_api_key)
    elif llm_choice == 'Claude Sonnet 3.5':
        config = {
            "llm": {
                "provider": "litellm",
                "config": {
                    "model": "claude-3-5-sonnet-20240620",
                    "temperature": 0.5,
                    "max_tokens": 2000,
                }
            }
        }
        client = Memory.from_config(config)

    prompt = st.text_input("Pregunta al LLM")

    if st.button('Chatear con LLM'):
        with st.spinner('Buscando...'):
            relevant_memories = memory.search(query=prompt, user_id=user_id)
            context = "Información relevante del pasado:\n"
            if relevant_memories and "results" in relevant_memories:
                for memory in relevant_memories["results"]:
                    if "memory" in memory:
                        context += f"- {memory['memory']}\n"
                
            full_prompt = f"{context}\nHumano: {prompt}\nIA:"

            if llm_choice == 'OpenAI GPT-4o':
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Eres un asistente útil con acceso a conversaciones pasadas."},
                        {"role": "user", "content": full_prompt}
                    ]
                )
                answer = response.choices[0].message.content
            elif llm_choice == 'Claude Sonnet 3.5':
                messages=[
                        {"role": "system", "content": "Eres un asistente útil con acceso a conversaciones pasadas."},
                        {"role": "user", "content": full_prompt}
                    ]
                response = completion(model="claude-3-5-sonnet-20240620", messages=messages)
                answer = response.choices[0].message.content
            st.write("Respuesta: ", answer)

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