from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import streamlit as st
from PIL import Image
from typing import List, Optional

def initialize_agents(api_key: str) -> tuple[Agent, Agent, Agent]:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)
        
        vision_agent = Agent(
            model=model,
            instructions=[
                "Eres un experto en análisis visual que:",
                "1. Identifica elementos de diseño, patrones y jerarquía visual",
                "2. Analiza esquemas de color, tipografía y diseños",
                "3. Detecta componentes de UI y sus relaciones",
                "4. Evalúa la consistencia visual y la marca",
                "Sé específico y técnico en tu análisis"
            ],
            markdown=True
        )

        ux_agent = Agent(
            model=model,
            instructions=[
                "Eres un experto en análisis UX que:",
                "1. Evalúa flujos de usuario y patrones de interacción",
                "2. Identifica problemas de usabilidad y oportunidades",
                "3. Sugiere mejoras UX basadas en mejores prácticas",
                "4. Analiza accesibilidad y diseño inclusivo",
                "Enfócate en ideas centradas en el usuario y mejoras prácticas"
            ],
            markdown=True
        )

        market_agent = Agent(
            model=model,
            tools=[DuckDuckGo(search=True)],
            instructions=[
                "Eres un experto en investigación de mercado que:",
                "1. Identifica tendencias de mercado y patrones de competidores",
                "2. Analiza productos y características similares",
                "3. Sugiere posicionamiento de mercado y oportunidades",
                "4. Proporciona información específica de la industria",
                "Enfócate en inteligencia de mercado accionable"
            ],
            markdown=True
        )
        
        return vision_agent, ux_agent, market_agent
    except Exception as e:
        st.error(f"Error al inicializar los agentes: {str(e)}")
        return None, None, None

# Barra lateral para la entrada de clave API
with st.sidebar:
    st.header("🔑 Configuración de API")

    if "api_key_input" not in st.session_state:
        st.session_state.api_key_input = ""
        
    api_key = st.text_input(
        "Ingresa tu Clave API de Gemini",
        value=st.session_state.api_key_input,
        type="password",
        help="Obtén tu clave API desde Google AI Studio",
        key="api_key_widget"  
    )

    if api_key != st.session_state.api_key_input:
        st.session_state.api_key_input = api_key
    
    if api_key:
        st.success("¡Clave API proporcionada! ✅")
    else:
        st.warning("Por favor, ingresa tu clave API para continuar")
        st.markdown("""
        Para obtener tu clave API:
        1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
        """)

st.title("Equipo de Agentes de Diseño IA Multimodal")

if st.session_state.api_key_input:
    vision_agent, ux_agent, market_agent = initialize_agents(st.session_state.api_key_input)
    
    if all([vision_agent, ux_agent, market_agent]):
        # Sección de carga de archivos
        st.header("📤 Subir Contenido")
        col1, space, col2 = st.columns([1, 0.1, 1])
        
        with col1:
            design_files = st.file_uploader(
                "Sube Diseños UI/UX",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                key="designs"
            )
            
            if design_files:
                for file in design_files:
                    image = Image.open(file)
                    st.image(image, caption=file.name, use_container_width=True)

        with col2:
            competitor_files = st.file_uploader(
                "Sube Diseños de Competidores (Opcional)",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                key="competitors"
            )
            
            if competitor_files:
                for file in competitor_files:
                    image = Image.open(file)
                    st.image(image, caption=f"Competidor: {file.name}", use_container_width=True)

        # Configuración de Análisis
        st.header("🎯 Configuración de Análisis")

        analysis_types = st.multiselect(
            "Selecciona Tipos de Análisis",
            ["Diseño Visual", "Experiencia de Usuario", "Análisis de Mercado"],
            default=["Diseño Visual"]
        )

        specific_elements = st.multiselect(
            "Áreas de Enfoque",
            ["Esquema de Color", "Tipografía", "Diseño", "Navegación", 
             "Interacciones", "Accesibilidad", "Marca", "Ajuste de Mercado"]
        )

        context = st.text_area(
            "Contexto Adicional",
            placeholder="Describe tu producto, audiencia objetivo o preocupaciones específicas..."
        )

        # Proceso de Análisis
        if st.button("🚀 Ejecutar Análisis", type="primary"):
            if design_files:
                try:
                    st.header("📊 Resultados del Análisis")
                    
                    # Procesar imágenes una vez
                    def process_images(files):
                        processed_images = []
                        for file in files:
                            try:
                                # Crear una ruta de archivo temporal para la imagen
                                import tempfile
                                import os

                                temp_dir = tempfile.gettempdir()
                                temp_path = os.path.join(temp_dir, f"temp_{file.name}")
                                
                                # Guardar el archivo subido en la ubicación temporal
                                with open(temp_path, "wb") as f:
                                    f.write(file.getvalue())
                                
                                # Agregar la ruta a las imágenes procesadas
                                processed_images.append(temp_path)
                                
                            except Exception as e:
                                st.error(f"Error al procesar la imagen {file.name}: {str(e)}")
                                continue
                        return processed_images
                    
                    design_images = process_images(design_files)
                    competitor_images = process_images(competitor_files) if competitor_files else []
                    all_images = design_images + competitor_images
                    
                    # Análisis de Diseño Visual
                    if "Diseño Visual" in analysis_types and design_files:
                        with st.spinner("🎨 Analizando diseño visual..."):
                            if all_images:
                                vision_prompt = f"""
                                Analiza estos diseños enfocándote en: {', '.join(specific_elements)}
                                Contexto adicional: {context}
                                Proporciona ideas específicas sobre elementos de diseño visual.
                                
                                Por favor, formatea tu respuesta con encabezados claros y viñetas.
                                Enfócate en observaciones concretas e ideas accionables.
                                """
                                
                                response = vision_agent.run(
                                    message=vision_prompt,
                                    images=all_images
                                )
                                
                                st.subheader("🎨 Análisis de Diseño Visual")
                                st.markdown(response.content)
                    
                    # Análisis UX
                    if "Experiencia de Usuario" in analysis_types:
                        with st.spinner("🔄 Analizando experiencia de usuario..."):
                            if all_images:
                                ux_prompt = f"""
                                Evalúa la experiencia de usuario considerando: {', '.join(specific_elements)}
                                Contexto adicional: {context}
                                Enfócate en flujos de usuario, interacciones y accesibilidad.
                                
                                Por favor, formatea tu respuesta con encabezados claros y viñetas.
                                Enfócate en observaciones concretas y mejoras accionables.
                                """
                                
                                response = ux_agent.run(
                                    message=ux_prompt,
                                    images=all_images
                                )
                                
                                st.subheader("🔄 Análisis UX")
                                st.markdown(response.content)
                    
                    # Análisis de Mercado
                    if "Análisis de Mercado" in analysis_types:
                        with st.spinner("📊 Realizando análisis de mercado..."):
                            market_prompt = f"""
                            Analiza el posicionamiento de mercado y las tendencias basadas en estos diseños.
                            Contexto: {context}
                            Compara con diseños de competidores si se proporcionan.
                            Sugiere oportunidades de mercado y posicionamiento.
                            
                            Por favor, formatea tu respuesta con encabezados claros y viñetas.
                            Enfócate en ideas de mercado concretas y recomendaciones accionables.
                            """
                            
                            response = market_agent.run(
                                message=market_prompt,
                                images=all_images
                            )
                            
                            st.subheader("📊 Análisis de Mercado")
                            st.markdown(response.content)
                    
                    # Ideas Combinadas
                    if len(analysis_types) > 1:
                        st.subheader("🎯 Conclusiones Clave")
                        st.info("""
                        Arriba encontrarás un análisis detallado de múltiples agentes de IA especializados, cada uno enfocado en su área de especialización:
                        - Agente de Diseño Visual: Analiza elementos y patrones de diseño
                        - Agente UX: Evalúa la experiencia de usuario e interacciones
                        - Agente de Investigación de Mercado: Proporciona contexto de mercado y oportunidades
                        """)
                
                except Exception as e:
                    st.error(f"Ocurrió un error durante el análisis: {str(e)}")
                    st.error("Por favor, verifica tu clave API e inténtalo de nuevo.")
            else:
                st.warning("Por favor, sube al menos una imagen para analizar.")
    else:
        st.info("👈 Por favor, ingresa tu clave API en la barra lateral para comenzar")
else:
    st.info("👈 Por favor, ingresa tu clave API en la barra lateral para comenzar")

# Pie de página con consejos para obtener mejores resultados
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <h4>Consejos para Obtener Mejores Resultados</h4>
    <p>
    • Sube imágenes claras y de alta resolución<br>
    • Incluye múltiples vistas/pantallas para mejor contexto<br>
    • Sube diseños de competidores para análisis comparativo<br>
    • Proporciona contexto específico sobre tu audiencia objetivo
    </p>
</div>
""", unsafe_allow_html=True) 