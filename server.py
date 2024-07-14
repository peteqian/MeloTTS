from fastapi import FastAPI, HTTPException, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from melo.api import TTS
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class TextToSpeechRequest(BaseModel):
    text: str
    accent: str
    speed: float = 1.0

def cleanup_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)

@app.post("/tts")
async def generate_tts(request: TextToSpeechRequest, background_tasks: BackgroundTasks):
    try:
        # Set up the TTS model
        device = 'auto'
        model = TTS(language='EN', device=device)
        speaker_ids = model.hps.data.spk2id

        accent_mapping = {
            'EN-US': 'en-us.wav',
            'EN-BR': 'en-br.wav',
            'EN_INDIA': 'en-india.wav',
            'EN-AU': 'en-au.wav',
            'EN-Default': 'en-default.wav'
        }

        if request.accent not in accent_mapping:
            raise HTTPException(status_code=400, detail="Invalid accent")

        output_path = accent_mapping[request.accent]
        model.tts_to_file(request.text, speaker_ids[request.accent], output_path, speed=request.speed)

        # Schedule the file for deletion after the response is sent
        background_tasks.add_task(cleanup_file, output_path)

        return FileResponse(output_path, media_type='audio/wav', filename=output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)