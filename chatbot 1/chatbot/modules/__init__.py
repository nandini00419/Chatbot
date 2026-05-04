"""
Voice Chatbot Modules Package
=============================
This package contains modular components for the voice-enabled AI chatbot:
- stt_module: Speech-to-Text conversion
- chatbot_module: AI chatbot using Groq API
- tts_module: Text-to-Speech conversion
"""

from .stt_module import speech_to_text, speech_to_text_from_array
from .chatbot_module import get_chat_response, reset_conversation, get_conversation_history, set_model
from .tts_module import tts_gtts, tts_pyttsx3, tts_advanced_gtts, list_available_voices

__all__ = [
    # STT functions
    'speech_to_text',
    'speech_to_text_from_array',
    # Chatbot functions
    'get_chat_response',
    'reset_conversation',
    'get_conversation_history',
    'set_model',
    # TTS functions
    'tts_gtts',
    'tts_pyttsx3',
    'tts_advanced_gtts',
    'list_available_voices',
]

