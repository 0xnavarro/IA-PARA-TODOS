## 📊 Agente Financiero IA con xAI Grok
Esta aplicación crea un agente de análisis financiero impulsado por el modelo Grok de xAI, combinando datos bursátiles en tiempo real con capacidades de búsqueda web. Proporciona información financiera estructurada a través de una interfaz de juego interactiva.

### Características

- Impulsado por el modelo Grok-beta de xAI
- Análisis de datos bursátiles en tiempo real a través de YFinance
- Capacidades de búsqueda web mediante DuckDuckGo
- Salida formateada con tablas para datos financieros
- Interfaz de juego interactiva

### ¿Cómo empezar?

1. Clona el repositorio de GitHub
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
```

2. Instala las dependencias requeridas:

```bash
cd ai_agent_tutorials/xai_finance_agent
pip install -r requirements.txt
```

3. Obtén tu clave API de OpenAI

- Regístrate para obtener una [cuenta API de xAI](https://console.x.ai/)
- Configura tu variable de entorno XAI_API_KEY.
```bash
export XAI_API_KEY='tu-clave-api-aquí'
```

4. Ejecuta el equipo de Agentes IA
```bash
python xai_finance_agent.py
```

5. Abre tu navegador web y navega a la URL proporcionada en la salida de la consola para interactuar con el agente financiero IA a través de la interfaz de juego.
