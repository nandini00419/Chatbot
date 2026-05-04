"""
Standalone Example Script - Voice Chatbot Pipeline
===================================================
This script demonstrates how to use each module independently.
You can run this script to test the complete pipeline without Flask.

Usage:
    python example_standalone.py

This script shows:
1. Speech-to-text conversion
2. Chatbot interaction with context
3. Text-to-speech generation
"""

import os
from modules.stt_module import speech_to_text
from modules.chatbot_module import get_chat_response, reset_conversation
from modules.tts_module import tts_gtts, tts_pyttsx3

def main():
    """
    Main function demonstrating the complete voice chatbot pipeline.
    """
    print("=" * 60)
    print("Voice-Enabled AI Chatbot - Standalone Example")
    print("=" * 60)
    print()
    
    # Example 1: Speech-to-Text
    print("Step 1: Speech-to-Text (STT)")
    print("-" * 60)
    audio_file = "static/audio/user_audio.wav"
    
    if os.path.exists(audio_file):
        print(f"Processing audio file: {audio_file}")
        transcribed_text = speech_to_text(audio_file)
        print(f"Transcribed text: {transcribed_text}")
    else:
        print(f"Audio file not found: {audio_file}")
        print("Using example text instead...")
        transcribed_text = "Hello, how are you today?"
    
    print()
    
    # Example 2: Chatbot Response
    print("Step 2: Chatbot Response (Groq API)")
    print("-" * 60)
    print(f"User input: {transcribed_text}")
    
    # Reset conversation for clean start
    reset_conversation()
    
    # Get chatbot response (first turn)
    bot_response_1 = get_chat_response(transcribed_text)
    print(f"Bot response: {bot_response_1}")
    print()
    
    # Multi-turn conversation example
    print("Multi-turn conversation example:")
    follow_up = "Tell me more about that"
    print(f"User follow-up: {follow_up}")
    bot_response_2 = get_chat_response(follow_up)
    print(f"Bot response (with context): {bot_response_2}")
    print()
    
    # Example 3: Text-to-Speech
    print("Step 3: Text-to-Speech (TTS)")
    print("-" * 60)
    
    # Using gTTS (online, high quality)
    print("Generating speech with gTTS...")
    audio_path_gtts = tts_gtts(
        bot_response_1,
        filename="static/audio/example_response_gtts.mp3"
    )
    print(f"Audio saved to: {audio_path_gtts}")
    print()
    
    # Using pyttsx3 (offline, system voices)
    print("Generating speech with pyttsx3 (offline)...")
    try:
        audio_path_pyttsx3 = tts_pyttsx3(
            bot_response_1,
            filename="static/audio/example_response_pyttsx3.wav"
        )
        print(f"Audio saved to: {audio_path_pyttsx3}")
    except Exception as e:
        print(f"pyttsx3 error: {e}")
    
    print()
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


def example_stt_only():
    """
    Example: Speech-to-Text only
    """
    print("\n--- STT Only Example ---")
    audio_file = "static/audio/user_audio.wav"
    if os.path.exists(audio_file):
        text = speech_to_text(audio_file)
        print(f"Transcribed: {text}")
    else:
        print("Audio file not found")


def example_chatbot_only():
    """
    Example: Chatbot only (text input/output)
    """
    print("\n--- Chatbot Only Example ---")
    reset_conversation()
    
    user_inputs = [
        "Hello!",
        "What's the weather like?",
        "Tell me a joke"
    ]
    
    for user_input in user_inputs:
        response = get_chat_response(user_input)
        print(f"User: {user_input}")
        print(f"Bot: {response}")
        print()


def example_tts_only():
    """
    Example: Text-to-Speech only
    """
    print("\n--- TTS Only Example ---")
    text = "Hello! This is a test of the text-to-speech system."
    
    # gTTS
    audio_path = tts_gtts(text, "static/audio/test_gtts.mp3")
    print(f"gTTS audio saved to: {audio_path}")
    
    # pyttsx3
    try:
        audio_path = tts_pyttsx3(text, "static/audio/test_pyttsx3.wav")
        print(f"pyttsx3 audio saved to: {audio_path}")
    except Exception as e:
        print(f"pyttsx3 error: {e}")


if __name__ == "__main__":
    # Run main example
    main()
    
    # Uncomment to run individual module examples:
    # example_stt_only()
    # example_chatbot_only()
    # example_tts_only()

