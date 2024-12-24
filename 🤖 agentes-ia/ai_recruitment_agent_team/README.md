# Equipo de Agentes de Reclutamiento IA

Un sistema de reclutamiento agéntico construido sobre phidata y Streamlit que automatiza el proceso de contratación técnica, facilitando la vida de los reclutadores. El equipo de agentes consta de múltiples agentes especializados que trabajan juntos para manejar el análisis de currículums, la programación de entrevistas con Zoom y las comunicaciones con los candidatos.

## Demostración

## Características

- **Análisis Automatizado de Currículums**
  - Coincidencia de habilidades basada en los requisitos del rol - [Ingeniero de IA/ML, Ingeniero Frontend, Ingeniero Backend]
  - Evaluación de Experiencia - Si el currículum cumple con el 70% de los requisitos, el candidato es seleccionado para la siguiente ronda

- **Comunicaciones Automatizadas**
  - Correo de aceptación y correo de entrevista técnica
  - Retroalimentación de rechazo
  - Programación de entrevistas con Zoom

- **Programación Inteligente**
  - Configuración automatizada de reuniones de Zoom
  - Gestión de zonas horarias
  - Integración de calendario
  - Sistema de recordatorios

## Cosas Importantes a Hacer Antes de Ejecutar la Aplicación

- Crear/Usar una nueva cuenta de Gmail para el reclutador
- Habilitar la Verificación en Dos Pasos y generar una Contraseña de Aplicación para la cuenta de Gmail
- La Contraseña de Aplicación es un código de 16 dígitos (usar sin espacios) que debe generarse aquí - [Contraseña de Aplicación de Google](https://support.google.com/accounts/answer/185833?hl=es) Por favor, sigue los pasos para generar la contraseña - será del formato - 'afec wejf awoj fwrv' (elimina los espacios e ingrésalo en la aplicación Streamlit)
- Crear/Usar una cuenta de Zoom e ir al Mercado de Aplicaciones de Zoom para obtener las credenciales de la API:
[Mercado de Zoom](https://marketplace.zoom.us)
- Ir al Panel de Desarrolladores y crear una nueva aplicación - Seleccionar OAuth de Servidor a Servidor y obtener las credenciales. Verás 3 credenciales - ID de Cliente, Secreto de Cliente y ID de Cuenta
- Después de eso, necesitas agregar algunos alcances a la aplicación - para que el enlace de Zoom del candidato sea enviado y creado a través del correo.
- Los Alcances son meeting:write:invite_links:admin, meeting:write:meeting:admin, meeting:write:meeting:master, meeting:write:invite_links:master, meeting:write:open_app:admin, user:read:email:admin, user:read:list_users:admin, billing:read:user_entitlement:admin, dashboard:read:list_meeting_participants:admin [los últimos 3 son opcionales]

## Cómo Ejecutar

1. **Configurar el Entorno**
   ```bash
   # Clonar el repositorio
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd ai_agent_tutorials/ai_recruitment_agent_team

   # Instalar dependencias
pip install -r requirements.txt
```

2. **Configurar Claves API**
   - Clave API de OpenAI para acceso a GPT-4o
   - Credenciales de API de Zoom (ID de Cuenta, ID de Cliente, Secreto de Cliente)
   - Contraseña de Aplicación del Correo del Reclutador

3. **Ejecutar la Aplicación**
   ```bash
   streamlit run ai_recruitment_agent_team.py
   ```

## Componentes del Sistema

- **Agente Analizador de Currículums**
  - Algoritmo de coincidencia de habilidades
  - Verificación de experiencia
  - Evaluación técnica
  - Toma de decisiones de selección

- **Agente de Comunicación por Correo**
  - Redacción profesional de correos
  - Notificaciones automatizadas
  - Comunicación de retroalimentación
  - Gestión de seguimiento

- **Agente Programador de Entrevistas**
  - Coordinación de reuniones de Zoom
  - Gestión de calendarios
  - Manejo de zonas horarias
  - Sistema de recordatorios

- **Experiencia del Candidato**
  - Interfaz de carga simple
  - Retroalimentación en tiempo real
  - Comunicación clara
  - Proceso simplificado

## Stack Técnico

- **Framework**: Phidata
- **Modelo**: OpenAI GPT-4o
- **Integración**: API de Zoom, Herramienta de Correo de Phidata
- **Procesamiento de PDF**: PyPDF2
- **Gestión del Tiempo**: pytz
- **Gestión de Estado**: Estado de Sesión de Streamlit


## Descargo de Responsabilidad

Esta herramienta está diseñada para asistir en el proceso de reclutamiento, pero no debe reemplazar completamente el juicio humano en las decisiones de contratación. Todas las decisiones automatizadas deben ser revisadas por reclutadores humanos para su aprobación final.

## Mejoras Futuras

- Integración con sistemas ATS
- Puntuación avanzada de candidatos
- Capacidades de entrevistas en video
- Integración de evaluación de habilidades
- Soporte multilingüe
