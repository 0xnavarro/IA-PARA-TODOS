## 📰 Investigador IA Multi-Agente
Esta aplicación de Streamlit te permite investigar las principales historias y usuarios en HackerNews utilizando un equipo de asistentes de IA con GPT-4o.

### Características
- Investiga las principales historias y usuarios en HackerNews
- Utiliza un equipo de asistentes de IA especializados en investigación de historias y usuarios
- Genera publicaciones de blog, informes y contenido para redes sociales basado en tus consultas de investigación

### ¿Cómo empezar?

1. Clona el repositorio de GitHub

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
```
2. Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
```
3. Obtén tu clave API de OpenAI

- Regístrate para obtener una [cuenta de OpenAI](https://platform.openai.com/) (o el proveedor de LLM de tu elección) y obtén tu clave API.

4. Ejecuta la aplicación Streamlit
```bash
streamlit run research_agent.py
```

### ¿Cómo funciona?

- Al ejecutar la aplicación, se te pedirá que ingreses tu clave API de OpenAI. Esta clave se utiliza para autenticar y acceder a los modelos de lenguaje de OpenAI.
- Una vez que proporciones una clave API válida, se crearán tres instancias de la clase Assistant:
    - **story_researcher**: Especializado en investigar historias de HackerNews.
    - **user_researcher**: Se enfoca en investigar usuarios de HackerNews y leer artículos desde URLs.
    - **hn_assistant**: Un asistente de equipo que coordina los esfuerzos de investigación de los investigadores de historias y usuarios.

- Ingresa tu consulta de investigación en el campo de texto proporcionado. Esto podría ser un tema, palabra clave o pregunta específica relacionada con historias o usuarios de HackerNews.
- El hn_assistant orquestará el proceso de investigación delegando tareas al story_researcher y user_researcher según tu consulta.
- Los asistentes de IA recopilarán información relevante de HackerNews utilizando las herramientas proporcionadas y generarán una respuesta integral utilizando el modelo de lenguaje GPT-4.
- El contenido generado, que podría ser una publicación de blog, informe o publicación en redes sociales, se mostrará en la aplicación para que lo revises y uses.

