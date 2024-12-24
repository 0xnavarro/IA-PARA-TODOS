from typing import Literal, Tuple, Dict, Optional
import os
import time
import json
import requests
import PyPDF2
from datetime import datetime, timedelta
import pytz

import streamlit as st
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.email import EmailTools
from phi.tools.zoom import ZoomTool
from phi.utils.log import logger
from streamlit_pdf_viewer import pdf_viewer



class CustomZoomTool(ZoomTool):
    def __init__(self, *, account_id: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None, name: str = "zoom_tool"):
        super().__init__(account_id=account_id, client_id=client_id, client_secret=client_secret, name=name)
        self.token_url = "https://zoom.us/oauth/token"
        self.access_token = None
        self.token_expires_at = 0

    def get_access_token(self) -> str:
        if self.access_token and time.time() < self.token_expires_at:
            return str(self.access_token)
            
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "account_credentials", "account_id": self.account_id}

        try:
            response = requests.post(self.token_url, headers=headers, data=data, auth=(self.client_id, self.client_secret))
            response.raise_for_status()

            token_info = response.json()
            self.access_token = token_info["access_token"]
            expires_in = token_info["expires_in"]
            self.token_expires_at = time.time() + expires_in - 60

            self._set_parent_token(str(self.access_token))
            return str(self.access_token)

        except requests.RequestException as e:
            logger.error(f"Error fetching access token: {e}")
            return ""

    def _set_parent_token(self, token: str) -> None:
        """Helper method to set the token in the parent ZoomTool class"""
        if token:
            self._ZoomTool__access_token = token


# Role requirements as a constant dictionary
ROLE_REQUIREMENTS: Dict[str, str] = {
    "ai_ml_engineer": """
        Required Skills:
        - Python, PyTorch/TensorFlow
        - Machine Learning algorithms and frameworks
        - Deep Learning and Neural Networks
        - Data preprocessing and analysis
        - MLOps and model deployment
        - RAG, LLM, Finetuning and Prompt Engineering
    """,

    "frontend_engineer": """
        Required Skills:
        - React/Vue.js/Angular
        - HTML5, CSS3, JavaScript/TypeScript
        - Responsive design
        - State management
        - Frontend testing
    """,

    "backend_engineer": """
        Required Skills:
        - Python/Java/Node.js
        - REST APIs
        - Database design and management
        - System architecture
        - Cloud services (AWS/GCP/Azure)
        - Kubernetes, Docker, CI/CD
    """
}


def init_session_state() -> None:
    """Initialize only necessary session state variables."""
    defaults = {
        'candidate_email': "", 'openai_api_key': "", 'resume_text': "", 'analysis_complete': False,
        'is_selected': False, 'zoom_account_id': "", 'zoom_client_id': "", 'zoom_client_secret': "",
        'email_sender': "", 'email_passkey': "", 'company_name': "", 'current_pdf': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def create_resume_analyzer() -> Agent:
    """Creates and returns a resume analysis agent."""
    if not st.session_state.openai_api_key:
        st.error("Please enter your OpenAI API key first.")
        return None

    return Agent(
        model=OpenAIChat(
            id="gpt-4o",
            api_key=st.session_state.openai_api_key
        ),
        description="You are an expert technical recruiter who analyzes resumes.",
        instructions=[
            "Analyze the resume against the provided job requirements",
            "Be lenient with AI/ML candidates who show strong potential",
            "Consider project experience as valid experience",
            "Value hands-on experience with key technologies",
            "Return a JSON response with selection decision and feedback"
        ],
        markdown=True
    )

def create_email_agent() -> Agent:
    return Agent(
        model=OpenAIChat(
            id="gpt-4o",
            api_key=st.session_state.openai_api_key
        ),
        tools=[EmailTools(
            receiver_email=st.session_state.candidate_email,
            sender_email=st.session_state.email_sender,
            sender_name=st.session_state.company_name,
            sender_passkey=st.session_state.email_passkey
        )],
        description="Eres un coordinador de reclutamiento profesional que maneja las comunicaciones por correo electrónico.",
        instructions=[
            "Redacta y envía correos electrónicos de reclutamiento profesionales.",
            "Actúa como un humano escribiendo un correo electrónico y usa todas las letras en minúsculas.",
            "Mantén un tono amigable pero profesional.",
            "Siempre termina los correos electrónicos con exactamente: 'saludos, el equipo de reclutamiento de ia'.",
            "Nunca incluyas el nombre del remitente o del receptor en la firma.",
            f"El nombre de la empresa es '{st.session_state.company_name}'."
        ],
        markdown=True,
        show_tool_calls=True
    )


def create_scheduler_agent() -> Agent:
    zoom_tools = CustomZoomTool(
        account_id=st.session_state.zoom_account_id,
        client_id=st.session_state.zoom_client_id,
        client_secret=st.session_state.zoom_client_secret
    )

    return Agent(
        name="Interview Scheduler",
        model=OpenAIChat(
            id="gpt-4o",
            api_key=st.session_state.openai_api_key
        ),
        tools=[zoom_tools],
        description="You are an interview scheduling coordinator.",
        instructions=[
            "You are an expert at scheduling technical interviews using Zoom.",
            "Schedule interviews during business hours (9 AM - 5 PM EST)",
            "Create meetings with proper titles and descriptions",
            "Ensure all meeting details are included in responses",
            "Use ISO 8601 format for dates",
            "Handle scheduling errors gracefully"
        ],
        markdown=True,
        show_tool_calls=True
    )


def extract_text_from_pdf(pdf_file) -> str:
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting PDF text: {str(e)}")
        return ""


def analyze_resume(
    resume_text: str,
    role: Literal["ai_ml_engineer", "frontend_engineer", "backend_engineer"],
    analyzer: Agent
) -> Tuple[bool, str]:
    try:
        response = analyzer.run(
            f"""Please analyze this resume against the following requirements and provide your response in valid JSON format:
            Role Requirements:
            {ROLE_REQUIREMENTS[role]}
            Resume Text:
            {resume_text}
            Your response must be a valid JSON object like this:
            {{
                "selected": true/false,
                "feedback": "Detailed feedback explaining the decision",
                "matching_skills": ["skill1", "skill2"],
                "missing_skills": ["skill3", "skill4"],
                "experience_level": "junior/mid/senior"
            }}
            Evaluation criteria:
            1. Match at least 70% of required skills
            2. Consider both theoretical knowledge and practical experience
            3. Value project experience and real-world applications
            4. Consider transferable skills from similar technologies
            5. Look for evidence of continuous learning and adaptability
            Important: Return ONLY the JSON object without any markdown formatting or backticks.
            """
        )

        assistant_message = next((msg.content for msg in response.messages if msg.role == 'assistant'), None)
        if not assistant_message:
            raise ValueError("No assistant message found in response.")

        result = json.loads(assistant_message.strip())
        if not isinstance(result, dict) or not all(k in result for k in ["selected", "feedback"]):
            raise ValueError("Invalid response format")

        return result["selected"], result["feedback"]

    except (json.JSONDecodeError, ValueError) as e:
        st.error(f"Error processing response: {str(e)}")
        return False, f"Error analyzing resume: {str(e)}"


def send_selection_email(email_agent: Agent, to_email: str, role: str) -> None:
    email_agent.run(
        f"""
        Send an email to {to_email} regarding their selection for the {role} position.
        The email should:
        1. Congratulate them on being selected
        2. Explain the next steps in the process
        3. Mention that they will receive interview details shortly
        4. The name of the company is 'AI Recruiting Team'
        """
    )


def send_rejection_email(email_agent: Agent, to_email: str, role: str, feedback: str) -> None:
    """
    Envía un correo de rechazo con retroalimentación constructiva.
    """
    email_agent.run(
        f"""
        Envía un correo electrónico a {to_email} sobre su aplicación para el puesto de {role}.
        Usa este estilo específico:
        1. usa todas las letras en minúsculas
        2. sé empático y humano
        3. menciona retroalimentación específica de: {feedback}
        4. anímalos a mejorar sus habilidades y volver a intentarlo
        5. sugiere algunos recursos de aprendizaje basados en las habilidades faltantes
        6. termina el correo electrónico con exactamente:
           saludos,
           el equipo de reclutamiento de ia
        
        No incluyas ningún nombre en la firma.
        El tono debe ser como el de un humano escribiendo un correo rápido pero reflexivo.
        """
    )


def schedule_interview(scheduler: Agent, candidate_email: str, email_agent: Agent, role: str) -> None:
    """
    Programa entrevistas durante el horario laboral (9 AM - 5 PM IST).
    """
    try:
        # Obtener la hora actual en IST
        ist_tz = pytz.timezone('Asia/Kolkata')
        current_time_ist = datetime.now(ist_tz)

        tomorrow_ist = current_time_ist + timedelta(days=1)
        interview_time = tomorrow_ist.replace(hour=11, minute=0, second=0, microsecond=0)
        formatted_time = interview_time.strftime('%Y-%m-%dT%H:%M:%S')

        meeting_response = scheduler.run(
            f"""Programa una entrevista técnica de 60 minutos con estas especificaciones:
            - Título: 'Entrevista Técnica para {role}'
            - Fecha: {formatted_time}
            - Zona horaria: IST (Hora Estándar de India)
            - Asistente: {candidate_email}
            
            Notas Importantes:
            - La reunión debe ser entre 9 AM - 5 PM IST
            - Usa la zona horaria IST (UTC+5:30) para todas las comunicaciones
            - Incluye información de la zona horaria en los detalles de la reunión
            """
        )

        email_agent.run(
            f"""Envía un correo de confirmación de entrevista con estos detalles:
            - Rol: puesto de {role}
            - Detalles de la reunión: {meeting_response}
            
            Importante:
            - Especifica claramente que la hora es en IST (Hora Estándar de India)
            - Pide al candidato que se una 5 minutos antes
            - Incluye un enlace de conversión de zona horaria si es posible
            - Anímalo a estar seguro y no tan nervioso y a prepararse bien para la entrevista
            """
        )
        
        st.success("¡Entrevista programada con éxito! Revisa tu correo para más detalles.")
        
    except Exception as e:
        logger.error(f"Error al programar la entrevista: {str(e)}")
        st.error("No se pudo programar la entrevista. Por favor, inténtalo de nuevo.")


def main() -> None:
    st.title("Sistema de Reclutamiento IA")

    init_session_state()
    with st.sidebar:
        st.header("Configuración")
        
        # Configuración de OpenAI
        st.subheader("Configuración de OpenAI")
        api_key = st.text_input("Clave API de OpenAI", type="password", value=st.session_state.openai_api_key, help="Obtén tu clave API desde platform.openai.com")
        if api_key: st.session_state.openai_api_key = api_key

        st.subheader("Configuración de Zoom")
        zoom_account_id = st.text_input("ID de Cuenta de Zoom", type="password", value=st.session_state.zoom_account_id)
        zoom_client_id = st.text_input("ID de Cliente de Zoom", type="password", value=st.session_state.zoom_client_id)
        zoom_client_secret = st.text_input("Secreto de Cliente de Zoom", type="password", value=st.session_state.zoom_client_secret)
        
        st.subheader("Configuración de Correo")
        email_sender = st.text_input("Correo del Remitente", value=st.session_state.email_sender, help="Dirección de correo desde la cual enviar")
        email_passkey = st.text_input("Contraseña de Aplicación de Correo", type="password", value=st.session_state.email_passkey, help="Contraseña específica de la aplicación para el correo")
        company_name = st.text_input("Nombre de la Empresa", value=st.session_state.company_name, help="Nombre a usar en las comunicaciones por correo")

        if zoom_account_id: st.session_state.zoom_account_id = zoom_account_id
        if zoom_client_id: st.session_state.zoom_client_id = zoom_client_id
        if zoom_client_secret: st.session_state.zoom_client_secret = zoom_client_secret
        if email_sender: st.session_state.email_sender = email_sender
        if email_passkey: st.session_state.email_passkey = email_passkey
        if company_name: st.session_state.company_name = company_name

        required_configs = {'Clave API de OpenAI': st.session_state.openai_api_key, 'ID de Cuenta de Zoom': st.session_state.zoom_account_id,
                          'ID de Cliente de Zoom': st.session_state.zoom_client_id, 'Secreto de Cliente de Zoom': st.session_state.zoom_client_secret,
                          'Correo del Remitente': st.session_state.email_sender, 'Contraseña de Correo': st.session_state.email_passkey,
                          'Nombre de la Empresa': st.session_state.company_name}

    missing_configs = [k for k, v in required_configs.items() if not v]
    if missing_configs:
        st.warning(f"Por favor, configura lo siguiente en la barra lateral: {', '.join(missing_configs)}")
        return

    if not st.session_state.openai_api_key:
        st.warning("Por favor, ingresa tu clave API de OpenAI en la barra lateral para continuar.")
        return

    role = st.selectbox("Selecciona el rol para el que estás aplicando:", ["ai_ml_engineer", "frontend_engineer", "backend_engineer"])
    with st.expander("Ver Habilidades Requeridas", expanded=True): st.markdown(ROLE_REQUIREMENTS[role])

    # Agregar un botón de "Nueva Aplicación" antes de la carga del currículum
    if st.button("📝 Nueva Aplicación"):
        # Limpiar solo los estados relacionados con la aplicación
        keys_to_clear = ['resume_text', 'analysis_complete', 'is_selected', 'candidate_email', 'current_pdf']
        for key in keys_to_clear:
            if key in st.session_state:
                st.session_state[key] = None if key == 'current_pdf' else ""
        st.rerun()

    resume_file = st.file_uploader("Sube tu currículum (PDF)", type=["pdf"], key="resume_uploader")
    if resume_file is not None and resume_file != st.session_state.get('current_pdf'):
        st.session_state.current_pdf = resume_file
        st.session_state.resume_text = ""
        st.session_state.analysis_complete = False
        st.session_state.is_selected = False
        st.rerun()

    if resume_file:
        st.subheader("Currículum Subido")
        col1, col2 = st.columns([4, 1])
        
        with col1:
            import tempfile, os
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(resume_file.read())
                tmp_file_path = tmp_file.name
            resume_file.seek(0)
            try: pdf_viewer(tmp_file_path)
            finally: os.unlink(tmp_file_path)
        
        with col2:
            st.download_button(label="📥 Descargar", data=resume_file, file_name=resume_file.name, mime="application/pdf")
        # Procesar el texto del currículum
        if not st.session_state.resume_text:
            with st.spinner("Procesando tu currículum..."):
                resume_text = extract_text_from_pdf(resume_file)
                if resume_text:
                    st.session_state.resume_text = resume_text
                    st.success("¡Currículum procesado con éxito!")
                else:
                    st.error("No se pudo procesar el PDF. Por favor, inténtalo de nuevo.")

    # Entrada de correo electrónico con estado de sesión
    email = st.text_input(
        "Dirección de correo del candidato",
        value=st.session_state.candidate_email,
        key="email_input"
    )
    st.session_state.candidate_email = email

    # Análisis y próximos pasos
    if st.session_state.resume_text and email and not st.session_state.analysis_complete:
        if st.button("Analizar Currículum"):
            with st.spinner("Analizando tu currículum..."):
                resume_analyzer = create_resume_analyzer()
                email_agent = create_email_agent()  # Crear agente de correo aquí
                
                if resume_analyzer and email_agent:
                    print("DEBUG: Iniciando análisis de currículum")
                    is_selected, feedback = analyze_resume(
                        st.session_state.resume_text,
                        role,
                        resume_analyzer
                    )
                    print(f"DEBUG: Análisis completo - Seleccionado: {is_selected}, Retroalimentación: {feedback}")

                    if is_selected:
                        st.success("¡Felicidades! Tus habilidades coinciden con nuestros requisitos.")
                        st.session_state.analysis_complete = True
                        st.session_state.is_selected = True
                        st.rerun()
                    else:
                        st.warning("Desafortunadamente, tus habilidades no coinciden con nuestros requisitos.")
                        st.write(f"Retroalimentación: {feedback}")
                        
                        # Enviar correo de rechazo
                        with st.spinner("Enviando correo de retroalimentación..."):
                            try:
                                send_rejection_email(
                                    email_agent=email_agent,
                                    to_email=email,
                                    role=role,
                                    feedback=feedback
                                )
                                st.info("Te hemos enviado un correo con retroalimentación detallada.")
                            except Exception as e:
                                logger.error(f"Error al enviar correo de rechazo: {e}")
                                st.error("No se pudo enviar el correo de retroalimentación. Por favor, inténtalo de nuevo.")

    if st.session_state.get('analysis_complete') and st.session_state.get('is_selected', False):
        st.success("¡Felicidades! Tus habilidades coinciden con nuestros requisitos.")
        st.info("Haz clic en 'Continuar con la Aplicación' para continuar con el proceso de entrevista.")
        
        if st.button("Continuar con la Aplicación", key="proceed_button"):
            print("DEBUG: Botón de continuar clicado")  # Debug
            with st.spinner("🔄 Procesando tu aplicación..."):
                try:
                    print("DEBUG: Creando agente de correo")  # Debug
                    email_agent = create_email_agent()
                    print(f"DEBUG: Agente de correo creado: {email_agent}")  # Debug
                    
                    print("DEBUG: Creando agente de programación")  # Debug
                    scheduler_agent = create_scheduler_agent()
                    print(f"DEBUG: Agente de programación creado: {scheduler_agent}")  # Debug

                    # 3. Enviar correo de selección
                    with st.status("📧 Enviando correo de confirmación...", expanded=True) as status:
                        print(f"DEBUG: Intentando enviar correo a {st.session_state.candidate_email}")  # Debug
                        send_selection_email(
                            email_agent,
                            st.session_state.candidate_email,
                            role
                        )
                        print("DEBUG: Correo enviado con éxito")  # Debug
                        status.update(label="✅ ¡Correo de confirmación enviado!")

                    # 4. Programar entrevista
                    with st.status("📅 Programando entrevista...", expanded=True) as status:
                        print("DEBUG: Intentando programar entrevista")  # Debug
                        schedule_interview(
                            scheduler_agent,
                            st.session_state.candidate_email,
                            email_agent,
                            role
                        )
                        print("DEBUG: Entrevista programada con éxito")  # Debug
                        status.update(label="✅ ¡Entrevista programada!")

                    print("DEBUG: Todos los procesos completados con éxito")  # Debug
                    st.success("""
                        🎉 ¡Aplicación Procesada con Éxito!
                        
                        Por favor, revisa tu correo para:
                        1. Confirmación de selección ✅
                        2. Detalles de la entrevista con enlace de Zoom 🔗
                        
                        Próximos pasos:
                        1. Revisa los requisitos del rol
                        2. Prepárate para tu entrevista técnica
                        3. Únete a la entrevista 5 minutos antes
                    """)

                except Exception as e:
                    print(f"DEBUG: Ocurrió un error: {str(e)}")  # Debug
                    print(f"DEBUG: Tipo de error: {type(e)}")  # Debug
                    import traceback
                    print(f"DEBUG: Trazado completo: {traceback.format_exc()}")  # Debug
                    st.error(f"Ocurrió un error: {str(e)}")
                    st.error("Por favor, inténtalo de nuevo o contacta con soporte.")

    # Botón de reinicio
    if st.sidebar.button("Reiniciar Aplicación"):
        for key in st.session_state.keys():
            if key != 'openai_api_key':
                del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()