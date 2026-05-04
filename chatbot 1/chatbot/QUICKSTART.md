# Quick Start Guide

Get your voice-enabled AI chatbot running in 5 minutes!

## Step-by-Step Setup

### 1. Install Dependencies (2 minutes)

```bash
# Activate virtual environment (if using one)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install all packages
pip install -r requirements.txt
```

**Note**: First installation will download Wav2Vec2 model (~300MB). This is a one-time download.

### 2. Verify Groq API Key (30 seconds)

The API key is already configured in `modules/chatbot_module.py`. If you want to use a different key:

```python
# Edit modules/chatbot_module.py, line 14:
GROQ_API_KEY = "your_new_api_key_here"
```

### 3. Run the Application (30 seconds)

```bash
python app.py
```

You should see:
```
==================================================
Voice-Enabled AI Chatbot
==================================================
Starting Flask server...
Access the chatbot at: http://localhost:5000
==================================================
```

### 4. Test the Chatbot (1 minute)

1. Open browser: `http://localhost:5000`
2. Click the microphone button 🎤
3. Speak for up to 3 seconds
4. Wait for processing
5. See your transcribed text and bot response
6. Listen to the audio response

## Testing Individual Modules

### Test Speech-to-Text Only

```python
from modules.stt_module import speech_to_text
text = speech_to_text("static/audio/user_audio.wav")
print(text)
```

### Test Chatbot Only

```python
from modules.chatbot_module import get_chat_response
response = get_chat_response("Hello!")
print(response)
```

### Test Text-to-Speech Only

```python
from modules.tts_module import tts_gtts
tts_gtts("Hello world", "output.mp3")
```

### Run Complete Example

```bash
python example_standalone.py
```

## Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| Module not found | `pip install -r requirements.txt` |
| Groq API error | Check API key in `modules/chatbot_module.py` |
| Audio not playing | Check browser permissions, console for errors |
| Model download slow | Normal on first run, ~300MB download |
| gTTS fails | Falls back to pyttsx3 automatically |

## Next Steps

- Read `README.md` for detailed documentation
- Check `example_standalone.py` for code examples
- Explore module files for customization options
- See "Optional Improvements" in README for enhancements

## Need Help?

1. Check the troubleshooting section in `README.md`
2. Review code comments in module files
3. Test individual modules using examples above

---

**You're all set! Start chatting! 🎤🤖**

