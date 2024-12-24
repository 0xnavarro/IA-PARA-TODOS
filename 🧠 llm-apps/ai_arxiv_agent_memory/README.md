## 📚 Agente Arxiv IA con Memoria

Una aplicación de Streamlit que implementa un asistente de investigación inteligente con memoria persistente. Este agente puede buscar, analizar y discutir artículos científicos de Arxiv mientras mantiene un registro de los intereses y consultas anteriores del usuario.

### Características

- **Búsqueda Inteligente**
  - Consultas semánticas
  - Filtrado por categoría
  - Ordenamiento por relevancia

- **Análisis de Artículos**
  - Resúmenes automáticos
  - Extracción de puntos clave
  - Conexiones entre papers

- **Memoria Personalizada**
  - Historial de búsquedas
  - Intereses del usuario
  - Recomendaciones adaptativas

### Cómo Empezar

1. Clona el repositorio
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd llm_apps_with_memory_tutorials/ai_arxiv_agent_memory
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
streamlit run ai_arxiv_agent_memory.py
```

### Cómo Funciona

1. **Entrada del Usuario**
   - Tema de investigación
   - Palabras clave
   - Filtros específicos

2. **Procesamiento**
   - Búsqueda en Arxiv
   - Análisis de contenido
   - Generación de insights

3. **Resultados**
   - Lista de artículos relevantes
   - Resúmenes personalizados
   - Recomendaciones relacionadas