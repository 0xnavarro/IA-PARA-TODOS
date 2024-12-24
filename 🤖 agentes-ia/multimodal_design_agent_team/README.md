# Equipo de Agentes de Diseño IA Multimodal

Una aplicación de Streamlit que proporciona un análisis de diseño integral utilizando un equipo de agentes de IA especializados impulsados por el modelo Gemini de Google.

Esta aplicación aprovecha múltiples agentes de IA especializados para proporcionar un análisis integral de los diseños UI/UX de tu producto y de tus competidores, combinando comprensión visual, evaluación de la experiencia del usuario e información de investigación de mercado.

## Características

- **Equipo de Agentes de IA Legal Especializado**

   - 🎨 **Agente de Diseño Visual**: Evalúa elementos de diseño, patrones, esquemas de color, tipografía y jerarquía visual
   - 🔄 **Agente de Análisis UX**: Evalúa flujos de usuario, patrones de interacción, usabilidad y accesibilidad
   - 📊 **Agente de Análisis de Mercado**: Proporciona información de mercado, análisis de competidores y recomendaciones de posicionamiento
   
- **Múltiples Tipos de Análisis**: Elige entre Diseño Visual, UX y Análisis de Mercado
- **Análisis Comparativo**: Sube diseños de competidores para obtener información comparativa
- **Áreas de Enfoque Personalizables**: Selecciona aspectos específicos para un análisis detallado
- **Consciente del Contexto**: Proporciona contexto adicional para obtener información más relevante
- **Procesamiento en Tiempo Real**: Obtén análisis instantáneos con indicadores de progreso
- **Salida Estructurada**: Recibe información bien organizada y accionable

## Cómo Ejecutar

1. **Configurar el Entorno**
   ```bash
   # Clona el repositorio
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
   cd ai_agent_tutorials/multimodal_design_agent_team

   # Crea y activa un entorno virtual (opcional)
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate

   # Instala las dependencias
   pip install -r requirements.txt
   ```

2. **Obtener Clave API**
   - Visita [Google AI Studio](https://aistudio.google.com/apikey)
   - Genera una clave API

3. **Ejecutar la Aplicación**
   ```bash
   streamlit run design_agent_team.py
   ```

4. **Usar la Aplicación**
   - Ingresa tu clave API de Gemini en la barra lateral
   - Sube archivos de diseño (formatos soportados: JPG, JPEG, PNG)
   - Selecciona tipos de análisis y áreas de enfoque
   - Agrega contexto si es necesario
   - Haz clic en "Ejecutar Análisis" para obtener información


## Stack Técnico

- **Frontend**: Streamlit
- **Modelo IA**: Google Gemini 2.0
- **Procesamiento de Imágenes**: Pillow
- **Investigación de Mercado**: API de Búsqueda DuckDuckGo
- **Framework**: Phidata para orquestación de agentes

## Consejos para Mejores Resultados

- Sube imágenes claras y de alta resolución
- Incluye múltiples vistas/pantallas para un mejor contexto
- Agrega diseños de competidores para análisis comparativo
- Proporciona contexto específico sobre tu audiencia objetivo

