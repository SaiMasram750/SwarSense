"""
Simple audio processing module for SwarSense.
"""

import tempfile
import os
from typing import Optional

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

def transcribe_audio(audio_file) -> Optional[str]:
    """
    Transcribe audio from uploaded file.
    
    Args:
        audio_file: Streamlit uploaded file object
        
    Returns:
        Transcribed text or None if transcription fails
    """
    if not SPEECH_RECOGNITION_AVAILABLE:
        return None
    
    try:
        recognizer = sr.Recognizer()
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Transcribe the audio
        with sr.AudioFile(tmp_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        return text
        
    except Exception as e:
        print(f"Audio transcription error: {e}")
        return None

def record_and_transcribe(duration: int = 5) -> Optional[str]:
    """
    Record audio from microphone and transcribe it.
    
    Args:
        duration: Recording duration in seconds
        
    Returns:
        Transcribed text or None if recording/transcription fails
    """
    # This is a simplified version - live recording would require PyAudio
    return None