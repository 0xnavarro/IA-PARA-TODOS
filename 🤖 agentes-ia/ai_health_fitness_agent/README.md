# Agente Planificador de Salud y Fitness IA 🏋️‍♂️

El **Planificador de Salud y Fitness IA** es un Agente personalizado de salud y fitness impulsado por el framework de Agentes IA de Phidata. Esta aplicación genera planes dietéticos y de fitness personalizados basados en datos del usuario como edad, peso, altura, nivel de actividad, preferencias dietéticas y objetivos de fitness.

## Características

- **Agente de Salud y Agente de Fitness**
    - La aplicación tiene dos agentes phidata que son especialistas en dar consejos de Dieta y consejos de Fitness/entrenamiento respectivamente.

- **Planes Dietéticos Personalizados**:
  - Genera planes detallados de comidas (desayuno, almuerzo, cena y snacks).
  - Incluye consideraciones importantes como hidratación, electrolitos e ingesta de fibra.
  - Soporta varias preferencias dietéticas como Keto, Vegetariana, Baja en Carbohidratos, etc.

- **Planes de Fitness Personalizados**:
  - Proporciona rutinas de ejercicio personalizadas basadas en objetivos de fitness.
  - Cubre calentamientos, entrenamientos principales y enfriamientos.
  - Incluye consejos prácticos de fitness y consejos de seguimiento de progreso.

- **Preguntas y Respuestas Interactivas**: Permite a los usuarios hacer preguntas de seguimiento sobre sus planes.


## Requisitos

La aplicación requiere las siguientes bibliotecas de Python:

- `phidata`
- `google-generativeai`
- `streamlit`

Asegúrate de que estas dependencias estén instaladas a través del archivo `requirements.txt` según sus versiones mencionadas

## Cómo Ejecutar

Sigue los pasos a continuación para configurar y ejecutar la aplicación:
Antes que nada, por favor obtén una Clave API gratuita de Gemini proporcionada por Google AI aquí: https://aistudio.google.com/apikey

1. **Clonar el Repositorio**:
   ```bash
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
   cd ai_agent_tutorials```

2. **Instalar las dependencias**
    ```bash
    pip install -r requirements.txt
    ```
3. **Ejecutar la aplicación Streamlit**
    ```bash
    streamlit run ai_health-fitness_agent/health_agent.py
    ```


