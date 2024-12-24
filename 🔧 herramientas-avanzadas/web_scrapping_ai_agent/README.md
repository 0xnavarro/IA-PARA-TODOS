## 💻 Agente IA de Web Scraping
Esta aplicación Streamlit te permite hacer scraping de un sitio web usando la API de OpenAI y la biblioteca scrapegraphai. Simplemente proporciona tu clave API de OpenAI, ingresa la URL del sitio web que deseas analizar y especifica qué quieres que el agente IA extraiga del sitio web.

### Características
- Haz scraping de cualquier sitio web proporcionando la URL
- Utiliza los LLMs de OpenAI (GPT-3.5-turbo o GPT-4) para scraping inteligente
- Personaliza la tarea de scraping especificando qué quieres que el agente IA extraiga

### ¿Cómo empezar?

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

4. Ejecuta la Aplicación Streamlit
```bash
streamlit run ai_scrapper.py
```

### ¿Cómo funciona?

- La aplicación te pide que ingreses tu clave API de OpenAI, que se utiliza para autenticar y acceder a los modelos de lenguaje de OpenAI.
- Puedes seleccionar el modelo de lenguaje deseado (GPT-3.5-turbo o GPT-4) para la tarea de scraping.
- Ingresa la URL del sitio web que deseas analizar en el campo de entrada de texto proporcionado.
- Especifica qué quieres que el agente IA extraiga del sitio web ingresando un prompt de usuario.
- La aplicación crea un objeto SmartScraperGraph usando la URL proporcionada, el prompt del usuario y la configuración de OpenAI.
- El objeto SmartScraperGraph hace scraping del sitio web y extrae la información solicitada usando el modelo de lenguaje especificado.
- Los resultados del scraping se muestran en la aplicación para que los veas