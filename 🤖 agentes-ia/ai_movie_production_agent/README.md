## 🎬 Agente de Producción de Películas IA
Esta aplicación Streamlit es un asistente de producción de películas impulsado por IA que ayuda a dar vida a tus ideas cinematográficas utilizando el modelo Claude 3.5 Sonnet. Automatiza el proceso de escritura de guiones y casting, permitiéndote crear conceptos de películas atractivos con facilidad.

### Características
- Genera esquemas de guiones basados en tu idea de película, género y público objetivo
- Sugiere actores adecuados para los roles principales, considerando sus actuaciones pasadas y disponibilidad actual
- Proporciona una visión general concisa del concepto de la película

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

- Regístrate para obtener una [cuenta de SerpAPI](https://serpapi.com/) y obtén tu clave API.

5. Ejecuta la Aplicación Streamlit
```bash
streamlit run movie_production_agent.py
```

### ¿Cómo Funciona?

El Agente de Producción de Películas IA utiliza tres componentes principales:
- **Guionista**: Desarrolla un esquema de guion atractivo con descripciones de personajes y puntos clave de la trama basados en la idea de película y el género dados.
- **Director de Casting**: Sugiere actores adecuados para los roles principales, considerando sus actuaciones pasadas y disponibilidad actual.
- **Productor de Películas**: Supervisa todo el proceso, coordinando entre el Guionista y el Director de Casting, y proporcionando una visión general concisa del concepto de la película.