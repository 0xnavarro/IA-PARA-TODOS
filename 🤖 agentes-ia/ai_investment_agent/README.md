## 📈 Agente de Inversiones IA
Esta aplicación Streamlit es un agente de inversiones impulsado por IA que compara el rendimiento de dos acciones y genera informes detallados. Utilizando GPT-4o con datos de Yahoo Finance, esta aplicación proporciona información valiosa para ayudarte a tomar decisiones de inversión informadas.

### Características
- Compara el rendimiento de dos acciones
- Obtiene información completa de las empresas
- Obtiene las últimas noticias y recomendaciones de analistas
- Proporciona análisis detallado del mercado

### ¿Cómo Empezar?

1. Clona el repositorio de GitHub

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
```
2. Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
```
3. Obtén tu Clave API de OpenAI

- Regístrate para obtener una [cuenta de OpenAI](https://platform.openai.com/) (o el proveedor de LLM de tu elección) y obtén tu clave API.

4. Ejecuta la Aplicación Streamlit
```bash
streamlit run investment_agent.py
```

### ¿Cómo Funciona?

- Al ejecutar la aplicación, se te pedirá que ingreses tu clave API de OpenAI. Esta clave se utiliza para autenticar y acceder al modelo de lenguaje de OpenAI.
- Una vez que proporciones una clave API válida, se crea una instancia de la clase Assistant. Este asistente utiliza el modelo de lenguaje GPT-4 de OpenAI y las herramientas YFinanceTools para acceder a datos bursátiles.
- Ingresa los símbolos bursátiles de las dos empresas que deseas comparar en los campos de texto proporcionados.
- El asistente realizará los siguientes pasos:
    - Recuperar precios de acciones en tiempo real y datos históricos usando YFinanceTools
    - Obtener las últimas noticias de la empresa y recomendaciones de analistas
    - Recopilar información completa de la empresa
    - Generar un informe de comparación detallado utilizando el modelo de lenguaje GPT-4
- El informe generado se mostrará en la aplicación, proporcionándote información valiosa y análisis para guiar tus decisiones de inversión.