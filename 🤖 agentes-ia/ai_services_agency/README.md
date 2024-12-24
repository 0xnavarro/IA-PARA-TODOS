# Agencia de Servicios IA 👨‍💼

Una aplicación de IA que simula una agencia digital de servicio completo utilizando múltiples agentes de IA para analizar y planificar proyectos de software. Cada agente representa un rol diferente en el ciclo de vida del proyecto, desde la planificación estratégica hasta la implementación técnica.

## Demo: 

https://github.com/user-attachments/assets/a0befa3a-f4c3-400d-9790-4b9e37254405

## Características

### Cinco agentes IA especializados 

- **Agente CEO**: Líder estratégico y tomador final de decisiones
  - Analiza ideas de startups usando evaluación estructurada
  - Toma decisiones estratégicas en dominios de producto, técnicos, marketing y financieros
  - Utiliza herramientas AnalyzeStartupTool y MakeStrategicDecision

- **Agente CTO**: Experto en arquitectura técnica y viabilidad
  - Evalúa requisitos técnicos y viabilidad
  - Proporciona decisiones de arquitectura
  - Utiliza herramientas QueryTechnicalRequirements y EvaluateTechnicalFeasibility

- **Agente Product Manager**: Especialista en estrategia de producto
  - Define la estrategia y hoja de ruta del producto
  - Coordina entre equipos técnicos y de marketing
  - Se enfoca en el ajuste producto-mercado

- **Agente Desarrollador**: Experto en implementación técnica
  - Proporciona guía detallada de implementación técnica
  - Sugiere stack tecnológico óptimo y soluciones en la nube
  - Estima costos y tiempos de desarrollo

- **Agente de Éxito del Cliente**: Líder de estrategia de marketing
  - Desarrolla estrategias de entrada al mercado
  - Planifica enfoques de adquisición de clientes
  - Coordina con el equipo de producto

### Herramientas Personalizadas

La agencia utiliza herramientas especializadas construidas con OpenAI Schema para análisis estructurado:
- **Herramientas de Análisis**: AnalyzeProjectRequirements para evaluación de mercado y análisis de idea de startup
- **Herramientas Técnicas**: CreateTechnicalSpecification para evaluación técnica

### 🔄 Comunicación Asíncrona

La agencia opera en modo asíncrono, permitiendo:
- Procesamiento paralelo de análisis de diferentes agentes
- Colaboración eficiente multi-agente
- Comunicación en tiempo real entre agentes
- Operaciones no bloqueantes para mejor rendimiento

### 🔗 Flujos de Comunicación entre Agentes
- CEO ↔️ Todos los Agentes (Supervisión Estratégica)
- CTO ↔️ Desarrollador (Implementación Técnica)
- Product Manager ↔️ Marketing Manager (Estrategia de Entrada al Mercado)
- Product Manager ↔️ Desarrollador (Implementación de Características)
- (¡y más!)

## Cómo Ejecutar

Sigue los pasos a continuación para configurar y ejecutar la aplicación:
Antes que nada, por favor obtén tu Clave API de OpenAI aquí: https://platform.openai.com/api-keys

1. **Clonar el Repositorio**:
   ```bash
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
   cd ai_agent_tutorials
   ```

2. **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Ejecutar la aplicación Streamlit**:
    ```bash
    streamlit run ai_services_agency/agency.py
    ```

4. **Ingresa tu Clave API de OpenAI** en la barra lateral cuando se te solicite y ¡comienza a analizar tu idea de startup!
