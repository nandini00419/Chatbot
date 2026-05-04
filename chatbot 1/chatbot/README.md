# Voice-Enabled AI Chatbot

A complete voice-enabled AI chatbot system that processes speech input, generates intelligent responses using Groq API, and converts responses back to speech. Built with a modular architecture for easy maintenance and extension.

## Features

✅ **Speech-to-Text**: Converts user speech to text using Wav2Vec2 from Hugging Face  
✅ **AI Chatbot**: Generates responses using Groq API (Llama models)  
✅ **Text-to-Speech**: Converts bot responses to audio using gTTS or pyttsx3  
✅ **Multi-turn Conversations**: Maintains context across multiple exchanges  
✅ **Modular Architecture**: Each component can be used independently  
✅ **Web Interface**: Flask-based web application with microphone input  
✅ **Comprehensive Comments**: Well-documented code with step-by-step explanations  

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Audio     │ --> │ Speech-to-   │ --> │   Groq      │ --> │ Text-to-    │
│   Input     │     │ Text (STT)   │     │   Chatbot   │     │ Speech(TTS) │
│             │     │              │     │             │     │             │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for downloading models and using Groq API)

### Step 1: Clone or Download the Project

```bash
cd chatbot
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The first run will download the Wav2Vec2 model (~300MB), which may take a few minutes.

### Step 4: Set Groq API Key (Optional)

The API key is already configured in `modules/chatbot_module.py`, but you can also set it as an environment variable:

```bash
# Windows
set GROQ_API_KEY=your_api_key_here

# Linux/Mac
export GROQ_API_KEY=your_api_key_here
```

## Usage

### Web Application (Recommended)

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Click the microphone button** 🎤 to start recording
   - Speak for up to 3 seconds
   - The audio will be processed automatically
   - You'll see the transcribed text and bot response
   - The bot's response will be played as audio

### Standalone Script

Run the example script to test individual modules:

```bash
python example_standalone.py
```

## Module Usage

### 1. Speech-to-Text Module

```python
from modules.stt_module import speech_to_text

# Convert audio file to text
text = speech_to_text("path/to/audio.wav")
print(text)
```

**Supported formats**: WAV, MP3, OGG, FLAC, and more  
**Model**: facebook/wav2vec2-base-960h  
**Requirements**: 16kHz mono audio (automatically converted)

### 2. Chatbot Module

```python
from modules.chatbot_module import get_chat_response, reset_conversation

# Single turn conversation
response = get_chat_response("Hello, how are you?")
print(response)

# Multi-turn conversation (maintains context)
response1 = get_chat_response("What's the weather?")
response2 = get_chat_response("What about tomorrow?")  # Remembers previous context

# Reset conversation
reset_conversation()
```

**API**: Groq API  
**Model**: llama-3.1-8b-instant (configurable)  
**Features**: Context memory, configurable temperature and max tokens

### 3. Text-to-Speech Module

```python
from modules.tts_module import tts_gtts, tts_pyttsx3

# Using gTTS (online, high quality)
audio_path = tts_gtts("Hello world", "output.mp3")

# Using pyttsx3 (offline, system voices)
audio_path = tts_pyttsx3("Hello world", "output.wav", rate=150, volume=0.9)
```

**gTTS**: Requires internet, high quality, natural voices  
**pyttsx3**: Offline, uses system voices, no internet required

## Project Structure

```
chatbot/
├── app.py                      # Main Flask application
├── example_standalone.py       # Standalone example script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── modules/
│   ├── __init__.py
│   ├── stt_module.py          # Speech-to-Text module
│   ├── chatbot_module.py      # Chatbot module (Groq API)
│   └── tts_module.py          # Text-to-Speech module
├── static/
│   ├── audio/                 # Audio files storage
│   ├── css/
│   │   └── style.css          # Web interface styles
│   └── js/
│       └── script.js          # Web interface JavaScript
└── templates/
    └── index.html             # Web interface HTML
```

## Configuration

### Groq API Models

You can change the model in `modules/chatbot_module.py`:

```python
MODEL_NAME = "llama-3.1-8b-instant"  # Fast, efficient
# MODEL_NAME = "llama-3.1-70b-versatile"  # More capable, slower
# MODEL_NAME = "mixtral-8x7b-32768"  # Good balance
```

### TTS Settings

**gTTS options**:
- `lang`: Language code (default: "en")
- `slow`: Slow speech mode (default: False)
- `tld`: Top-level domain for accent ("com", "co.uk", "com.au")

**pyttsx3 options**:
- `rate`: Speech rate in words per minute (default: 150)
- `volume`: Volume level 0.0-1.0 (default: 0.9)
- `voice_id`: System voice ID

## Optional Improvements

### 1. Context Memory Enhancement

**Current**: Keeps last 20 messages  
**Improvement**: Implement sliding window with importance scoring

```python
# In chatbot_module.py, add:
def manage_context(history, max_tokens=2000):
    """Keep most important messages within token limit"""
    # Implementation here
```

### 2. Better TTS Voices

**Current**: Basic gTTS and system voices  
**Improvements**:
- Use **ElevenLabs API** for premium voices
- Use **Azure Cognitive Services** for natural voices
- Use **Amazon Polly** for AWS integration

```python
# Example: ElevenLabs integration
from elevenlabs import generate, play
audio = generate(text="Hello", voice="Rachel")
play(audio)
```

### 3. Streaming Audio Input

**Current**: Fixed 3-second recording  
**Improvements**:
- Implement **VAD (Voice Activity Detection)** for automatic start/stop
- Use **WebRTC** for real-time streaming
- Add **silence detection** for better UX

### 4. Enhanced STT

**Current**: Wav2Vec2 base model  
**Improvements**:
- Use **Whisper** model for better accuracy
- Add **language detection**
- Support **multiple languages**

```python
# Example: Whisper integration
from transformers import WhisperProcessor, WhisperForConditionalGeneration
processor = WhisperProcessor.from_pretrained("openai/whisper-base")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
```

### 5. Real-time Processing

**Current**: Request-response model  
**Improvements**:
- Implement **WebSocket** for real-time bidirectional communication
- Add **streaming responses** from Groq API
- Use **chunked audio processing**

### 6. Error Handling & Logging

**Improvements**:
- Add comprehensive logging with `logging` module
- Implement retry logic for API calls
- Add error recovery mechanisms

### 7. User Interface Enhancements

**Improvements**:
- Add **visual waveform** display
- Show **processing status** indicators
- Add **conversation history** panel
- Implement **voice commands** for controls

## Troubleshooting

### Issue: "No module named 'groq'"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Model download fails"

**Solution**: Check internet connection. Models are downloaded from Hugging Face on first run.

### Issue: "gTTS fails"

**Solution**: 
- Check internet connection
- Falls back to pyttsx3 automatically
- Or use pyttsx3 directly for offline use

### Issue: "Audio not playing"

**Solution**:
- Check browser audio permissions
- Ensure audio files are generated in `static/audio/`
- Check browser console for errors

### Issue: "Groq API errors"

**Solution**:
- Verify API key is correct
- Check API quota/limits
- Ensure internet connection is active

## API Endpoints

- `GET /` - Main web interface
- `POST /chat` - Process audio and return response
- `POST /reset` - Reset conversation context
- `GET /health` - Health check

## License

This project is provided as-is for educational and development purposes.

## Credits

- **Wav2Vec2**: Facebook AI Research
- **Groq API**: Groq Inc.
- **gTTS**: Google Text-to-Speech
- **Flask**: Pallets Projects

## Support

For issues or questions, please check:
1. Troubleshooting section above
2. Module documentation in code comments
3. Example scripts for usage patterns

---

**Happy Chatting! 🎤🤖**

