import streamlit as st
import asyncio
import os
from together import AsyncTogether, Together

# Configurar la aplicación Streamlit
st.title("Aplicación LLM de Mezcla de Agentes")

# Obtener la clave API del usuario
together_api_key = st.text_input("Ingresa tu Clave API de Together:", type="password")

if together_api_key:
    os.environ["TOGETHER_API_KEY"] = together_api_key
    client = Together(api_key=together_api_key)
    async_client = AsyncTogether(api_key=together_api_key)

    # Definir los modelos
    reference_models = [
        "Qwen/Qwen2-72B-Instruct",
        "Qwen/Qwen1.5-72B-Chat",
        "mistralai/Mixtral-8x22B-Instruct-v0.1",
        "databricks/dbrx-instruct",
    ]
    aggregator_model = "mistralai/Mixtral-8x22B-Instruct-v0.1"

    # Definir el prompt del sistema para el agregador
    aggregator_system_prompt = """Se te han proporcionado un conjunto de respuestas de varios modelos de código abierto a la última consulta del usuario. Tu tarea es sintetizar estas respuestas en una única respuesta de alta calidad. Es crucial evaluar críticamente la información proporcionada en estas respuestas, reconociendo que parte de ella puede estar sesgada o ser incorrecta. Tu respuesta no debe simplemente replicar las respuestas dadas, sino ofrecer una respuesta refinada, precisa y completa a la instrucción. Asegúrate de que tu respuesta esté bien estructurada, sea coherente y se adhiera a los más altos estándares de precisión y fiabilidad. Respuestas de los modelos:"""

    # Obtener entrada del usuario
    user_prompt = st.text_input("Ingresa tu pregunta:")

    async def run_llm(model):
        """Ejecutar una única llamada LLM con un modelo de referencia."""
        response = await async_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.7,
            max_tokens=512,
        )
        return model, response.choices[0].message.content

    async def main():
        results = await asyncio.gather(*[run_llm(model) for model in reference_models])
        
        # Mostrar respuestas individuales de los modelos
        st.subheader("Respuestas Individuales de los Modelos:")
        for model, response in results:
            with st.expander(f"Respuesta de {model}"):
                st.write(response)
        
        # Agregar respuestas
        st.subheader("Respuesta Agregada:")
        finalStream = client.chat.completions.create(
            model=aggregator_model,
            messages=[
                {"role": "system", "content": aggregator_system_prompt},
                {"role": "user", "content": ",".join(response for _, response in results)},
            ],
            stream=True,
        )
        
        # Mostrar respuesta agregada
        response_container = st.empty()
        full_response = ""
        for chunk in finalStream:
            content = chunk.choices[0].delta.content or ""
            full_response += content
            response_container.markdown(full_response + "▌")
        response_container.markdown(full_response)

    if st.button("Obtener Respuesta"):
        if user_prompt:
            asyncio.run(main())
        else:
            st.warning("Por favor ingresa una pregunta.")

else:
    st.warning("Por favor ingresa tu clave API de Together para usar la aplicación.")

# Agregar información sobre la aplicación
st.sidebar.title("Acerca de esta aplicación")
st.sidebar.write(
    "Esta aplicación demuestra un enfoque de Mezcla de Agentes usando múltiples Modelos de Lenguaje (LLMs) "
    "para responder una sola pregunta."
)

st.sidebar.subheader("Cómo funciona:")
st.sidebar.markdown(
    """
    1. La aplicación envía tu pregunta a múltiples LLMs:
        - Qwen/Qwen2-72B-Instruct
        - Qwen/Qwen1.5-72B-Chat
        - mistralai/Mixtral-8x22B-Instruct-v0.1
        - databricks/dbrx-instruct
    2. Cada modelo proporciona su propia respuesta
    3. Todas las respuestas son luego agregadas usando Mixtral-8x22B-Instruct-v0.1
    4. Se muestra la respuesta agregada final
    """
)

st.sidebar.write(
    "Este enfoque permite una respuesta más completa y equilibrada al aprovechar múltiples modelos de IA."
)