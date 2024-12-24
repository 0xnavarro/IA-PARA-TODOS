# 👀 Aplicación RAG con Búsqueda Híbrida 

Una potente aplicación de preguntas y respuestas sobre documentos que aprovecha la Búsqueda Híbrida (RAG) y las capacidades avanzadas de lenguaje de Claude para proporcionar respuestas completas. Construida con RAGLite para un procesamiento y recuperación robusta de documentos, y Streamlit para una interfaz de chat intuitiva, este sistema combina perfectamente el conocimiento específico de documentos con la inteligencia general de Claude para entregar respuestas precisas y contextuales.

## Video de demostración:


https://github.com/user-attachments/assets/b576bf6e-4a48-4a43-9600-48bcc8f359a5


## Características

- **Preguntas y Respuestas con Búsqueda Híbrida**
    - Respuestas basadas en RAG para consultas específicas de documentos
    - Respaldo en Claude para preguntas de conocimiento general

- **Procesamiento de Documentos**:
  - Carga y procesamiento de documentos PDF
  - Fragmentación automática de texto y generación de embeddings
  - Búsqueda híbrida combinando coincidencia semántica y por palabras clave
  - Reordenamiento para mejor selección de contexto

- **Integración Multi-Modelo**:
  - Claude para generación de texto - probado con Claude 3 Opus 
  - OpenAI para embeddings - probado con text-embedding-3-large
  - Cohere para reordenamiento - probado con Cohere 3.5 reranker

## Prerrequisitos

Necesitarás las siguientes claves API y configuración de base de datos:

1. **Base de Datos**: Crea una base de datos PostgreSQL gratuita en [Neon](https://neon.tech):
   - Regístrate/Inicia sesión en Neon
   - Crea un nuevo proyecto
   - Copia la cadena de conexión (se ve así: `postgresql://user:pass@ep-xyz.region.aws.neon.tech/dbname`)

2. **Claves API**:
   - [Clave API de OpenAI](https://platform.openai.com/api-keys) para embeddings
   - [Clave API de Anthropic](https://console.anthropic.com/settings/keys) para Claude
   - [Clave API de Cohere](https://dashboard.cohere.com/api-keys) para reordenamiento

## ¿Cómo empezar?

1. **Clonar el Repositorio**:
   ```bash
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
   cd rag_tutorials/hybrid_search_rag
   ```

2. **Instalar Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Instalar Modelo spaCy**:
   ```bash
   pip install https://github.com/explosion/spacy-models/releases/download/xx_sent_ud_sm-3.7.0/xx_sent_ud_sm-3.7.0-py3-none-any.whl
   ```

4. **Ejecutar la Aplicación**:
   ```bash
   streamlit run main.py
   ```

## Uso

1. Inicia la aplicación
2. Ingresa tus claves API en la barra lateral:
   - Clave API de OpenAI
   - Clave API de Anthropic
   - Clave API de Cohere
   - URL de la base de datos (opcional, por defecto usa SQLite)
3. Haz clic en "Guardar Configuración"
4. Sube documentos PDF
5. ¡Comienza a hacer preguntas!
   - Las preguntas específicas sobre documentos usarán RAG
   - Las preguntas generales usarán Claude directamente

## Opciones de Base de Datos

La aplicación soporta múltiples backends de base de datos:

- **PostgreSQL** (Recomendado):
  - Crea una base de datos PostgreSQL serverless gratuita en [Neon](https://neon.tech)
  - Obtén aprovisionamiento instantáneo y capacidad de escalar a cero
  - Formato de cadena de conexión: `postgresql://user:pass@ep-xyz.region.aws.neon.tech/dbname`

- **MySQL**:
  ```
  mysql://user:pass@host:port/db
  ```
- **SQLite** (Desarrollo local):
  ```
  sqlite:///path/to/db.sqlite
  ```

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, siéntete libre de enviar un Pull Request.
