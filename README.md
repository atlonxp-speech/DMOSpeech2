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
   *Note: This downloads large model files (~500MB each) to the `ckpts/` directory from HuggingFace.*

## Usage

### HuggingFace Spaces Demo

Try the original DMOSpeech2 online without any setup:
- **HuggingFace Spaces** (Original Repository): https://huggingface.co/spaces/yl4579/DMOSpeech2-demo

### Google Colab (Cloud GPU)

For quick testing without local setup, use the Google Colab notebook:
- Open `DOMSpeech2_gradio_colab_GPU.ipynb` in Google Colab
- Run all cells to set up environment and launch Gradio interface
- Provides free GPU access for faster inference

### Local Development (Recommended)

For single-machine development and testing. Services bind to `127.0.0.1` (localhost only) for security.

#### FastAPI Server
```bash
python scripts/local-fastapi.py
```
- Access API at: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs

#### Gradio UI
```bash
python scripts/local-gradio.py
```
- Access UI at: http://127.0.0.1:7860

#### Jupyter Lab
```bash
./scripts/jupyter-lab-local.sh
```
- Access Jupyter at: http://127.0.0.1:8888

#### Jupyter Notebooks
Three notebook demos are available:

1. **`src/serveDMO.ipynb`** - FastAPI demo
   - Run the cell to start FastAPI server on port 8000

2. **`src/gradio-test.ipynb`** - Gradio UI demo  
   - Run the cell to start Gradio interface on port 7860

3. **`DOMSpeech2_gradio_colab_GPU.ipynb`** - Google Colab demo with GPU support
   - Run DMOSpeech2 in Google Colab with free GPU access
   - Includes all necessary setup and Gradio interface

### Remote Access (SSH Tunnels)

To access local services from a remote machine, use SSH port forwarding:

```bash
# From your remote machine to access local services
ssh -L 7860:localhost:7860 -L 8000:localhost:8000 user@hostname

# Then access in your remote browser:
# - Gradio UI: http://localhost:7860  
# - FastAPI docs: http://localhost:8000/docs
```

This enables microphone access and full UI functionality from remote browsers while maintaining security.

### Network Access (Advanced)

⚠️ **Security Warning**: These scripts expose services to your local network. Only use on trusted networks behind firewalls.

#### FastAPI Server (Network)
```bash
python scripts/remote-fastapi.py
```
- Access from any device on your network: http://YOUR_IP:8000

#### Gradio UI (Network)  
```bash
python scripts/remote-gradio.py
```
- Access from any device on your network: http://YOUR_IP:7860

#### Jupyter Lab (Network)
```bash
./scripts/jupyter-lab-remote.sh
```
- Access from any device on your network: http://YOUR_IP:8888

## API Usage Examples

### REST API Example

```bash
# Initialize voice with reference audio
curl -X POST "http://127.0.0.1:8000/init_voice" \
  -F "audio_file=@reference.wav" \
  -F "reference_text=Your reference text here"

# Generate speech from text
curl -X POST "http://127.0.0.1:8000/generate_audio" \
  -F "target_text=This is the text I want synthesized." \
  --output generated_audio.wav
```

For network access, replace `127.0.0.1` with your server's IP address.

## Security Considerations

### Local Development (127.0.0.1)
- ✅ **Secure**: Services only accessible from the same machine
- ✅ **Recommended**: For development and testing
- ✅ **Safe**: No network exposure

### SSH Tunnels
- ✅ **Secure**: Encrypted connection to remote services
- ✅ **Flexible**: Access remote services as if they were local
- ✅ **Best Practice**: For remote access to development servers

### Network Access (0.0.0.0)
- ⚠️ **Caution Required**: Exposes services to local network
- ⚠️ **Firewall Needed**: Ensure proper network security
- ⚠️ **No Authentication**: Services have no built-in security
- ⚠️ **HTTP Only**: No encryption (consider HTTPS for production)

### Production Deployment
For production use, consider:
- HTTPS/SSL certificates  
- Authentication and authorization
- Rate limiting and monitoring
- Reverse proxy (nginx, Apache)
- Network security hardening

## Troubleshooting

### Common Issues

1. **Port already in use**: Change port numbers in scripts if conflicts occur
2. **Permission denied**: Ensure scripts are executable (`chmod +x scripts/*.sh`)
3. **Module not found**: Verify virtual environment is activated
4. **CUDA errors**: Check GPU availability and PyTorch installation

### Getting Help

- Check the original documentation in `original-README.md`
- Review error logs for specific issues
- Ensure all prerequisites are installed

## Acknowledgments

- Original DMOSpeech2 repository: [DMOSpeech2](https://github.com/yl4579/DMOSpeech2)
- Additional codebase references: [F5-TTS](https://github.com/SWivid/F5-TTS), [DMD2](https://github.com/tianweiy/DMD2), [simple\_GRPO](https://github.com/lsdefine/simple_GRPO)

---

This fork aims to provide enhanced ease-of-use and seamless integration of DMOSpeech2 into broader workflows and user interfaces.