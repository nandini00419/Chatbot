"""
Voice-Enabled AI Chatbot - Flask Application
============================================
Main Flask application that orchestrates the voice chatbot pipeline:
1. Speech-to-Text (STT) - Converts user audio to text
2. Chatbot - Generates AI response using Groq API
3. Text-to-Speech (TTS) - Converts bot response to audio

Features:
- Multi-turn conversation handling
- Context memory across exchanges
- Modular architecture for easy maintenance
"""

from flask import Flask, request, jsonify, render_template
import os
from modules.stt_module import speech_to_text
from modules.chatbot_module import get_chat_response, reset_conversation
from modules.tts_module import tts_gtts

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "static/audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Maximum file size for audio uploads (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/")
def index():
    """
    Serve the main chatbot interface page.
    """
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint that processes voice or text input and returns text + audio response.
    
    Pipeline:
    1. Receive audio file OR text input from client
    2. If audio: Convert speech to text (STT), else use provided text
    3. Get chatbot response (with context)
    4. Convert response to speech (TTS)
    5. Return JSON with user text, bot response, and audio file path
    
    Returns:
        JSON response with:
        - user_text: User input (transcribed or typed)
        - bot_response: AI chatbot response
        - audio_file: Path to generated audio file
    """
    user_text = None
    
    # Check if text input was provided (typing mode)
    if request.is_json:
        data = request.get_json()
        user_text = data.get("text", "").strip()
    
    # If no text, check for audio file (mic mode)
    if not user_text:
        if "audio_file" not in request.files:
            return jsonify({"error": "No text or audio file provided"}), 400
        
        audio_file = request.files["audio_file"]
        
        # Check if file has a name
        if audio_file.filename == "":
            return jsonify({"error": "Empty filename"}), 400
        
        # Save uploaded audio file
        filepath = os.path.join(UPLOAD_FOLDER, "user_audio.wav")
        audio_file.save(filepath)
        
        try:
            # Step 1: Speech-to-Text (STT)
            # Convert the user's audio to text using Wav2Vec2
            print("Processing speech-to-text...")
            user_text = speech_to_text(filepath)
            
            if not user_text or user_text.strip() == "":
                # Still return a response even if transcription failed
                return jsonify({
                    "error": "Could not transcribe audio. Please try again.",
                    "user_text": "",
                    "bot_response": "I couldn't understand your audio. Could you please try speaking more clearly?",
                    "audio_file": None
                })
        except Exception as e:
            import traceback
            print(f"Error in STT: {e}")
            traceback.print_exc()
            return jsonify({
                "error": str(e),
                "user_text": "",
                "bot_response": "I'm sorry, I encountered an error processing your audio. Please try again.",
                "audio_file": None
            })
    
    if not user_text or user_text.strip() == "":
        return jsonify({"error": "Empty input provided"}), 400
    
    print(f"User said: {user_text}")
    
    try:
        # Step 2: Chatbot Response
        # Get AI response using Groq API (maintains conversation context)
        print("Getting chatbot response...")
        try:
            bot_response = get_chat_response(user_text)
            print(f"Bot responded: {bot_response}")
        except Exception as e:
            print(f"Error getting chatbot response: {e}")
            bot_response = "I'm sorry, I'm having trouble connecting to the AI service. Please try again."
        
        # Step 3: Text-to-Speech (TTS)
        # Convert bot response to audio using gTTS
        print("Generating speech...")
        audio_url = None
        try:
            audio_path = tts_gtts(
                bot_response,
                filename=os.path.join(UPLOAD_FOLDER, "response.mp3")
            )
            # Convert Windows path to web-friendly path
            audio_url = "/" + audio_path.replace("\\", "/")
        except Exception as e:
            print(f"Error generating TTS: {e}")
            # Continue without audio if TTS fails
        
        # Return JSON response (always return success, even if some steps failed)
        return jsonify({
            "user_text": user_text,
            "bot_response": bot_response,
            "audio_file": audio_url
        })
    
    except Exception as e:
        import traceback
        print(f"Error in chat endpoint: {e}")
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "user_text": user_text or "",
            "bot_response": "I'm sorry, I encountered an error processing your request. Please try again.",
            "audio_file": None
        })


@app.route("/reset", methods=["POST"])
def reset():
    """
    Reset conversation context.
    
    This clears the conversation history, allowing the chatbot to start fresh.
    """
    reset_conversation()
    return jsonify({"message": "Conversation context reset successfully"})


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    """
    return jsonify({"status": "healthy", "message": "Voice chatbot API is running"})


if __name__ == "__main__":
    print("=" * 50)
    print("Voice-Enabled AI Chatbot")
    print("=" * 50)
    print("Starting Flask server...")
    print("Access the chatbot at: http://localhost:5000")
    print("=" * 50)
    
    # Run Flask app in debug mode
    # Set debug=False in production
    app.run(debug=True, host="0.0.0.0", port=5000)
