import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini

st.set_page_config(
    page_title="Planificador de Salud y Fitness IA",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0fff4;
        border: 1px solid #9ae6b4;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fffaf0;
        border: 1px solid #fbd38d;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

def display_dietary_plan(plan_content):
    with st.expander("📋 Tu Plan Dietético Personalizado", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Por qué este plan funciona")
            st.info(plan_content.get("why_this_plan_works", "Información no disponible"))
            st.markdown("### 🍽️ Plan de Comidas")
            st.write(plan_content.get("meal_plan", "Plan no disponible"))
        
        with col2:
            st.markdown("### ⚠️ Consideraciones Importantes")
            considerations = plan_content.get("important_considerations", "").split('\n')
            for consideration in considerations:
                if consideration.strip():
                    st.warning(consideration)

def display_fitness_plan(plan_content):
    with st.expander("💪 Tu Plan de Fitness Personalizado", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Objetivos")
            st.success(plan_content.get("goals", "Objetivos no especificados"))
            st.markdown("### 🏋️‍♂️ Rutina de Ejercicios")
            st.write(plan_content.get("routine", "Rutina no disponible"))
        
        with col2:
            st.markdown("### 💡 Consejos Pro")
            tips = plan_content.get("tips", "").split('\n')
            for tip in tips:
                if tip.strip():
                    st.info(tip)

def main():
    if 'dietary_plan' not in st.session_state:
        st.session_state.dietary_plan = {}
        st.session_state.fitness_plan = {}
        st.session_state.qa_pairs = []
        st.session_state.plans_generated = False

    st.title("🏋️‍♂️ Planificador de Salud y Fitness IA")
    st.markdown("""
        <div style='background-color: #00008B; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem;'>
        Obtén planes dietéticos y de fitness personalizados adaptados a tus objetivos y preferencias.
        Nuestro sistema impulsado por IA considera tu perfil único para crear el plan perfecto para ti.
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.header("🔑 Configuración de API")
        gemini_api_key = st.text_input(
            "Clave API de Gemini",
            type="password",
            help="Ingresa tu clave API de Gemini para acceder al servicio"
        )
        
        if not gemini_api_key:
            st.warning("⚠️ Por favor, ingresa tu Clave API de Gemini para continuar")
            st.markdown("[Obtén tu clave API aquí](https://aistudio.google.com/apikey)")
            return
        
        st.success("¡Clave API aceptada!")

    if gemini_api_key:
        try:
            gemini_model = Gemini(id="gemini-1.5-flash", api_key=gemini_api_key)
        except Exception as e:
            st.error(f"❌ Error al inicializar el modelo Gemini: {e}")
            return

        st.header("👤 Tu Perfil")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Edad", min_value=10, max_value=100, step=1, help="Ingresa tu edad")
            height = st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, step=0.1)
            activity_level = st.selectbox(
                "Nivel de Actividad",
                options=["Sedentario", "Ligeramente Activo", "Moderadamente Activo", "Muy Activo", "Extremadamente Activo"],
                help="Elige tu nivel típico de actividad"
            )
            dietary_preferences = st.selectbox(
                "Preferencias Dietéticas",
                options=["Vegetariano", "Keto", "Sin Gluten", "Bajo en Carbohidratos", "Sin Lácteos"],
                help="Selecciona tu preferencia dietética"
            )

        with col2:
            weight = st.number_input("Peso (kg)", min_value=20.0, max_value=300.0, step=0.1)
            sex = st.selectbox("Sexo", options=["Masculino", "Femenino", "Otro"])
            fitness_goals = st.selectbox(
                "Objetivos de Fitness",
                options=["Perder Peso", "Ganar Músculo", "Resistencia", "Mantenerse en Forma", "Entrenamiento de Fuerza"],
                help="¿Qué quieres lograr?"
            )

        if st.button("🎯 Generar Mi Plan Personalizado", use_container_width=True):
            with st.spinner("Creando tu rutina perfecta de salud y fitness..."):
                try:
                    dietary_agent = Agent(
                        name="Experto en Dieta",
                        role="Proporciona recomendaciones dietéticas personalizadas",
                        model=gemini_model,
                        instructions=[
                            "Considera la entrada del usuario, incluyendo restricciones y preferencias dietéticas.",
                            "Sugiere un plan detallado de comidas para el día, incluyendo desayuno, almuerzo, cena y snacks.",
                            "Proporciona una breve explicación de por qué el plan se adapta a los objetivos del usuario.",
                            "Enfócate en la claridad, coherencia y calidad de las recomendaciones.",
                        ]
                    )

                    fitness_agent = Agent(
                        name="Experto en Fitness",
                        role="Proporciona recomendaciones de fitness personalizadas",
                        model=gemini_model,
                        instructions=[
                            "Proporciona ejercicios adaptados a los objetivos del usuario.",
                            "Incluye ejercicios de calentamiento, entrenamiento principal y enfriamiento.",
                            "Explica los beneficios de cada ejercicio recomendado.",
                            "Asegúrate de que el plan sea accionable y detallado.",
                        ]
                    )

                    user_profile = f"""
                    Edad: {age}
                    Peso: {weight}kg
                    Altura: {height}cm
                    Sexo: {sex}
                    Nivel de Actividad: {activity_level}
                    Preferencias Dietéticas: {dietary_preferences}
                    Objetivos de Fitness: {fitness_goals}
                    """

                    dietary_plan_response = dietary_agent.run(user_profile)
                    dietary_plan = {
                        "why_this_plan_works": "Alta en Proteínas, Grasas Saludables, Carbohidratos Moderados y Balance Calórico",
                        "meal_plan": dietary_plan_response.content,
                        "important_considerations": """
                        - Hidratación: Bebe abundante agua durante el día
                        - Electrolitos: Monitorea los niveles de sodio, potasio y magnesio
                        - Fibra: Asegura una ingesta adecuada a través de vegetales y frutas
                        - Escucha a tu cuerpo: Ajusta los tamaños de las porciones según sea necesario
                        """
                    }

                    fitness_plan_response = fitness_agent.run(user_profile)
                    fitness_plan = {
                        "goals": "Construir fuerza, mejorar resistencia y mantener la forma física general",
                        "routine": fitness_plan_response.content,
                        "tips": """
                        - Registra tu progreso regularmente
                        - Permite un descanso adecuado entre entrenamientos
                        - Concéntrate en la forma correcta
                        - Mantén la consistencia en tu rutina
                        """
                    }

                    st.session_state.dietary_plan = dietary_plan
                    st.session_state.fitness_plan = fitness_plan
                    st.session_state.plans_generated = True
                    st.session_state.qa_pairs = []

                    display_dietary_plan(dietary_plan)
                    display_fitness_plan(fitness_plan)

                except Exception as e:
                    st.error(f"❌ Ocurrió un error: {e}")

        if st.session_state.plans_generated:
            st.header("❓ ¿Preguntas sobre tu plan?")
            question_input = st.text_input("¿Qué te gustaría saber?")

            if st.button("Obtener Respuesta"):
                if question_input:
                    with st.spinner("Encontrando la mejor respuesta para ti..."):
                        dietary_plan = st.session_state.dietary_plan
                        fitness_plan = st.session_state.fitness_plan

                        context = f"Plan Dietético: {dietary_plan.get('meal_plan', '')}\n\nPlan de Fitness: {fitness_plan.get('routine', '')}"
                        full_context = f"{context}\nPregunta del Usuario: {question_input}"

                        try:
                            agent = Agent(model=gemini_model, show_tool_calls=True, markdown=True)
                            run_response = agent.run(full_context)

                            if hasattr(run_response, 'content'):
                                answer = run_response.content
                            else:
                                answer = "Lo siento, no pude generar una respuesta en este momento."

                            st.session_state.qa_pairs.append((question_input, answer))
                        except Exception as e:
                            st.error(f"❌ Ocurrió un error al obtener la respuesta: {e}")

            if st.session_state.qa_pairs:
                st.header("💬 Historial de Preguntas y Respuestas")
                for question, answer in st.session_state.qa_pairs:
                    st.markdown(f"**P:** {question}")
                    st.markdown(f"**R:** {answer}")

if __name__ == "__main__":
    main()