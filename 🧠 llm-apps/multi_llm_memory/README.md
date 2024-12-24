## 🧠 Aplicación Multi-LLM con Memoria

Una aplicación de Streamlit que demuestra el uso de múltiples modelos de lenguaje (LLMs) con memoria compartida. Esta aplicación permite a los usuarios interactuar con diferentes LLMs mientras mantiene un contexto conversacional coherente.

### Características

- **Múltiples LLMs**
  - GPT-4 para razonamiento complejo
  - Claude para análisis detallado
  - Llama2 para procesamiento local
  
- **Memoria Compartida**
  - Historial de conversación persistente
  - Contexto compartido entre modelos
  - Recuperación de información previa

- **Interfaz Intuitiva**
  - Selección de modelo sencilla
  - Visualización del historial
  - Indicadores de estado claros

### Cómo Empezar

1. Clona el repositorio
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd llm_apps_with_memory_tutorials/multi_llm_memory
```

2. Instala las dependencias
```bash
pip install -r requirements.txt
```

3. Configura las claves API
```bash
# Crea un archivo .env con:
OPENAI_API_KEY=tu_clave_api_aquí
ANTHROPIC_API_KEY=tu_clave_api_aquí
```

4. Ejecuta la aplicación
```bash
streamlit run multi_llm_memory.py
```

### Cómo Funciona

1. **Selección de Modelo**
   - Elige entre GPT-4, Claude o Llama2
   - Cada modelo tiene sus fortalezas únicas

2. **Interacción**
   - Ingresa tu mensaje o pregunta
   - El modelo seleccionado responde
   - La conversación se guarda en memoria

3. **Memoria Compartida**
   - El historial persiste entre cambios de modelo
   - Los modelos pueden referenciar información previa
   - Mantiene la coherencia conversacional