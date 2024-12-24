## 🦙 Uso de Herramientas con Llama3 Local
Esta aplicación Streamlit demuestra el llamado a funciones con el modelo Llama3 local usando Ollama. Permite a los usuarios interactuar con un asistente de IA que puede acceder a herramientas específicas basadas en la selección del usuario.

### Características
- Utiliza el modelo Llama3 local a través de Ollama como LLM
- Integra YFinance para la obtención de datos bursátiles y SerpAPI para capacidades de búsqueda web
- Selección dinámica de herramientas a través de una barra lateral amigable
- Interfaz de chat en tiempo real con el asistente de IA

### Cómo Empezar

1. Clonar el repositorio de GitHub

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd local-llama3-tool-use
```
2. Instalar las dependencias requeridas:

```bash
pip install -r requirements.txt
```

3. Obtener tu Clave API de OpenAI

- Configura tu clave API de SerpAPI: Exporta tu clave API de SerpAPI como una variable de entorno.
```bash
export SERPAPI_API_KEY=tu_clave_api_aquí
```

4. Ejecutar la Aplicación Streamlit
```bash
streamlit run llama3_tool_use.py
```

## ¿Cómo Funciona?

1. **Selección de Herramientas:** Los usuarios pueden seleccionar qué herramientas (YFinance y/o SerpAPI) quieren que el asistente use a través de casillas de verificación en la barra lateral.

2. **Inicialización del Asistente:** La aplicación inicializa o actualiza el asistente basado en las herramientas seleccionadas.

3. **Interfaz de Chat:** Los usuarios pueden hacer preguntas a través de una entrada de chat, y el asistente responde usando las herramientas habilitadas.

4. **Respuesta en Tiempo Real:** La respuesta del asistente se muestra en tiempo real, con un indicador de escritura.

5. **Visualización de Uso de Herramientas:** La aplicación muestra qué herramientas están actualmente habilitadas en la barra lateral.