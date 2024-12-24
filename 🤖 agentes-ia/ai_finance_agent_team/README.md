## 💲 Equipo de Agentes Financieros IA con Acceso Web
Este script demuestra cómo construir un equipo de agentes IA que trabajan juntos como analistas financieros utilizando GPT-4o en solo 20 líneas de código Python. El sistema combina capacidades de búsqueda web con herramientas de análisis de datos financieros para proporcionar información financiera integral.

### Características
- Sistema multi-agente con roles especializados:
    - Agente Web para investigación general en internet
    - Agente Financiero para análisis financiero detallado
    - Agente de Equipo para coordinar entre agentes
- Acceso a datos financieros en tiempo real a través de YFinance
- Capacidades de búsqueda web usando DuckDuckGo
- Almacenamiento persistente de interacciones de agentes usando SQLite

### ¿Cómo Comenzar?

1. Clona el repositorio de GitHub
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
```

2. Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
```

3. Obtén tu Clave API de OpenAI

- Regístrate para obtener una [cuenta de OpenAI](https://platform.openai.com/) (o el proveedor de LLM de tu elección) y obtén tu clave API.
- Establece tu clave API de OpenAI como una variable de entorno:
```bash
export OPENAI_API_KEY='tu-clave-api-aquí'
```

4. Ejecuta el equipo de Agentes IA
```bash
python3 finance_agent_team.py
```

5. Abre tu navegador web y navega a la URL proporcionada en la salida de la consola para interactuar con el equipo de agentes IA a través de la interfaz de playground.
