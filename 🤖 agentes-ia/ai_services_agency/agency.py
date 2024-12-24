from typing import List, Literal, Dict, Optional
from agency_swarm import Agent, Agency, set_openai_key, BaseTool
from pydantic import Field, BaseModel
import streamlit as st

class AnalyzeProjectRequirements(BaseTool):
    project_name: str = Field(..., description="Nombre del proyecto")
    project_description: str = Field(..., description="Descripción y objetivos del proyecto")
    project_type: Literal["Web Application", "Mobile App", "API Development", 
                         "Data Analytics", "AI/ML Solution", "Other"] = Field(..., 
                         description="Tipo de proyecto")
    budget_range: Literal["$10k-$25k", "$25k-$50k", "$50k-$100k", "$100k+"] = Field(..., 
                         description="Rango de presupuesto para el proyecto")

    class ToolConfig:
        name = "analyze_project"
        description = "Analiza los requisitos y viabilidad del proyecto"
        one_call_at_a_time = True

    def run(self) -> str:
        """Analiza el proyecto y almacena resultados en el estado compartido"""
        if self._shared_state.get("project_analysis", None) is not None:
            raise ValueError("El análisis del proyecto ya existe. Por favor, procede con la especificación técnica.")
        
        analysis = {
            "name": self.project_name,
            "type": self.project_type,
            "complexity": "alta",
            "timeline": "6 meses",
            "budget_feasibility": "dentro del rango",
            "requirements": ["Arquitectura escalable", "Seguridad", "Integración API"]
        }
        
        self._shared_state.set("project_analysis", analysis)
        return "Análisis del proyecto completado. Por favor, procede con la especificación técnica."

class CreateTechnicalSpecification(BaseTool):
    architecture_type: Literal["monolithic", "microservices", "serverless", "hybrid"] = Field(
        ..., 
        description="Tipo de arquitectura propuesta"
    )
    core_technologies: str = Field(
        ..., 
        description="Lista de tecnologías y frameworks principales separados por comas"
    )
    scalability_requirements: Literal["high", "medium", "low"] = Field(
        ..., 
        description="Necesidades de escalabilidad"
    )

    class ToolConfig:
        name = "create_technical_spec"
        description = "Crea especificaciones técnicas basadas en el análisis del proyecto"
        one_call_at_a_time = True

    def run(self) -> str:
        """Crea especificación técnica basada en el análisis"""
        project_analysis = self._shared_state.get("project_analysis", None)
        if project_analysis is None:
            raise ValueError("Por favor, analiza primero los requisitos del proyecto usando la herramienta AnalyzeProjectRequirements.")
        
        spec = {
            "project_name": project_analysis["name"],
            "architecture": self.architecture_type,
            "technologies": self.core_technologies.split(","),
            "scalability": self.scalability_requirements
        }
        
        self._shared_state.set("technical_specification", spec)
        return f"Especificación técnica creada para {project_analysis['name']}."

def init_session_state() -> None:
    """Inicializar variables de estado de la sesión"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None

def main() -> None:
    st.set_page_config(page_title="Agencia de Servicios IA", layout="wide")
    init_session_state()
    
    st.title("🚀 Agencia de Servicios IA")
    
    # Configuración de API
    with st.sidebar:
        st.header("🔑 Configuración de API")
        openai_api_key = st.text_input(
            "Clave API de OpenAI",
            type="password",
            help="Ingresa tu clave API de OpenAI para continuar"
        )

        if openai_api_key:
            st.session_state.api_key = openai_api_key
            st.success("¡Clave API aceptada!")
        else:
            st.warning("⚠️ Por favor, ingresa tu Clave API de OpenAI para continuar")
            st.markdown("[Obtén tu clave API aquí](https://platform.openai.com/api-keys)")
            return
        
    # Inicializar agentes con la clave API proporcionada
    set_openai_key(st.session_state.api_key)
    api_headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
    
    # Formulario de Entrada del Proyecto
    with st.form("project_form"):
        st.subheader("Detalles del Proyecto")
        
        project_name = st.text_input("Nombre del Proyecto")
        project_description = st.text_area(
            "Descripción del Proyecto",
            help="Describe el proyecto, sus objetivos y cualquier requisito específico"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            project_type = st.selectbox(
                "Tipo de Proyecto",
                ["Web Application", "Mobile App", "API Development", 
                 "Data Analytics", "AI/ML Solution", "Other"]
            )
            timeline = st.selectbox(
                "Tiempo Estimado",
                ["1-2 meses", "3-4 meses", "5-6 meses", "6+ meses"]
            )
        
        with col2:
            budget_range = st.selectbox(
                "Rango de Presupuesto",
                ["$10k-$25k", "$25k-$50k", "$50k-$100k", "$100k+"]
            )
            priority = st.selectbox(
                "Prioridad del Proyecto",
                ["Alta", "Media", "Baja"]
            )
        
        tech_requirements = st.text_area(
            "Requisitos Técnicos (opcional)",
            help="Cualquier requisito técnico específico o preferencias"
        )
        
        special_considerations = st.text_area(
            "Consideraciones Especiales (opcional)",
            help="Cualquier información adicional o requisitos especiales"
        )
        
        submitted = st.form_submit_button("Analizar Proyecto")
        
        if submitted and project_name and project_description:
            try:
                # Establecer clave OpenAI
                set_openai_key(st.session_state.api_key)
                
                # Crear agentes
                ceo = Agent(
                    name="Director de Proyecto",
                    description="Eres un CEO de múltiples empresas en el pasado y tienes mucha experiencia en evaluar proyectos y tomar decisiones estratégicas.",
                    instructions="""
                    Eres un CEO experimentado que evalúa proyectos. Sigue estos pasos estrictamente:

                    1. PRIMERO, usa la herramienta AnalyzeProjectRequirements con:
                       - project_name: El nombre de los detalles del proyecto
                       - project_description: La descripción completa del proyecto
                       - project_type: El tipo de proyecto (Web Application, Mobile App, etc)
                       - budget_range: El rango de presupuesto especificado

                    2. ESPERA a que el análisis se complete antes de continuar.
                    
                    3. Revisa los resultados del análisis y proporciona recomendaciones estratégicas.
                    """,
                    tools=[AnalyzeProjectRequirements],
                    api_headers=api_headers,
                    temperature=0.7,
                    max_prompt_tokens=25000
                )

                cto = Agent(
                    name="Arquitecto Técnico",
                    description="Arquitecto técnico senior con profunda experiencia en diseño de sistemas.",
                    instructions="""
                    Eres un arquitecto técnico. Sigue estos pasos estrictamente:

                    1. ESPERA a que el análisis del proyecto sea completado por el CEO.
                    
                    2. Usa la herramienta CreateTechnicalSpecification con:
                       - architecture_type: Elige entre monolithic/microservices/serverless/hybrid
                       - core_technologies: Lista las tecnologías principales separadas por comas
                       - scalability_requirements: Elige high/medium/low según las necesidades del proyecto

                    3. Revisa la especificación técnica y proporciona recomendaciones adicionales.
                    """,
                    tools=[CreateTechnicalSpecification],
                    api_headers=api_headers,
                    temperature=0.5,
                    max_prompt_tokens=25000
                )

                product_manager = Agent(
                    name="Gerente de Producto",
                    description="Gerente de producto experimentado enfocado en la excelencia de entrega.",
                    instructions="""
                    - Gestiona el alcance y cronograma del proyecto proporcionando la hoja de ruta
                    - Define los requisitos del producto y debes dar productos y características potenciales que se pueden construir para la startup
                    """,
                    api_headers=api_headers,
                    temperature=0.4,
                    max_prompt_tokens=25000
                )

                developer = Agent(
                    name="Desarrollador Líder",
                    description="Desarrollador senior con experiencia full-stack.",
                    instructions="""
                    - Planifica la implementación técnica
                    - Proporciona estimaciones de esfuerzo
                    - Revisa la viabilidad técnica
                    """,
                    api_headers=api_headers,
                    temperature=0.3,
                    max_prompt_tokens=25000
                )

                client_manager = Agent(
                    name="Gerente de Éxito del Cliente",
                    description="Gerente de clientes experimentado enfocado en la entrega del proyecto.",
                    instructions="""
                    - Asegura la satisfacción del cliente
                    - Gestiona expectativas
                    - Maneja retroalimentación
                    """,
                    api_headers=api_headers,
                    temperature=0.6,
                    max_prompt_tokens=25000
                )

                # Crear agencia
                agency = Agency(
                    [
                        ceo, cto, product_manager, developer, client_manager,
                        [ceo, cto],
                        [ceo, product_manager],
                        [ceo, developer],
                        [ceo, client_manager],
                        [cto, developer],
                        [product_manager, developer],
                        [product_manager, client_manager]
                    ],
                    async_mode='threading',
                    shared_files='shared_files'
                )
                
                # Prepare project info
                project_info = {
                    "name": project_name,
                    "description": project_description,
                    "type": project_type,
                    "timeline": timeline,
                    "budget": budget_range,
                    "priority": priority,
                    "technical_requirements": tech_requirements,
                    "special_considerations": special_considerations
                }

                st.session_state.messages.append({"role": "user", "content": str(project_info)})
                # Create tabs and run analysis
                with st.spinner("AI Services Agency is analyzing your project..."):
                    try:
                        # Get analysis from each agent using agency.get_completion()
                        ceo_response = agency.get_completion(
                            message=f"""Analyze this project using the AnalyzeProjectRequirements tool:
                            Project Name: {project_name}
                            Project Description: {project_description}
                            Project Type: {project_type}
                            Budget Range: {budget_range}
                            
                            Use these exact values with the tool and wait for the analysis results.""",
                            recipient_agent=ceo
                        )
                        
                        cto_response = agency.get_completion(
                            message=f"""Review the project analysis and create technical specifications using the CreateTechnicalSpecification tool.
                            Choose the most appropriate:
                            - architecture_type (monolithic/microservices/serverless/hybrid)
                            - core_technologies (comma-separated list)
                            - scalability_requirements (high/medium/low)
                            
                            Base your choices on the project requirements and analysis.""",
                            recipient_agent=cto
                        )
                        
                        pm_response = agency.get_completion(
                            message=f"Analyze project management aspects: {str(project_info)}",
                            recipient_agent=product_manager,
                            additional_instructions="Focus on product-market fit and roadmap development, and coordinate with technical and marketing teams."
                        )

                        developer_response = agency.get_completion(
                            message=f"Analyze technical implementation based on CTO's specifications: {str(project_info)}",
                            recipient_agent=developer,
                            additional_instructions="Provide technical implementation details, optimal tech stack you would be using including the costs of cloud services (if any) and feasibility feedback, and coordinate with product manager and CTO to build the required products for the startup."
                        )
                        
                        client_response = agency.get_completion(
                            message=f"Analyze client success aspects: {str(project_info)}",
                            recipient_agent=client_manager,
                            additional_instructions="Provide detailed go-to-market strategy and customer acquisition plan, and coordinate with product manager."
                        )
                        
                        # Create tabs for different analyses
                        tabs = st.tabs([
                            "CEO's Project Analysis",
                            "CTO's Technical Specification",
                            "Product Manager's Plan",
                            "Developer's Implementation",
                            "Client Success Strategy"
                        ])
                        
                        with tabs[0]:
                            st.markdown("## CEO's Strategic Analysis")
                            st.markdown(ceo_response)
                            st.session_state.messages.append({"role": "assistant", "content": ceo_response})
                        
                        with tabs[1]:
                            st.markdown("## CTO's Technical Specification")
                            st.markdown(cto_response)
                            st.session_state.messages.append({"role": "assistant", "content": cto_response})
                        
                        with tabs[2]:
                            st.markdown("## Product Manager's Plan")
                            st.markdown(pm_response)
                            st.session_state.messages.append({"role": "assistant", "content": pm_response})
                        
                        with tabs[3]:
                            st.markdown("## Lead Developer's Development Plan")
                            st.markdown(developer_response)
                            st.session_state.messages.append({"role": "assistant", "content": developer_response})
                        
                        with tabs[4]:
                            st.markdown("## Client Success Strategy")
                            st.markdown(client_response)
                            st.session_state.messages.append({"role": "assistant", "content": client_response})

                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
                        st.error("Please check your inputs and API key and try again.")

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.error("Please check your API key and try again.")

    # Add history management in sidebar
    with st.sidebar:
        st.subheader("Options")
        if st.checkbox("Show Analysis History"):
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        if st.button("Clear History"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()