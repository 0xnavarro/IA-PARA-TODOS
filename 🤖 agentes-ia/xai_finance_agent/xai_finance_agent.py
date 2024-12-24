# importar las bibliotecas de Python necesarias
from phi.agent import Agent
from phi.model.xai import xAI
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.playground import Playground, serve_playground_app

# crear el agente financiero IA
agent = Agent(
    name="Agente Financiero xAI",
    model = xAI(id="grok-beta"),
    tools=[DuckDuckGo(), YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    instructions = ["Usa siempre tablas para mostrar datos financieros/numericos. Para datos de texto usa viñetas y pequeños párrafos."],
    show_tool_calls = True,
    markdown = True,
    )

# Interfaz de usuario para el agente financiero
app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("xai_finance_agent:app", reload=True)