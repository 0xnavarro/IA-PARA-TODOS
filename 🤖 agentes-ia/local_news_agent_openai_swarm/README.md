## 📰 Agente de Noticias Locales con OpenAI Swarm

Una aplicación de Streamlit que utiliza un enjambre de agentes de OpenAI para investigar y generar noticias locales. Los agentes trabajan juntos para recopilar información, verificar hechos y producir artículos de noticias bien investigados.

### Características

- **Equipo de Agentes Especializados**
  - 🔍 **Investigador**: Recopila información de múltiples fuentes
  - ✓ **Verificador de Hechos**: Verifica la precisión de la información
  - ✍️ **Escritor**: Redacta artículos coherentes y atractivos
  - 📊 **Editor**: Revisa y mejora el contenido final

- **Capacidades**
  - Investigación multimodal usando GPT-4V
  - Verificación de hechos en tiempo real
  - Generación de contenido estructurado
  - Edición y mejora colaborativa

### Cómo Empezar

1. Clona el repositorio
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd ai_agent_tutorials/local_news_agent_openai_swarm
```

2. Instala las dependencias
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno
```bash
# Crea un archivo .env con:
OPENAI_API_KEY=tu_clave_api_aquí
```

4. Ejecuta la aplicación
```bash
streamlit run news_agent.py
```

### Cómo Funciona

1. **Entrada del Usuario**
   - Proporciona un tema o evento de noticias locales
   - Especifica el área geográfica de interés
   - Selecciona el tipo de artículo deseado

2. **Proceso de Investigación**
   - El Investigador recopila información relevante
   - El Verificador de Hechos valida los datos
   - El Escritor crea el primer borrador
   - El Editor refina y finaliza el artículo

3. **Salida**
   - Artículo de noticias estructurado
   - Fuentes citadas y verificadas
   - Análisis de contexto local
   - Elementos visuales sugeridos