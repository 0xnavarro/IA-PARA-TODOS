from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import time

# 1. Inicializar el Agente Multimodal
agent = Agent(model=Gemini(id="gemini-2.0-flash-exp"), tools=[DuckDuckGo()], markdown=True)

# 2. Entrada de Imagen
image_url = "https://example.com/sample_image.jpg"

# 3. Entrada de Audio
audio_file = "sample_audio.mp3"

# 4. Entrada de Video
video_file = upload_file("sample_video.mp4")  
while video_file.state.name == "PROCESSING":  
    time.sleep(2)
    video_file = get_file(video_file.name)

# 5. Consulta Multimodal
query = """ 
Combina ideas de las entradas:
1. **Imagen**: Describe la escena y su significado.  
2. **Audio**: Extrae mensajes clave que se relacionen con lo visual.  
3. **Video**: Observa la entrada de video y proporciona ideas que conecten con el contexto de la imagen y el audio.  
4. **Búsqueda Web**: Encuentra las últimas actualizaciones o eventos que vinculen todos estos temas.
Resume el tema o historia general que transmiten estas entradas.
"""

# 6. El Agente Multimodal genera una respuesta unificada
agent.print_response(query, images=[image_url], audio=audio_file, videos=[video_file], stream=True)