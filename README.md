# DMOSpeech 2 (Fork)

This repository is a fork of the original [DMOSpeech2 repository](https://github.com/yl4579/DMOSpeech2). The original README has been renamed to `original-README.md`.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) - Python package installer and virtual environment manager

## Setup

1. **Activate the virtual environment:**
   ```bash
   source setup-source-me.sh
   ```

2. **Run the setup script:**
   ```bash
   ./scripts/setup.sh
   ```

## Jupyter Lab Setup

Launch Jupyter Lab:
```bash
source .venv/bin/activate && ./jupyter-lab.sh
```

### Notebook Demos

Two one-cell demos are provided:

1. **`src/serveDMO.ipynb`** - FastAPI demo
   - Load and run the single cell to start the FastAPI server
   - Access the API at `http://localhost:8000`

2. **`src/gradio-test.ipynb`** - Gradio UI demo
   - Load and run the single cell to start the Gradio interface
   - Access the UI at `http://localhost:7860`

## Standalone Python Servers

### 1. FastAPI Server (without Jupyter)

```bash
python ./dmo_tts_api.py
```

API endpoints:
- `POST /init_voice` - Initialize voice with reference audio
- `POST /generate_audio` - Generate speech from text

### 2. Gradio UI Server (without Jupyter)

```bash
python gradio_app.py
```

Access the interactive UI at `http://localhost:7860`

## Sample Clients

TBD

## Testing

### Remote Access via SSH Tunnel

To access the Gradio interface (port 7860) or FastAPI (port 8000) from a remote machine, use SSH port forwarding:

```bash
# From your local machine (e.g., Mac) to access Gradio on remote server
ssh -L 7860:localhost:7860 user@swarm

# To access both Gradio and FastAPI
ssh -L 7860:localhost:7860 -L 8000:localhost:8000 user@swarm

# Then access in your local browser:
# - Gradio UI: http://localhost:7860
# - FastAPI docs: http://localhost:8000/docs
```

This enables microphone access and full UI functionality from your local browser.

## API Usage Examples

### REST API Example

```bash
# Initialize voice with reference audio
curl -X POST "http://localhost:8000/init_voice" \
  -F "audio_file=@reference.wav" \
  -F "reference_text=Your reference text here"

# Generate speech from text
curl -X POST "http://localhost:8000/generate_audio" \
  -F "target_text=This is the text I want synthesized." \
  --output generated_audio.wav
```

## Acknowledgments

- Original DMOSpeech2 repository: [DMOSpeech2](https://github.com/yl4579/DMOSpeech2)
- Additional codebase references: [F5-TTS](https://github.com/SWivid/F5-TTS), [DMD2](https://github.com/tianweiy/DMD2), [simple\_GRPO](https://github.com/lsdefine/simple_GRPO)

---

This fork aims to provide enhanced ease-of-use and seamless integration of DMOSpeech2 into broader workflows and user interfaces.

