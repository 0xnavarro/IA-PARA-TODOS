from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.playground import Playground, serve_playground_app

reasoning_agent = Agent(name="Reasoning Agent", model=Ollama(id="qwq:32b"), markdown=True)

# Interfaz de usuario para el agente de razonamiento

# Ejecutar la aplicación Playground
app = Playground(agents=[reasoning_agent]).get_app()

# Run the Playground app
if __name__ == "__main__":
    serve_playground_app("local_ai_reasoning_agent:app", reload=True)