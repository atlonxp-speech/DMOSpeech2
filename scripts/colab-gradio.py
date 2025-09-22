import sys
sys.path.insert(0, "./src")

import torch
import torchaudio
import uuid
import gradio as gr
from infer import DMOInference

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

tts = DMOInference(
    student_checkpoint_path="./ckpts/model_85000.pt",
    duration_predictor_path="./ckpts/model_1500.pt",
    device=DEVICE,
    model_type="F5TTS_Base"
)

style_state = {"prompt_audio": None, "prompt_text": None}

def prepare_audio_for_download(prompt_audio):
    if prompt_audio is None:
        raise gr.Error("No audio recorded yet.")

    sr, audio_data = prompt_audio
    audio_tensor = torch.from_numpy(audio_data)

    if audio_tensor.dim() == 1:
        audio_tensor = audio_tensor.unsqueeze(0)

    audio_path = f"/tmp/{uuid.uuid4().hex}_ref_download.wav"
    torchaudio.save(audio_path, audio_tensor, sr)

    return audio_path

def initialize_voice(prompt_audio, prompt_text):
    if prompt_audio is None or prompt_text.strip() == "":
        return "Provide both audio and reference text."

    sr, audio_data = prompt_audio
    audio_tensor = torch.from_numpy(audio_data)

    if audio_tensor.dim() == 1:
        audio_tensor = audio_tensor.unsqueeze(0)

    # Save audio exactly as provided by Gradio (float32, no resampling here)
    audio_path = f"/tmp/{uuid.uuid4().hex}_ref.wav"
    torchaudio.save(audio_path, audio_tensor, sr)

    # Pass file paths explicitly to DMOInference (exactly like dmo_tts_api.py)
    style_state["prompt_audio"] = audio_path
    style_state["prompt_text"] = prompt_text.strip()

    return "Voice initialized successfully."

def generate_audio(gen_text):
    if style_state["prompt_audio"] is None or style_state["prompt_text"] is None:
        raise gr.Error("Initialize voice first!")

    if gen_text.strip() == "":
        raise gr.Error("Please enter text to synthesize.")

    # Pass paths explicitly—no manual tensor handling here
    with torch.no_grad():
        generated_audio = tts.generate(
            gen_text=gen_text.strip(),
            audio_path=style_state["prompt_audio"],
            prompt_text=style_state["prompt_text"],
        )

    # generated_audio is numpy float32 array directly from model
    audio_tensor = torch.from_numpy(generated_audio).unsqueeze(0)
    audio_path = f"/tmp/{uuid.uuid4().hex}_generated.wav"
    torchaudio.save(audio_path, audio_tensor, 24000)

    return (24000, generated_audio), audio_path

with gr.Blocks() as demo:
    gr.Markdown("# DMOSpeech2 Gradio Interface (Local)")

    with gr.Tab("Initialize Voice"):
        prompt_audio = gr.Audio(
            sources=["upload", "microphone"],
            type="numpy",
            label="Reference Audio (upload or record)"
        )
        prompt_text = gr.Textbox(label="Reference Text (neutral distinct sentence)")
        download_ref_btn = gr.Button("Prepare Reference Audio for Download")
        download_ref_link = gr.File(label="Download Reference Audio")
        
        download_ref_btn.click(
            prepare_audio_for_download,
            prompt_audio,
            download_ref_link
        )

        init_btn = gr.Button("Initialize Voice")
        init_result = gr.Textbox(label="Initialization Status", interactive=False)
        
        init_btn.click(initialize_voice, [prompt_audio, prompt_text], init_result)

    with gr.Tab("Generate Speech"):
        gen_text = gr.Textbox(label="Text to Synthesize")
        generate_btn = gr.Button("Generate Audio")
        generated_audio = gr.Audio(label="Generated Speech", type="numpy")
        download_btn = gr.File(label="Download Generated Audio")
        
        generate_btn.click(
            generate_audio,
            gen_text,
            [generated_audio, download_btn]
        )

if __name__ == "__main__":
    demo.launch(debug=True, share=True)
