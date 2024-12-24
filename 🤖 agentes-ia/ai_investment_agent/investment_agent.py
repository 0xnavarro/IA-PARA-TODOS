# Importar las bibliotecas requeridas
import streamlit as st
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools

# Configurar la aplicación Streamlit
st.title("Agente de Inversiones IA 📈🤖")
st.caption("Esta aplicación te permite comparar el rendimiento de dos acciones y generar informes detallados.")

# Obtener la clave API de OpenAI del usuario
openai_api_key = st.text_input("Clave API de OpenAI", type="password")

if openai_api_key:
    # Crear una instancia del Asistente
    assistant = Assistant(
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
        show_tool_calls=True,
    )

    # Campos de entrada para las acciones a comparar
    stock1 = st.text_input("Ingresa el símbolo de la primera acción")
    stock2 = st.text_input("Ingresa el símbolo de la segunda acción")

    if stock1 and stock2:
        # Obtener la respuesta del asistente
        query = f"Compara {stock1} con {stock2}. Utiliza todas las herramientas disponibles."
        response = assistant.run(query, stream=False)
        st.write(response)