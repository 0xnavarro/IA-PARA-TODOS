## 🎯 Asistente de Búsqueda con IA Generativa
Esta aplicación Streamlit combina el poder de los motores de búsqueda y los LLMs para proporcionarte respuestas precisas a tus consultas. Aprovechando GPT-4o de OpenAI y el motor de búsqueda DuckDuckGo, este asistente de búsqueda con IA entrega respuestas precisas y concisas a tus preguntas.

### Características
- Obtén respuestas precisas a tus consultas
- Utiliza el motor de búsqueda DuckDuckGo para búsquedas web
- Usa OpenAI GPT-4o para la generación inteligente de respuestas

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
streamlit run ai_websearch.py
```

### ¿Cómo funciona?

- Al ejecutar la aplicación, se te pedirá que ingreses tu clave API de OpenAI. Esta clave se utiliza para autenticar y acceder a los modelos de lenguaje de OpenAI.

- Una vez que proporciones una clave API válida, se crea una instancia de la clase Assistant. Este asistente utiliza el modelo de lenguaje GPT-4 de OpenAI y la herramienta del motor de búsqueda DuckDuckGo.

- Ingresa tu consulta de búsqueda en el campo de entrada de texto proporcionado.

- El asistente realizará los siguientes pasos:
    - Realizar una búsqueda web usando DuckDuckGo basada en tu consulta
    - Analizar los resultados de búsqueda y extraer información relevante
    - Generar una respuesta concisa y dirigida usando el modelo de lenguaje GPT-4

- La respuesta precisa se mostrará en la aplicación, proporcionándote la información que necesitas.