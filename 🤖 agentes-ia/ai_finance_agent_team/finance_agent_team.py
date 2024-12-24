from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.playground import Playground, serve_playground_app

web_agent = Agent(
    name="Agente Web",
    role="Buscar información en la web",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    storage=SqlAgentStorage(table_name="web_agent", db_file="agents.db"),
    add_history_to_messages=True,
    markdown=True,
)

finance_agent = Agent(
    name="Agente Financiero",
    role="Obtener datos financieros",
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Siempre usa tablas para mostrar datos"],
    storage=SqlAgentStorage(table_name="finance_agent", db_file="agents.db"),
    add_history_to_messages=True,
    markdown=True,
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    name="Equipo de Agentes (Web+Finanzas)",
    model=OpenAIChat(id="gpt-4o"),
    show_tool_calls=True,
    markdown=True,
)

app = Playground(agents=[agent_team]).get_app()

if __name__ == "__main__":
    serve_playground_app("finance_agent_team:app", reload=True)