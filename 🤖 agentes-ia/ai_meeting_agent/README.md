## 📝 Agente de Preparación de Reuniones IA
Esta aplicación Streamlit aprovecha múltiples agentes de IA para crear materiales completos de preparación para reuniones. Utiliza GPT-4 de OpenAI, Claude de Anthropic y la API de Serper para búsquedas web para generar análisis de contexto, conocimientos de la industria, estrategias de reunión e informes ejecutivos.

### Características

- Sistema de IA multi-agente para una preparación exhaustiva de reuniones
- Utiliza los modelos GPT-4 de OpenAI y Claude de Anthropic
- Capacidad de búsqueda web usando la API de Serper
- Genera análisis de contexto detallados, conocimientos de la industria, estrategias de reunión e informes ejecutivos

### ¿Cómo Comenzar?

1. Clona el repositorio de GitHub

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
```
2. Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
```
3. Obtén tu Clave API de Anthropic

- Regístrate para obtener una [cuenta de Anthropic](https://console.anthropic.com) (o el proveedor de LLM de tu elección) y obtén tu clave API.

4. Obtén tu Clave API de SerpAPI

- Regístrate para obtener una [cuenta de Serper API](https://serper.dev/) y obtén tu clave API.

5. Obtén tu Clave API de OpenAI

- Regístrate para obtener una [cuenta de OpenAI](https://platform.openai.com/) (o el proveedor de LLM de tu elección) y obtén tu clave API.

6. Ejecuta la Aplicación Streamlit
```bash
streamlit run meeting_agent.py
```