## 🛒 Agente de Atención al Cliente IA con Memoria
Esta aplicación Streamlit implementa un agente de atención al cliente impulsado por IA para datos sintéticos generados usando GPT-4o. El agente utiliza el modelo GPT-4o de OpenAI y mantiene una memoria de interacciones pasadas usando la biblioteca Mem0 con Qdrant como almacén de vectores.

### Características

- Interfaz de chat para interactuar con el agente de atención al cliente IA
- Memoria persistente de interacciones y perfiles de clientes
- Generación de datos sintéticos para pruebas y demostración
- Utiliza el modelo GPT-4o de OpenAI para respuestas inteligentes

### ¿Cómo Empezar?

1. Clona el repositorio de GitHub
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
```

2. Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
```

3. Asegúrate de que Qdrant esté ejecutándose:
La aplicación espera que Qdrant esté ejecutándose en localhost:6333. Ajusta la configuración en el código si tu configuración es diferente.

```bash
docker pull qdrant/qdrant

docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

4. Ejecuta la Aplicación Streamlit
```bash
streamlit run customer_support_agent.py
```
