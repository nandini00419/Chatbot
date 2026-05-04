"""
Speech-to-Text Module - Wav2Vec2 Integration
=============================================
This module converts speech audio to text using Hugging Face's Wav2Vec2 model.

Features:
- Supports microphone input (via audio file)
- Supports WAV files (no ffmpeg required)
- Automatic audio preprocessing (mono conversion, resampling)
- Uses pretrained Wav2Vec2 model for accurate transcription

Model: facebook/wav2vec2-base-960h
- Trained on 960 hours of LibriSpeech audio
- Supports English language
- Requires 16kHz mono audio input

Note: This version uses librosa and soundfile instead of pydub/ffmpeg
"""

import soundfile as sf
import numpy as np
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch

# Load Wav2Vec2 model and processor globally (loaded once for efficiency)
# Using processor instead of tokenizer for better compatibility
print("Loading Wav2Vec2 model... This may take a moment on first run.")
try:
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    print("Wav2Vec2 model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    processor = None
    model = None


def speech_to_text(audio_file_path):
    """
    Convert speech audio file to text using Wav2Vec2 model.
    
    This function:
    1. Loads the audio file using librosa (no ffmpeg required)
    2. Converts to mono channel and 16kHz sample rate
    3. Processes through Wav2Vec2 model
    4. Returns transcribed text
    
    Args:
        audio_file_path (str): Path to the audio file (WAV format recommended)
    
    Returns:
        str: Transcribed text from the audio
    
    Example:
        >>> text = speech_to_text("user_audio.wav")
        >>> print(text)
        "Hello, how are you today?"
    """
    if processor is None or model is None:
        print("Model not loaded. Please check the error messages above.")
        return ""
    
    try:
        # Step 1: Load audio file using librosa
        # librosa can handle WAV files without ffmpeg
        # It automatically converts to mono and can resample
        try:
            # Load audio with librosa - automatically converts to mono and resamples to 16kHz
            audio_array, sample_rate = librosa.load(
                audio_file_path,
                sr=16000,  # Resample to 16kHz (required by Wav2Vec2)
                mono=True  # Convert to mono
            )
        except Exception as e:
            print(f"Error loading audio with librosa: {e}")
            # Fallback: try soundfile directly (works for WAV files)
            try:
                audio_array, sample_rate = sf.read(audio_file_path)
                # Convert stereo to mono if needed
                if len(audio_array.shape) > 1:
                    audio_array = np.mean(audio_array, axis=1)
                # Resample to 16kHz if needed using librosa
                if sample_rate != 16000:
                    audio_array = librosa.resample(audio_array, orig_sr=sample_rate, target_sr=16000)
                    sample_rate = 16000
            except Exception as e2:
                print(f"Error with soundfile fallback: {e2}")
                return ""
        
        # Step 2: Ensure audio is in float32 format
        # Wav2Vec2 expects float32 values between -1.0 and 1.0
        if audio_array.dtype != np.float32:
            audio_array = audio_array.astype(np.float32)
        
        # Step 3: Normalize audio if needed (ensure values are in [-1, 1] range)
        if len(audio_array) > 0:
            max_val = np.max(np.abs(audio_array))
            if max_val > 0:
                audio_array = audio_array / max_val
        
        # Step 4: Process audio through Wav2Vec2
        # Tokenize the audio (converts to model input format)
        input_values = processor(audio_array, sampling_rate=16000, return_tensors="pt").input_values
        
        # Step 5: Run inference (no gradient computation needed)
        with torch.no_grad():
            # Get model predictions (logits)
            logits = model(input_values).logits
        
        # Step 6: Decode predictions to text
        # Get the most likely token IDs
        predicted_ids = torch.argmax(logits, dim=-1)
        
        # Decode token IDs to text string
        transcription = processor.decode(predicted_ids[0])
        
        return transcription.strip()  # Remove leading/trailing whitespace
    
    except Exception as e:
        print(f"Error in speech_to_text: {e}")
        import traceback
        traceback.print_exc()
        return ""


def speech_to_text_from_array(audio_array, sample_rate=16000):
    """
    Convert speech from numpy array to text.
    
    Useful for real-time processing or when audio is already loaded in memory.
    
    Args:
        audio_array (np.ndarray): Audio data as numpy array
        sample_rate (int): Sample rate of the audio (default: 16000)
    
    Returns:
        str: Transcribed text
    """
    if processor is None or model is None:
        return ""
    
    try:
        # Resample to 16kHz if needed
        if sample_rate != 16000:
            audio_array = librosa.resample(audio_array, orig_sr=sample_rate, target_sr=16000)
            sample_rate = 16000
        
        # Ensure float32 format
        if audio_array.dtype != np.float32:
            audio_array = audio_array.astype(np.float32)
        
        # Normalize if needed
        if len(audio_array) > 0:
            max_val = np.max(np.abs(audio_array))
            if max_val > 0:
                audio_array = audio_array / max_val
        
        # Process through model
        input_values = processor(audio_array, sampling_rate=sample_rate, return_tensors="pt").input_values
        
        with torch.no_grad():
            logits = model(input_values).logits
        
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(predicted_ids[0])
        
        return transcription.strip()
    
    except Exception as e:
        print(f"Error in speech_to_text_from_array: {e}")
        return ""
