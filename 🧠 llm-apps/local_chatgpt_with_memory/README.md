## 🧠 ChatGPT Local con Memoria

Una aplicación de Streamlit que implementa un chatbot similar a ChatGPT usando Llama2 localmente, con una capa de memoria persistente. Esta aplicación permite a los usuarios tener conversaciones naturales mientras mantiene el contexto y recuerda información importante.

### Características

- **Procesamiento Local**
  - Utiliza Llama2 para procesamiento en el dispositivo
  - Sin dependencia de servicios en la nube
  - Control total sobre el modelo y los datos

- **Memoria Persistente**
  - Almacenamiento vectorial con Qdrant
  - Recuperación de contexto relevante
  - Historial de conversación personalizado

- **Interfaz Amigable**
  - Diseño similar a ChatGPT
  - Historial de chat en tiempo real
  - Indicadores de estado claros

### Cómo Empezar

1. Clona el repositorio
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd llm_apps_with_memory_tutorials/local_chatgpt_with_memory
```

2. Instala las dependencias
```bash
pip install -r requirements.txt
```

3. Configura Llama2 y Qdrant
```bash
# Descarga el modelo
ollama pull llama2

# Inicia Qdrant
docker pull qdrant/qdrant
docker run -p 6333:6333 qdrant/qdrant
```

4. Ejecuta la aplicación
```bash
streamlit run local_chatgpt_memory.py
```

### Cómo Funciona

1. **Inicialización**
   - Carga el modelo Llama2 localmente
   - Configura la base de datos vectorial Qdrant
   - Prepara el sistema de memoria

2. **Interacción**
   - El usuario ingresa mensajes
   - El sistema busca contexto relevante
   - Llama2 genera respuestas coherentes

3. **Gestión de Memoria**
   - Almacena nuevas interacciones
   - Recupera información relacionada
   - Mantiene el contexto conversacional