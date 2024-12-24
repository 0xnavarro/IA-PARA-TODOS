import streamlit as st
from openai import OpenAI
from mem0 import Memory

# Configurar la aplicación Streamlit
st.title("Agente de Viajes IA con Memoria 🧳")
st.caption("Chatea con un asistente de viajes que recuerda tus preferencias e interacciones pasadas.")

# Establecer la clave API de OpenAI
openai_api_key = st.text_input("Ingresa tu Clave API de OpenAI", type="password")

if openai_api_key:
    # Inicializar cliente OpenAI
    client = OpenAI(api_key=openai_api_key)

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

    # Barra lateral para nombre de usuario y vista de memoria
    st.sidebar.title("Ingresa tu nombre de usuario:")
    previous_user_id = st.session_state.get("previous_user_id", None)
    user_id = st.sidebar.text_input("Ingresa tu Nombre de Usuario")

    if user_id != previous_user_id:
        st.session_state.messages = []
        st.session_state.previous_user_id = user_id

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
    else:
        st.sidebar.error("Por favor ingresa un nombre de usuario para ver la información de memoria.")

    # Inicializar el historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar el historial de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Aceptar entrada del usuario
    prompt = st.chat_input("¿A dónde te gustaría viajar?")

    if prompt and user_id:
        # Agregar mensaje del usuario al historial de chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Recuperar memorias relevantes
        relevant_memories = memory.search(query=prompt, user_id=user_id)
        context = "Información relevante del pasado:\n"
        if relevant_memories and "results" in relevant_memories:
            for memory in relevant_memories["results"]:
                if "memory" in memory:
                    context += f"- {memory['memory']}\n"

        # Preparar el prompt completo
        full_prompt = f"{context}\nHumano: {prompt}\nIA:"

        # Generar respuesta
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un asistente de viajes con acceso a conversaciones pasadas."},
                {"role": "user", "content": full_prompt}
            ]
        )
        answer = response.choices[0].message.content

        # Agregar respuesta del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Almacenar la consulta del usuario y la respuesta de IA en memoria
        memory.add(prompt, user_id=user_id, metadata={"role": "user"})
        memory.add(answer, user_id=user_id, metadata={"role": "assistant"})
    elif not user_id:
        st.error("Por favor ingresa un nombre de usuario para comenzar el chat.")
