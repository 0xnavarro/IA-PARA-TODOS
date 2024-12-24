import streamlit as st
from openai import OpenAI
from mem0 import Memory
import os
import json
from datetime import datetime, timedelta

# Configurar la aplicación Streamlit
st.title("Agente de Atención al Cliente IA con Memoria 🛒")
st.caption("Chatea con un asistente de atención al cliente que recuerda tus interacciones pasadas.")

# Configurar la clave API de OpenAI
openai_api_key = st.text_input("Ingresa tu Clave API de OpenAI", type="password")

if openai_api_key:
    os.environ['OPENAI_API_KEY'] = openai_api_key
    
    class CustomerSupportAIAgent:
        def __init__(self):
            config = {
                "vector_store": {
                    "provider": "qdrant",
                    "config": {
                        "model": "gpt-4o-mini",
                        "host": "localhost",
                        "port": 6333,
                    }
                },
            }
            self.memory = Memory.from_config(config)
            self.client = OpenAI()
            self.app_id = "customer-support"

        def handle_query(self, query, user_id=None):
            relevant_memories = self.memory.search(query=query, user_id=user_id)
            context = "Información relevante del pasado:\n"
            if relevant_memories and "results" in relevant_memories:
                for memory in relevant_memories["results"]:
                    if "memory" in memory:
                        context += f"- {memory['memory']}\n"

            full_prompt = f"{context}\nCliente: {query}\nAgente de Soporte:"

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un agente de atención al cliente IA para TechGadgets.com, una tienda en línea de electrónicos."},
                    {"role": "user", "content": full_prompt}
                ]
            )
            answer = response.choices[0].message.content

            self.memory.add(query, user_id=user_id, metadata={"app_id": self.app_id, "role": "user"})
            self.memory.add(answer, user_id=user_id, metadata={"app_id": self.app_id, "role": "assistant"})

            return answer

        def get_memories(self, user_id=None):
            return self.memory.get_all(user_id=user_id)

        def generate_synthetic_data(self, user_id):
            today = datetime.now()
            order_date = (today - timedelta(days=10)).strftime("%B %d, %Y")
            expected_delivery = (today + timedelta(days=2)).strftime("%B %d, %Y")

            prompt = f"""Genera un perfil detallado de cliente y historial de pedidos para un cliente de TechGadgets.com con ID {user_id}. Incluye:
            1. Nombre del cliente e información básica
            2. Un pedido reciente de un dispositivo electrónico de alta gama (realizado el {order_date}, a entregar el {expected_delivery})
            3. Detalles del pedido (producto, precio, número de pedido)
            4. Dirección de envío del cliente
            5. 2-3 pedidos anteriores del último año
            6. 2-3 interacciones con servicio al cliente relacionadas con estos pedidos
            7. Preferencias o patrones en su comportamiento de compra

            Formatea la salida como un objeto JSON."""

            response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres una IA generadora de datos que crea perfiles de clientes e historiales de pedidos realistas. Siempre responde con JSON válido."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
            )

            customer_data = json.loads(response.choices[0].message.content)

            # Agregar datos generados a la memoria
            for key, value in customer_data.items():
                if isinstance(value, list):
                    for item in value:
                        self.memory.add(json.dumps(item), user_id=user_id, metadata={"app_id": self.app_id, "role": "system"})
                else:
                    self.memory.add(f"{key}: {json.dumps(value)}", user_id=user_id, metadata={"app_id": self.app_id, "role": "system"})

            return customer_data

    # Inicializar el Agente de Atención al Cliente IA
    support_agent = CustomerSupportAIAgent()

    # Barra lateral para ID de cliente y vista de memoria
    st.sidebar.title("Ingresa tu ID de Cliente:")
    previous_customer_id = st.session_state.get("previous_customer_id", None)
    customer_id = st.sidebar.text_input("Ingresa tu ID de Cliente")

    if customer_id != previous_customer_id:
        st.session_state.messages = []
        st.session_state.previous_customer_id = customer_id
        st.session_state.customer_data = None

    # Agregar botón para generar datos sintéticos
    if st.sidebar.button("Generar Datos Sintéticos"):
        if customer_id:
            with st.spinner("Generando datos del cliente..."):
                st.session_state.customer_data = support_agent.generate_synthetic_data(customer_id)
            st.sidebar.success("¡Datos sintéticos generados exitosamente!")
        else:
            st.sidebar.error("Por favor, ingresa un ID de cliente primero.")

    if st.sidebar.button("Ver Perfil del Cliente"):
        if st.session_state.customer_data:
            st.sidebar.json(st.session_state.customer_data)
        else:
            st.sidebar.info("No hay datos de cliente generados aún. Haz clic en 'Generar Datos Sintéticos' primero.")

    if st.sidebar.button("Ver Información de Memoria"):
        if customer_id:
            memories = support_agent.get_memories(user_id=customer_id)
            if memories:
                st.sidebar.write(f"Memoria para el cliente **{customer_id}**:")
                if memories and "results" in memories:
                    for memory in memories["results"]:
                        if "memory" in memory:
                            st.write(f"- {memory['memory']}")
            else:
                st.sidebar.info("No se encontró memoria para este ID de cliente.")
        else:
            st.sidebar.error("Por favor, ingresa un ID de cliente para ver la información de memoria.")

    # Inicializar el historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar el historial de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Aceptar entrada del usuario
    query = st.chat_input("¿Cómo puedo ayudarte hoy?")

    if query and customer_id:
        # Agregar mensaje del usuario al historial de chat
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # Generar y mostrar respuesta
        answer = support_agent.handle_query(query, user_id=customer_id)

        # Agregar respuesta del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

    elif not customer_id:
        st.error("Por favor, ingresa un ID de cliente para comenzar el chat.")

else:
    st.warning("Por favor, ingresa tu clave API de OpenAI para usar el agente de atención al cliente.")