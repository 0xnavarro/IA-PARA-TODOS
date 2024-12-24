# Agente de Diagnóstico de Imágenes Médicas

Un Agente de Diagnóstico de Imágenes Médicas construido sobre phidata impulsado por Gemini 2.0 Flash Experimental que proporciona análisis asistido por IA de imágenes médicas de varios escaneos. El agente actúa como un experto en diagnóstico de imágenes médicas para analizar varios tipos de imágenes y videos médicos, proporcionando información diagnóstica detallada y explicaciones.

## Características

- **Análisis Integral de Imágenes**
  - Identificación del Tipo de Imagen (Rayos X, MRI, Tomografía, ultrasonido)
  - Detección de Región Anatómica
  - Hallazgos y Observaciones Clave
  - Detección de Anomalías Potenciales
  - Evaluación de Calidad de Imagen
  - Investigación y Referencia

## Cómo Ejecutar

1. **Configurar el Entorno**
   ```bash
   # Clonar el repositorio
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
   cd ai_agent_tutorials/ai_medical_imaging_agent

   # Instalar dependencias
   pip install -r requirements.txt
   ```

2. **Configurar Claves API**
   - Obtén la clave API de Google desde [Google AI Studio](https://aistudio.google.com)

3. **Ejecutar la Aplicación**
   ```bash
   streamlit run ai_medical_imaging.py
   ```

## Componentes de Análisis

- **Tipo de Imagen y Región**
  - Identifica la modalidad de imagen
  - Especifica la región anatómica

- **Hallazgos Clave**
  - Listado sistemático de observaciones
  - Descripciones detalladas de apariencia
  - Resaltado de anomalías

- **Evaluación Diagnóstica**
  - Clasificación de diagnósticos potenciales
  - Diagnósticos diferenciales
  - Evaluación de severidad

- **Explicaciones Amigables para el Paciente**
  - Terminología simplificada
  - Explicaciones detalladas de primeros principios
  - Puntos de referencia visuales

## Notas

- Utiliza Gemini 2.0 Flash para el análisis
- Requiere conexión a internet estable
- Se aplican costos de uso de API
- Solo para propósitos educativos y de desarrollo
- No es un reemplazo para el diagnóstico médico profesional

## Descargo de Responsabilidad

Esta herramienta es solo para propósitos educativos e informativos. Todos los análisis deben ser revisados por profesionales de la salud calificados. No tome decisiones médicas basadas únicamente en este análisis.