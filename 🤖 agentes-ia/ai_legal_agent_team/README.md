# 👨‍⚖️ Equipo de Agentes Legales IA

Una aplicación Streamlit que simula un equipo legal de servicio completo utilizando múltiples agentes de IA para analizar documentos legales y proporcionar información legal integral. Cada agente representa un rol de especialista legal diferente, desde investigación y análisis de contratos hasta planificación estratégica, trabajando juntos para proporcionar análisis y recomendaciones legales exhaustivas.

## Características

- **Equipo Especializado de Agentes Legales IA**
  - **Investigador Legal**: Equipado con la herramienta de búsqueda DuckDuckGo para encontrar y citar casos legales relevantes y precedentes. Proporciona resúmenes detallados de investigación con fuentes y referencias a secciones específicas de los documentos cargados.
  
  - **Analista de Contratos**: Se especializa en la revisión exhaustiva de contratos, identificando términos clave, obligaciones y posibles problemas. Hace referencia a cláusulas específicas de los documentos para un análisis detallado.
  
  - **Estratega Legal**: Se centra en desarrollar estrategias legales integrales, proporcionando recomendaciones accionables mientras considera tanto riesgos como oportunidades.
  
  - **Líder del Equipo**: Coordina el análisis entre los miembros del equipo, asegura respuestas integrales, recomendaciones debidamente fundamentadas y referencias a partes específicas del documento. Actúa como coordinador del Equipo de Agentes para los tres agentes.

- **Tipos de Análisis de Documentos**
  - Revisión de Contratos - Realizado por el Analista de Contratos
  - Investigación Legal - Realizado por el Investigador Legal
  - Evaluación de Riesgos - Realizado por el Estratega Legal, Analista de Contratos
  - Verificación de Cumplimiento - Realizado por el Estratega Legal, Investigador Legal, Analista de Contratos
  - Consultas Personalizadas - Realizado por el Equipo de Agentes - Investigador Legal, Estratega Legal, Analista de Contratos

## Cómo Ejecutar

1. **Configurar el Entorno**
   ```bash
   # Clonar el repositorio
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
   cd ai_legal_agent_team
   
   # Instalar dependencias
   pip install -r requirements.txt
   ```

2. **Configurar Claves API**
   - Obtener clave API de OpenAI desde [OpenAI Platform](https://platform.openai.com)
   - Obtener clave API y URL de Qdrant desde [Qdrant Cloud](https://cloud.qdrant.io)

3. **Ejecutar la Aplicación**
   ```bash
   streamlit run legal_agent_team.py
   ```
4. **Usar la Interfaz**
   - Ingresar credenciales API
   - Cargar un documento legal (PDF)
   - Seleccionar tipo de análisis
   - Agregar consultas personalizadas si es necesario
   - Ver resultados del análisis

## Notas

- Solo soporta documentos PDF
- Utiliza GPT-4o para el análisis
- Utiliza text-embedding-3-small para embeddings
- Requiere conexión estable a internet
- Se aplican costos de uso de API
