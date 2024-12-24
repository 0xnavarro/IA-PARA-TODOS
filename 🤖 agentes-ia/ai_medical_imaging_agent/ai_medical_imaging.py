import os
from PIL import Image
from phi.agent import Agent
from phi.model.google import Gemini
import streamlit as st
from phi.tools.duckduckgo import DuckDuckGo

if "GOOGLE_API_KEY" not in st.session_state:
    st.session_state.GOOGLE_API_KEY = None

with st.sidebar:
    st.title("ℹ️ Configuración")
    
    if not st.session_state.GOOGLE_API_KEY:
        api_key = st.text_input(
            "Ingresa tu Clave API de Google:",
            type="password"
        )
        st.caption(
            "Obtén tu clave API desde [Google AI Studio]"
            "(https://aistudio.google.com/apikey) 🔑"
        )
        if api_key:
            st.session_state.GOOGLE_API_KEY = api_key
            st.success("¡Clave API guardada!")
            st.rerun()
    else:
        st.success("La Clave API está configurada")
        if st.button("🔄 Restablecer Clave API"):
            st.session_state.GOOGLE_API_KEY = None
            st.rerun()
    
    st.info(
        "Esta herramienta proporciona análisis de datos de imágenes médicas impulsado por IA "
        "utilizando visión por computadora avanzada y experiencia radiológica."
    )
    st.warning(
        "⚠DESCARGO DE RESPONSABILIDAD: Esta herramienta es solo para propósitos educativos e informativos. "
        "Todos los análisis deben ser revisados por profesionales de la salud calificados. "
        "No tome decisiones médicas basadas únicamente en este análisis."
    )

medical_agent = Agent(
    model=Gemini(
        api_key=st.session_state.GOOGLE_API_KEY,
        id="gemini-2.0-flash-exp"
    ),
    tools=[DuckDuckGo()],
    markdown=True
) if st.session_state.GOOGLE_API_KEY else None

if not medical_agent:
    st.warning("Por favor, configura tu clave API en la barra lateral para continuar")

# Consulta de Análisis Médico
query = """
Eres un experto en imágenes médicas altamente capacitado con amplio conocimiento en radiología e imágenes diagnósticas. Analiza la imagen médica del paciente y estructura tu respuesta de la siguiente manera:

### 1. Tipo de Imagen y Región
- Especifica la modalidad de imagen (Rayos X/MRI/Tomografía/Ultrasonido/etc.)
- Identifica la región anatómica y la posición del paciente
- Comenta sobre la calidad de la imagen y la adecuación técnica

### 2. Hallazgos Clave
- Enumera las observaciones primarias de manera sistemática
- Nota cualquier anomalía en la imagen del paciente con descripciones precisas
- Incluye medidas y densidades donde sea relevante
- Describe ubicación, tamaño, forma y características
- Califica la severidad: Normal/Leve/Moderada/Severa

### 3. Evaluación Diagnóstica
- Proporciona diagnóstico principal con nivel de confianza
- Enumera diagnósticos diferenciales en orden de probabilidad
- Apoya cada diagnóstico con evidencia observada en la imagen del paciente
- Nota cualquier hallazgo crítico o urgente

### 4. Explicación Amigable para el Paciente
- Explica los hallazgos en un lenguaje simple y claro que el paciente pueda entender
- Evita jerga médica o proporciona definiciones claras
- Incluye analogías visuales si son útiles
- Aborda preocupaciones comunes del paciente relacionadas con estos hallazgos

### 5. Contexto de Investigación
IMPORTANTE: Usa la herramienta de búsqueda DuckDuckGo para:
- Encontrar literatura médica reciente sobre casos similares
- Buscar protocolos de tratamiento estándar
- Proporcionar una lista de enlaces médicos relevantes
- Investigar cualquier avance tecnológico relevante
- Incluir 2-3 referencias clave para apoyar tu análisis

Formatea tu respuesta usando encabezados claros de markdown y viñetas. Sé conciso pero exhaustivo.
"""

st.title("🏥 Agente de Diagnóstico de Imágenes Médicas")
st.write("Sube una imagen médica para análisis profesional")

# Crear contenedores para mejor organización
upload_container = st.container()
image_container = st.container()
analysis_container = st.container()

with upload_container:
    uploaded_file = st.file_uploader(
        "Subir Imagen Médica",
        type=["jpg", "jpeg", "png", "dicom"],
        help="Formatos soportados: JPG, JPEG, PNG, DICOM"
    )

if uploaded_file is not None:
    with image_container:
        # Centrar la imagen usando columnas
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image = Image.open(uploaded_file)
            # Calcular relación de aspecto para redimensionar
            width, height = image.size
            aspect_ratio = width / height
            new_width = 500
            new_height = int(new_width / aspect_ratio)
            resized_image = image.resize((new_width, new_height))
            
            st.image(
                resized_image,
                caption="Imagen Médica Subida",
                use_container_width=True
            )
            
            analyze_button = st.button(
                "🔍 Analizar Imagen",
                type="primary",
                use_container_width=True
            )
    
    with analysis_container:
        if analyze_button:
            image_path = "temp_medical_image.png"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("🔄 Analizando imagen... Por favor espera."):
                try:
                    response = medical_agent.run(query, images=[image_path])
                    st.markdown("### 📋 Resultados del Análisis")
                    st.markdown("---")
                    st.markdown(response.content)
                    st.markdown("---")
                    st.caption(
                        "Nota: Este análisis es generado por IA y debe ser revisado por "
                        "un profesional de la salud calificado."
                    )
                except Exception as e:
                    st.error(f"Error de análisis: {e}")
                finally:
                    if os.path.exists(image_path):
                        os.remove(image_path)
else:
    st.info("👆 Por favor, sube una imagen médica para comenzar el análisis")
