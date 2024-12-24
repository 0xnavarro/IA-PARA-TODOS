from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.lancedb import LanceDb, SearchType
from phi.playground import Playground, serve_playground_app
from phi.tools.duckduckgo import DuckDuckGo

db_uri = "tmp/lancedb"
# Crear una base de conocimientos a partir de un PDF
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    # Usar LanceDB como base de datos vectorial
    vector_db=LanceDb(table_name="recipes", uri=db_uri, search_type=SearchType.vector),
)
# Cargar la base de conocimientos: Comentar después de la primera ejecución
knowledge_base.load(upsert=True)

# Crear el agente RAG
rag_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    agent_id="rag-agent",
    knowledge=knowledge_base,  # Agregar la base de conocimientos al agente
    tools=[DuckDuckGo()],  # Agregar herramienta de búsqueda web
    show_tool_calls=True,  # Mostrar llamadas a herramientas
    markdown=True,  # Habilitar formato markdown
)

# Configurar la aplicación de playground
app = Playground(agents=[rag_agent]).get_app()

if __name__ == "__main__":
    # Iniciar el servidor del playground
    serve_playground_app("rag_agent:app", reload=True)