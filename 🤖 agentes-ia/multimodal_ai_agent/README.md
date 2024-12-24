## 🧬 Agente IA Multimodal

Una aplicación de Streamlit que combina análisis de video y capacidades de búsqueda web utilizando el modelo Gemini 2.0 de Google. Este agente puede analizar videos subidos y responder preguntas combinando comprensión visual con búsqueda web.

### Características

- Análisis de video usando Gemini 2.0 Flash
- Integración de investigación web a través de DuckDuckGo
- Soporte para múltiples formatos de video (MP4, MOV, AVI)
- Procesamiento de video en tiempo real
- Análisis visual y textual combinado

### ¿Cómo empezar?

1. Clona el repositorio de GitHub

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd multimodal_ai_agents
```
2. Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
```
3. Obtén tu clave API de Google Gemini

- Regístrate para obtener una [cuenta de Google AI Studio](https://aistudio.google.com/apikey) y obtén tu clave API.

4. Configura tu clave API de Gemini como variable de entorno

```bash
GOOGLE_API_KEY=tu_clave_api_aquí
```

5. Ejecuta la aplicación Streamlit
```bash
streamlit run multimodal_agent.py
```