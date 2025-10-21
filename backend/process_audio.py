"""
Audio processing module for SwarSense.
Handles audio transcription, recording, and preprocessing.
"""

import speech_recognition as sr
import tempfile
import os
import wave
import pyaudio
import numpy as np
import streamlit as st
from typing import Optional, Tuple
import io


class AudioProcessor:
    """Handles audio recording, transcription, and processing."""
    
    def __init__(self):
        """Initialize the audio processor with speech recognition engine."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
    
    def transcribe_audio_file(self, audio_file) -> Optional[str]:
        """
        Transcribe audio from uploaded file.
        
        Args:
            audio_file: Streamlit uploaded file object
            
        Returns:
            Transcribed text or None if transcription fails
        """
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Transcribe the audio
            with sr.AudioFile(tmp_file_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            return text
            
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio. Please speak more clearly.")
            return None
        except sr.RequestError as e:
            st.error(f"❌ Speech recognition service error: {e}")
            return None
        except Exception as e:
            st.error(f"❌ Audio processing error: {e}")
            return None
    
    def record_audio(self, duration: int = 5) -> Optional[bytes]:
        """
        Record audio from microphone for specified duration.
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Audio data as bytes or None if recording fails
        """
        try:
            with self.microphone as source:
                st.info(f"🎤 Recording for {duration} seconds... Speak now!")
                audio_data = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
                return audio_data
        except sr.WaitTimeoutError:
            st.error("❌ Recording timeout. Please try again.")
            return None
        except Exception as e:
            st.error(f"❌ Recording error: {e}")
            return None
    
    def transcribe_recorded_audio(self, audio_data) -> Optional[str]:
        """
        Transcribe recorded audio data.
        
        Args:
            audio_data: Audio data from microphone
            
        Returns:
            Transcribed text or None if transcription fails
        """
        try:
            text = self.recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio. Please speak more clearly.")
            return None
        except sr.RequestError as e:
            st.error(f"❌ Speech recognition service error: {e}")
            return None
        except Exception as e:
            st.error(f"❌ Transcription error: {e}")
            return None
    
    def get_audio_duration(self, audio_file) -> float:
        """
        Get duration of audio file in seconds.
        
        Args:
            audio_file: Audio file object
            
        Returns:
            Duration in seconds
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_file.getvalue())
                tmp_file_path = tmp_file.name
            
            with wave.open(tmp_file_path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                sample_rate = wav_file.getframerate()
                duration = frames / float(sample_rate)
            
            os.unlink(tmp_file_path)
            return duration
        except Exception as e:
            st.warning(f"⚠️ Could not determine audio duration: {e}")
            return 0.0


# Global audio processor instance
audio_processor = AudioProcessor()


def transcribe_audio(audio_file) -> Optional[str]:
    """
    Convenience function to transcribe audio file.
    
    Args:
        audio_file: Streamlit uploaded file object
        
    Returns:
        Transcribed text or None if transcription fails
    """
    return audio_processor.transcribe_audio_file(audio_file)


def record_and_transcribe(duration: int = 5) -> Optional[str]:
    """
    Record audio from microphone and transcribe it.
    
    Args:
        duration: Recording duration in seconds
        
    Returns:
        Transcribed text or None if recording/transcription fails
    """
    audio_data = audio_processor.record_audio(duration)
    if audio_data:
        return audio_processor.transcribe_recorded_audio(audio_data)
    return None