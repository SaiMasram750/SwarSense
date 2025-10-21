"""Audio processing utilities.

This module currently exposes `transcribe_audio` as a stub to be implemented
with a preferred speech-to-text backend. For a self-contained demo without
external APIs, we accept the limitation and return None.

Future options:
- Use Vosk or Whisper.cpp for offline transcription
- Use Google Cloud STT or Azure Cognitive Services for online transcription
"""

from __future__ import annotations

from typing import Optional


def transcribe_audio(file_like) -> Optional[str]:
    """
    Transcribe an uploaded WAV file-like object to text.

    Returns the transcribed string if successful or None on failure.
    Placeholder implementation to keep the demo runnable without heavy deps.
    """
    try:
        # Optional lightweight implementation using SpeechRecognition if available.
        # Falls back to None if dependency is missing or recognition fails.
        import speech_recognition as sr  # type: ignore

        recognizer = sr.Recognizer()
        # Streamlit uploads use BytesIO-like objects; ensure we can pass a name or bytes
        with sr.AudioFile(file_like) as source:
            audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except Exception:
            return None
    except Exception:
        return None