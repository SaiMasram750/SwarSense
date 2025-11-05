"""
Configuration file for SwarSense.
Contains all configuration settings and constants.
"""

import os
from typing import Dict, List

# Application settings
APP_NAME = "SwarSense"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Emotion-Aware Communication Coach"

# Audio settings
AUDIO_SETTINGS = {
    "sample_rate": 44100,
    "channels": 1,
    "chunk_size": 1024,
    "max_duration": 30,  # seconds
    "supported_formats": ["wav", "mp3", "m4a", "flac"]
}

# Pronunciation settings
PRONUNCIATION_SETTINGS = {
    "min_score_threshold": 80,
    "excellent_threshold": 90,
    "good_threshold": 80,
    "fair_threshold": 70,
    "needs_improvement_threshold": 50
}

# Emotion detection settings
EMOTION_SETTINGS = {
    "confidence_threshold": 0.5,
    "emotion_labels": [
        "Angry", "Disgust", "Fear", "Happy", 
        "Sad", "Surprise", "Neutral"
    ],
    "face_detection_scale": 1.1,
    "face_detection_min_neighbors": 4
}

# UI settings
UI_SETTINGS = {
    "page_title": "SwarSense - Emotion-Aware Communication Coach",
    "page_icon": "🎤",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# File paths
PATHS = {
    "temp_dir": "/tmp",
    "model_dir": "backend/model",
    "audio_dir": "audio",
    "image_dir": "images"
}

# Session settings
SESSION_SETTINGS = {
    "max_history_items": 100,
    "auto_save_interval": 300,  # seconds
    "session_timeout": 3600  # seconds
}

# Error messages
ERROR_MESSAGES = {
    "audio_transcription_failed": "Could not transcribe audio. Please try again.",
    "emotion_detection_failed": "Could not detect emotions. Please try again.",
    "pronunciation_analysis_failed": "Could not analyze pronunciation. Please try again.",
    "file_upload_failed": "File upload failed. Please check the file format.",
    "network_error": "Network error. Please check your connection.",
    "model_loading_failed": "Could not load required models. Please restart the application."
}

# Success messages
SUCCESS_MESSAGES = {
    "audio_transcribed": "Audio transcribed successfully!",
    "emotion_detected": "Emotion detected successfully!",
    "pronunciation_analyzed": "Pronunciation analyzed successfully!",
    "file_uploaded": "File uploaded successfully!",
    "session_saved": "Session saved successfully!"
}

# Tips and recommendations
PRONUNCIATION_TIPS = {
    "general": [
        "Speak clearly and at a moderate pace",
        "Practice difficult sounds repeatedly",
        "Record yourself and listen back",
        "Use a mirror to watch your mouth movements",
        "Practice with tongue twisters"
    ],
    "phoneme_specific": {
        "vowels": "Focus on clear vowel sounds",
        "consonants": "Ensure consonant sounds are crisp",
        "syllables": "Pronounce each syllable clearly",
        "stress": "Pay attention to word stress patterns"
    }
}

EMOTION_TIPS = {
    "Happy": [
        "Great! You look confident and positive",
        "Your positive energy is coming through clearly",
        "Keep up the good work with your presentation!"
    ],
    "Neutral": [
        "Try to show more expression in your face",
        "Consider smiling more to appear more engaging",
        "Your expression is neutral - try to show more emotion"
    ],
    "Sad": [
        "Try to lift your spirits and show more positivity",
        "Consider taking a break and coming back refreshed",
        "Your expression suggests low energy - try to be more upbeat"
    ],
    "Angry": [
        "Take a deep breath and try to relax",
        "Your expression shows tension - try to soften your features",
        "Consider taking a moment to calm down before continuing"
    ],
    "Fear": [
        "Take a deep breath and try to relax",
        "Remember, you're doing great! Don't be nervous",
        "Try to appear more confident and relaxed"
    ],
    "Surprise": [
        "Your expression shows surprise - that's good for engagement!",
        "Try to maintain this level of expressiveness",
        "Your animated expression is engaging to the audience"
    ],
    "Disgust": [
        "Try to show a more positive expression",
        "Your expression suggests discomfort - try to relax",
        "Consider adjusting your approach to be more positive"
    ]
}

# Demo settings
DEMO_SETTINGS = {
    "sample_words": [
        "hello", "world", "pronunciation", "communication",
        "emotion", "confidence", "practice", "improvement"
    ],
    "demo_emotions": [
        "Happy", "Neutral", "Sad", "Angry", "Fear", "Surprise"
    ]
}