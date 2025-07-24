import sys
sys.path.insert(0, "./src")

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import torch
import torchaudio
import uuid
import uvicorn
from transformers import AutoTokenizer
from infer import DMOInference

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize the model explicitly as confirmed working
tts = DMOInference(
    student_checkpoint_path="./ckpts/model_85000.pt",
    duration_predictor_path="./ckpts/model_1500.pt",
    device=DEVICE,
    model_type="F5TTS_Base"
)

app = FastAPI()

# Explicit state storage for reference voice
style_state = {"prompt_audio": None, "prompt_text": None}

@app.post("/init_voice")
async def init_voice(audio_file: UploadFile = File(...), reference_text: str = Form(...)):
    audio_data, sr = torchaudio.load(audio_file.file)
    audio_path = f"/tmp/{uuid.uuid4().hex}_ref.wav"
    torchaudio.save(audio_path, audio_data, sr)
    
    style_state["prompt_audio"] = audio_path
    style_state["prompt_text"] = reference_text
    
    return JSONResponse({"status": "Voice style initialized.", "audio_saved": audio_path})

@app.post("/generate_audio")
async def generate_audio(target_text: str = Form(...)):
    if style_state["prompt_audio"] is None or style_state["prompt_text"] is None:
        return JSONResponse({"error": "Initialize voice first."}, status_code=400)

    with torch.no_grad():
        generated_audio = tts.generate(
            gen_text=target_text,
            audio_path=style_state["prompt_audio"],
            prompt_text=style_state["prompt_text"]
        )

    audio_tensor = torch.from_numpy(generated_audio).unsqueeze(0)
    filename = f"/tmp/{uuid.uuid4().hex}_gen.wav"
    torchaudio.save(filename, audio_tensor, 24000)

    return FileResponse(filename, media_type='audio/wav', filename="generated.wav")

if __name__ == "__main__":
    print("Starting FastAPI server on http://0.0.0.0:8000 (network accessible)")
    print("Access API documentation at http://0.0.0.0:8000/docs")
    print("WARNING: This exposes the service to your local network")
    uvicorn.run(app, host="0.0.0.0", port=8000)

