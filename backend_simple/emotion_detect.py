"""
Simple emotion detection module for SwarSense.
"""

import numpy as np
from typing import Optional, Dict

def detect_emotion() -> Optional[str]:
    """
    Detect emotion (demo version).
    
    Returns:
        Detected emotion string or None if detection fails
    """
    try:
        # For demo purposes, return a random emotion
        emotions = ['Happy', 'Neutral', 'Sad', 'Angry', 'Fear', 'Surprise', 'Disgust']
        return np.random.choice(emotions)
    except Exception as e:
        print(f"Emotion detection error: {e}")
        return None

def detect_emotion_from_uploaded_image(uploaded_image) -> Optional[Dict[str, float]]:
    """
    Detect emotion from uploaded image (demo version).
    
    Args:
        uploaded_image: Streamlit uploaded image file
        
    Returns:
        Dictionary with emotion probabilities or None if detection fails
    """
    try:
        # Mock emotion detection for demo
        emotions = ['Happy', 'Neutral', 'Sad', 'Angry', 'Fear', 'Surprise', 'Disgust']
        probs = np.random.random(len(emotions))
        probs = probs / probs.sum()  # Normalize
        
        return dict(zip(emotions, probs))
    except Exception as e:
        print(f"Image emotion detection error: {e}")
        return None

def get_emotion_analysis(emotion_history) -> Dict[str, any]:
    """
    Get comprehensive emotion analysis.
    
    Args:
        emotion_history: List of emotion probability dictionaries
        
    Returns:
        Comprehensive emotion analysis results
    """
    if not emotion_history:
        return {"trend": "No data", "recommendation": "Start recording to analyze emotions"}
    
    # Simple analysis
    latest = emotion_history[-1]
    dominant_emotion = max(latest.get('emotion_probs', {}), key=latest.get('emotion_probs', {}).get)
    confidence = latest.get('emotion_probs', {}).get(dominant_emotion, 0)
    
    recommendations = {
        "Happy": "Great! You look confident and positive.",
        "Neutral": "Try to show more expression in your face.",
        "Sad": "Try to lift your spirits and show more positivity.",
        "Angry": "Take a deep breath and try to relax.",
        "Fear": "Remember, you're doing great! Don't be nervous.",
        "Surprise": "Your animated expression is engaging!",
        "Disgust": "Try to show a more positive expression."
    }
    
    return {
        "dominant_emotion": dominant_emotion,
        "confidence": confidence,
        "recommendations": [recommendations.get(dominant_emotion, "Keep practicing!")],
        "trend": "Stable emotional expression"
    }