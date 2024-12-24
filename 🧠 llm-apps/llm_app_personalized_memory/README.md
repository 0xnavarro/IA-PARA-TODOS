## 🧠 Aplicación LLM con Memoria Personalizada

Una aplicación de Streamlit que demuestra cómo implementar una capa de memoria personalizada para aplicaciones LLM. Esta aplicación permite a los usuarios mantener conversaciones contextuales mientras el sistema recuerda información importante de interacciones anteriores.

### Características

- **Memoria Personalizada**
  - Almacenamiento vectorial eficiente
  - Recuperación contextual precisa
  - Persistencia entre sesiones

- **Integración LLM**
  - Compatible con múltiples modelos
  - Procesamiento de lenguaje natural
  - Respuestas contextuales

- **Interfaz de Usuario**
  - Diseño limpio y moderno
  - Visualización de memoria
  - Gestión de sesiones

### Cómo Empezar

1. Clona el repositorio
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd llm_apps_with_memory_tutorials/llm_app_personalized_memory
```

2. Instala las dependencias
```bash
pip install -r requirements.txt
```

3. Configura las claves API
```bash
# Crea un archivo .env con:
OPENAI_API_KEY=tu_clave_api_aquí
```

4. Ejecuta la aplicación
```bash
streamlit run llm_app_memory.py
```

### Cómo Funciona

1. **Gestión de Memoria**
   - Almacena información importante
   - Recupera contexto relevante
   - Mantiene historial personalizado

2. **Procesamiento LLM**
   - Analiza las entradas del usuario
   - Genera respuestas contextuales
   - Integra información histórica

3. **Experiencia de Usuario**
   - Interacción natural
   - Respuestas personalizadas
   - Continuidad conversacional