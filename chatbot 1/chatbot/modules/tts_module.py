"""
Text-to-Speech Module
=====================
This module converts text to spoken audio using multiple TTS engines.

Available Engines:
1. gTTS (Google Text-to-Speech) - Online, high quality, requires internet
2. pyttsx3 - Offline, uses system voices, no internet required

Features:
- Multiple TTS engine support
- Audio file generation
- Configurable voice settings (for pyttsx3)
"""

import os
from gtts import gTTS
import pyttsx3


def tts_gtts(text, filename="static/audio/response.mp3", lang="en", slow=False):
    """
    Convert text to speech using Google Text-to-Speech (gTTS).
    
    This is an online service that provides high-quality, natural-sounding voices.
    Requires an internet connection.
    
    Args:
        text (str): Text to convert to speech
        filename (str): Output file path (default: "static/audio/response.mp3")
        lang (str): Language code (default: "en" for English)
        slow (bool): If True, speaks slower (default: False)
    
    Returns:
        str: Path to the generated audio file
    
    Example:
        >>> audio_path = tts_gtts("Hello, how are you?", "output.mp3")
        >>> print(audio_path)
        "output.mp3"
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Create gTTS object with text and language settings
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Save to file
        tts.save(filename)
        
        return filename
    
    except Exception as e:
        print(f"Error in gTTS: {e}")
        # Fallback to pyttsx3 if gTTS fails
        print("Falling back to pyttsx3...")
        return tts_pyttsx3(text, filename)


def tts_pyttsx3(text, filename="static/audio/response.mp3", rate=150, volume=0.9, voice_id=None):
    """
    Convert text to speech using pyttsx3 (offline TTS).
    
    This uses system-installed voices and works offline.
    Voice quality depends on your system's installed voices.
    
    Args:
        text (str): Text to convert to speech
        filename (str): Output file path (default: "static/audio/response.mp3")
        rate (int): Speech rate in words per minute (default: 150)
        volume (float): Volume level 0.0 to 1.0 (default: 0.9)
        voice_id (int): Voice ID to use (None = default voice)
    
    Returns:
        str: Path to the generated audio file
    
    Example:
        >>> audio_path = tts_pyttsx3("Hello world", "output.wav")
        >>> print(audio_path)
        "output.wav"
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Initialize TTS engine
        engine = pyttsx3.init()
        
        # Set speech rate (words per minute)
        engine.setProperty('rate', rate)
        
        # Set volume (0.0 to 1.0)
        engine.setProperty('volume', volume)
        
        # Set voice if specified
        if voice_id is not None:
            voices = engine.getProperty('voices')
            if voice_id < len(voices):
                engine.setProperty('voice', voices[voice_id].id)
        
        # Save to file
        # Note: pyttsx3 saves as WAV by default, but filename extension determines format
        engine.save_to_file(text, filename)
        engine.runAndWait()
        
        return filename
    
    except Exception as e:
        print(f"Error in pyttsx3: {e}")
        return filename


def list_available_voices():
    """
    List all available system voices (for pyttsx3).
    
    Returns:
        list: List of voice information dictionaries
    """
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        voice_list = []
        for idx, voice in enumerate(voices):
            voice_list.append({
                'id': idx,
                'name': voice.name,
                'gender': voice.gender if hasattr(voice, 'gender') else 'unknown',
                'languages': voice.languages if hasattr(voice, 'languages') else []
            })
        
        return voice_list
    
    except Exception as e:
        print(f"Error listing voices: {e}")
        return []


def tts_advanced_gtts(text, filename="static/audio/response.mp3", lang="en", tld="com", slow=False):
    """
    Advanced gTTS with custom top-level domain (TLD).
    
    Different TLDs can provide slightly different accents:
    - "com" - US English
    - "co.uk" - UK English
    - "com.au" - Australian English
    
    Args:
        text (str): Text to convert to speech
        filename (str): Output file path
        lang (str): Language code
        tld (str): Top-level domain for accent (default: "com")
        slow (bool): Slow speech mode
    
    Returns:
        str: Path to the generated audio file
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        tts = gTTS(text=text, lang=lang, tld=tld, slow=slow)
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error in advanced gTTS: {e}")
        return tts_pyttsx3(text, filename)
