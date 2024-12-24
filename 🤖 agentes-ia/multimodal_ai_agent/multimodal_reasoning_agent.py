import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
import tempfile
import os

def main():
    # Configurar el agente de razonamiento
    agent = Agent(
        model=Gemini(id="gemini-2.0-flash-thinking-exp-1219"), 
        markdown=True
    )

    # Título de la aplicación Streamlit
    st.title("Agente IA de Razonamiento Multimodal 🧠")

    # Instrucción
    st.write(
        "Sube una imagen y proporciona una tarea basada en razonamiento para el Agente IA. "
        "El Agente IA analizará la imagen y responderá según tu entrada."
    )

    # Cargador de archivos para imagen
    uploaded_file = st.file_uploader("Sube Imagen", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Guardar archivo subido en archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_path = tmp_file.name

            # Mostrar la imagen subida
            st.image(uploaded_file, caption="Imagen Subida", use_container_width=True)

            # Entrada para tarea dinámica
            task_input = st.text_area(
                "Ingresa tu tarea/pregunta para el Agente IA:"
            )

            # Botón para procesar la imagen y la tarea
            if st.button("Analizar Imagen") and task_input:
                with st.spinner("La IA está pensando... 🤖"):
                    try:
                        # Llamar al agente con la tarea dinámica y la ruta de la imagen
                        response = agent.run(task_input, images=[temp_path])
                        
                        # Mostrar la respuesta del modelo
                        st.markdown("### Respuesta de la IA:")
                        st.markdown(response.content)
                    except Exception as e:
                        st.error(f"Ocurrió un error durante el análisis: {str(e)}")
                    finally:
                        # Limpiar archivo temporal
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)

        except Exception as e:
            st.error(f"Ocurrió un error al procesar la imagen: {str(e)}")

if __name__ == "__main__":
    main()