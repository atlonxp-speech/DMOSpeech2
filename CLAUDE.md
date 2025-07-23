# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DMOSpeech2 is a reinforcement learning-based text-to-speech (TTS) system implementing Direct Metric Optimization for speech synthesis. This fork adds FastAPI and Gradio interfaces for easier deployment.

## Key Commands

### Environment Setup
```bash
# Create and activate Python 3.10 environment with uv
source setup-source-me.sh

# Download model checkpoints from HuggingFace
./scripts/setup.sh

# Launch Jupyter Lab (optional)
source .venv/bin/activate && ./jupyter-lab.sh
```

### Running Services
```bash
# FastAPI server (port 8000)
python dmo_tts_api.py

# Gradio UI (port 7860)
python gradio_app.py
```

### Development Notes
- **No test suite**: This is a research codebase without unit tests
- **No linting/formatting**: No automated code quality tools configured
- **Manual setup**: Uses shell scripts instead of standard Python build tools

## Architecture Overview

### Core Components
- **Teacher Model** (`model_85000.pt`): F5-TTS base model for initial denoising
- **Student Model**: DMO-optimized model with fewer denoising steps
- **Duration Predictor** (`model_1500.pt`): GRPO-trained for metric optimization

### Key Modules
- `src/infer.py`: Main DMOInference class orchestrating TTS generation
- `src/unimodel.py`: Unified model wrapper for student model
- `src/duration_predictor.py`: Predicts speech duration from text
- `src/dmd_trainer.py`: Direct Metric Distillation training
- `src/grpo_duration_trainer.py`: GRPO reinforcement learning for duration

### API Interfaces
- `dmo_tts_api.py`: FastAPI with `/init_voice` and `/generate_audio` endpoints
- `gradio_app.py`: Two-tab Gradio interface for voice cloning and synthesis

### Model Loading Flow
1. Models loaded from `ckpts/` directory
2. Teacher model provides initial guidance
3. Student model performs fast inference
4. Duration predictor ensures proper timing

### Text Processing Pipeline
1. Text normalization (handles Chinese via jieba/pypinyin)
2. Phoneme conversion using G2P
3. Duration prediction
4. Mel-spectrogram generation
5. Vocoder synthesis (Vocos)

## Working with the Codebase

### Adding Features
- New inference methods go in `src/infer.py`
- API endpoints in `dmo_tts_api.py` or `gradio_app.py`
- Model modifications in `src/unimodel.py` or `src/f5_tts/model/`

### Common Tasks
- **Changing models**: Update paths in inference classes
- **Adding languages**: Modify text processing in `src/f5_tts/infer/utils_infer.py`
- **Adjusting quality**: Tune sampling steps and guidance scale in inference

### Dependencies
- PyTorch with CUDA required
- Platform restrictions: bitsandbytes not available on ARM64/macOS
- Chinese processing requires jieba and pypinyin

## Important Considerations
- Models are large (~500MB each) and downloaded on first setup
- CUDA GPU recommended for reasonable inference speed
- No streaming support yet - generates complete audio before returning
- Reference audio quality significantly impacts voice cloning results