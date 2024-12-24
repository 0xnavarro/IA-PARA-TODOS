## 🤖 AutoRAG: RAG Autónomo con GPT-4o y Base de Datos Vectorial
Esta aplicación Streamlit implementa un sistema de Generación Aumentada por Recuperación (RAG) Autónomo usando el modelo GPT-4o de OpenAI y la base de datos PgVector. Permite a los usuarios subir documentos PDF, agregarlos a una base de conocimientos y consultar al asistente de IA con contexto tanto de la base de conocimientos como de búsquedas web.

### Características 
- Interfaz de chat para interactuar con el asistente de IA
- Carga y procesamiento de documentos PDF
- Integración de base de conocimientos usando PostgreSQL y Pgvector
- Capacidad de búsqueda web usando DuckDuckGo
- Almacenamiento persistente de datos del asistente y conversaciones

### ¿Cómo empezar?

1. Clona el repositorio de GitHub
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
```

2. Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
```

3. Asegúrate de que la Base de Datos PgVector esté ejecutándose:
La aplicación espera que PgVector esté ejecutándose en [localhost:5532](http://localhost:5532/). Ajusta la configuración en el código si tu configuración es diferente.

```bash
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```

4. Ejecuta la Aplicación Streamlit
```bash
streamlit run autorag.py
```
