## 🛫 Agente de Viajes IA
Esta aplicación Streamlit es un agente de viajes impulsado por IA que genera itinerarios de viaje personalizados utilizando OpenAI GPT-4o. Automatiza el proceso de investigación, planificación y organización de tus vacaciones soñadas, permitiéndote explorar destinos emocionantes con facilidad.

### Características
- Investiga y descubre destinos de viaje emocionantes, actividades y alojamientos
- Personaliza tu itinerario según el número de días que deseas viajar
- Utiliza el poder de GPT-4o para generar planes de viaje inteligentes y personalizados

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

4. Obtén tu Clave API de SerpAPI

- Regístrate para obtener una [cuenta de SerpAPI](https://serpapi.com/) y obtén tu clave API.

5. Ejecuta la Aplicación Streamlit
```bash
streamlit run travel_agent.py
```

### ¿Cómo Funciona?

El Agente de Viajes IA tiene dos componentes principales:
- Investigador: Responsable de generar términos de búsqueda basados en el destino del usuario y la duración del viaje, y buscar en la web actividades y alojamientos relevantes utilizando SerpAPI.
- Planificador: Toma los resultados de la investigación y las preferencias del usuario para generar un borrador de itinerario personalizado que incluye actividades sugeridas.