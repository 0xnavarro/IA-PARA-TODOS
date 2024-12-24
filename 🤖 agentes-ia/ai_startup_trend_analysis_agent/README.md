## 📈 Agente de Análisis de Tendencias de Startups IA 
El Agente de Análisis de Tendencias de Startups IA es una herramienta para emprendedores emergentes que genera información procesable identificando tendencias nacientes, posibles brechas de mercado y oportunidades de crecimiento en sectores específicos. Los emprendedores pueden usar estos insights basados en datos para validar ideas, detectar oportunidades de mercado y tomar decisiones informadas sobre sus emprendimientos. Combina Newspaper4k y DuckDuckGo para escanear y analizar artículos enfocados en startups y datos de mercado. Usando Claude 3.5 Sonnet, procesa esta información para extraer patrones emergentes y permitir a los emprendedores identificar oportunidades prometedoras para startups.

### Características
- **Entrada del Usuario**: Los emprendedores pueden ingresar sectores específicos de startups o tecnologías de interés para investigar.
- **Recopilación de Noticias**: Este agente recopila noticias recientes de startups, rondas de financiación y análisis de mercado usando DuckDuckGo.
- **Generación de Resúmenes**: Se generan resúmenes concisos de información verificada usando Newspaper4k.
- **Análisis de Tendencias**: El sistema identifica patrones emergentes en financiamiento de startups, adopción de tecnología y oportunidades de mercado a través de las historias analizadas.
- **Interfaz Streamlit**: La aplicación cuenta con una interfaz amigable construida con Streamlit para una fácil interacción.

### Cómo Comenzar
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git 
   cd ai_agent_tutorials/ai_business_insider_agent
   ```

2. **Crear y activar un entorno virtual**:
   ```bash
   # Para macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # Para Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instalar los paquetes requeridos**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**:
   ```bash
   streamlit run startup_trends_agent.py
   ```
### Nota Importante
- El sistema utiliza específicamente la API de Claude para el procesamiento avanzado del lenguaje. Puedes obtener tu clave API de Anthropic desde [el sitio web de Anthropic](https://www.anthropic.com/api).


