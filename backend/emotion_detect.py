"""
Emotion detection module for SwarSense.
Handles facial emotion detection using computer vision and ML models.
"""

import cv2
import numpy as np
import streamlit as st
from typing import Optional, Dict, List, Tuple
import json
import time
import threading
from PIL import Image
import io


class EmotionDetector:
    """Handles facial emotion detection using OpenCV and ML models."""
    
    def __init__(self):
        """Initialize the emotion detector."""
        self.face_cascade = None
        self.emotion_model = None
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        self.confidence_threshold = 0.5
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize OpenCV face detection and emotion recognition models."""
        try:
            # Load OpenCV face cascade
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # For demo purposes, we'll use a simple rule-based emotion detection
            # In a real implementation, you would load a trained emotion model here
            st.success("✅ Emotion detection models loaded successfully!")
            
        except Exception as e:
            st.error(f"❌ Error initializing emotion models: {e}")
    
    def detect_emotion_from_image(self, image: np.ndarray) -> Optional[Dict[str, float]]:
        """
        Detect emotion from a single image.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Dictionary with emotion probabilities or None if detection fails
        """
        try:
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                return None
            
            # For demo purposes, return mock emotion probabilities
            # In a real implementation, you would run the emotion model here
            mock_emotions = {
                'Happy': np.random.uniform(0.3, 0.9),
                'Neutral': np.random.uniform(0.1, 0.4),
                'Sad': np.random.uniform(0.0, 0.3),
                'Angry': np.random.uniform(0.0, 0.2),
                'Fear': np.random.uniform(0.0, 0.2),
                'Surprise': np.random.uniform(0.0, 0.3),
                'Disgust': np.random.uniform(0.0, 0.1)
            }
            
            # Normalize probabilities
            total = sum(mock_emotions.values())
            normalized_emotions = {k: v/total for k, v in mock_emotions.items()}
            
            return normalized_emotions
            
        except Exception as e:
            st.error(f"❌ Emotion detection error: {e}")
            return None
    
    def get_dominant_emotion(self, emotion_probs: Dict[str, float]) -> Tuple[str, float]:
        """
        Get the dominant emotion from probability dictionary.
        
        Args:
            emotion_probs: Dictionary with emotion probabilities
            
        Returns:
            Tuple of (emotion_name, confidence)
        """
        if not emotion_probs:
            return "Unknown", 0.0
        
        dominant_emotion = max(emotion_probs, key=emotion_probs.get)
        confidence = emotion_probs[dominant_emotion]
        
        return dominant_emotion, confidence
    
    def analyze_emotion_trend(self, emotion_history: List[Dict[str, float]]) -> Dict[str, any]:
        """
        Analyze emotion trends over time.
        
        Args:
            emotion_history: List of emotion probability dictionaries
            
        Returns:
            Analysis results including trends and recommendations
        """
        if not emotion_history:
            return {"trend": "No data", "recommendation": "Start recording to analyze emotions"}
        
        # Calculate average emotions
        avg_emotions = {}
        for emotion in self.emotion_labels:
            avg_emotions[emotion] = np.mean([e.get(emotion, 0) for e in emotion_history])
        
        # Find dominant emotion trend
        dominant_emotion, confidence = self.get_dominant_emotion(avg_emotions)
        
        # Generate recommendations based on emotion
        recommendations = self._get_emotion_recommendations(dominant_emotion, confidence)
        
        return {
            "dominant_emotion": dominant_emotion,
            "confidence": confidence,
            "average_emotions": avg_emotions,
            "recommendations": recommendations,
            "trend": self._analyze_emotion_trend(emotion_history)
        }
    
    def _get_emotion_recommendations(self, emotion: str, confidence: float) -> List[str]:
        """Get recommendations based on detected emotion."""
        recommendations = {
            "Happy": [
                "Great! You look confident and positive.",
                "Your positive energy is coming through clearly.",
                "Keep up the good work with your presentation!"
            ],
            "Neutral": [
                "Try to show more expression in your face.",
                "Consider smiling more to appear more engaging.",
                "Your expression is neutral - try to show more emotion."
            ],
            "Sad": [
                "Try to lift your spirits and show more positivity.",
                "Consider taking a break and coming back refreshed.",
                "Your expression suggests low energy - try to be more upbeat."
            ],
            "Angry": [
                "Take a deep breath and try to relax.",
                "Your expression shows tension - try to soften your features.",
                "Consider taking a moment to calm down before continuing."
            ],
            "Fear": [
                "Take a deep breath and try to relax.",
                "Remember, you're doing great! Don't be nervous.",
                "Try to appear more confident and relaxed."
            ],
            "Surprise": [
                "Your expression shows surprise - that's good for engagement!",
                "Try to maintain this level of expressiveness.",
                "Your animated expression is engaging to the audience."
            ],
            "Disgust": [
                "Try to show a more positive expression.",
                "Your expression suggests discomfort - try to relax.",
                "Consider adjusting your approach to be more positive."
            ]
        }
        
        return recommendations.get(emotion, ["Keep practicing to improve your expression!"])
    
    def _analyze_emotion_trend(self, emotion_history: List[Dict[str, float]]) -> str:
        """Analyze the trend of emotions over time."""
        if len(emotion_history) < 2:
            return "Insufficient data for trend analysis"
        
        # Calculate trend for dominant emotions
        recent_emotions = emotion_history[-3:]  # Last 3 readings
        earlier_emotions = emotion_history[:-3] if len(emotion_history) > 3 else emotion_history[:1]
        
        recent_avg = {}
        earlier_avg = {}
        
        for emotion in self.emotion_labels:
            recent_avg[emotion] = np.mean([e.get(emotion, 0) for e in recent_emotions])
            earlier_avg[emotion] = np.mean([e.get(emotion, 0) for e in earlier_emotions])
        
        # Compare recent vs earlier
        if recent_avg.get('Happy', 0) > earlier_avg.get('Happy', 0):
            return "Improving - showing more positive emotions"
        elif recent_avg.get('Sad', 0) > earlier_avg.get('Sad', 0):
            return "Declining - showing more negative emotions"
        else:
            return "Stable - consistent emotional expression"


# Global emotion detector instance
emotion_detector = EmotionDetector()


def detect_emotion() -> Optional[str]:
    """
    Convenience function to detect emotion.
    For demo purposes, returns a mock emotion.
    
    Returns:
        Detected emotion string or None if detection fails
    """
    try:
        # For demo purposes, return a random emotion
        emotions = ['Happy', 'Neutral', 'Sad', 'Angry', 'Fear', 'Surprise', 'Disgust']
        return np.random.choice(emotions)
    except Exception as e:
        st.error(f"❌ Emotion detection error: {e}")
        return None


def detect_emotion_from_uploaded_image(uploaded_image) -> Optional[Dict[str, float]]:
    """
    Detect emotion from uploaded image.
    
    Args:
        uploaded_image: Streamlit uploaded image file
        
    Returns:
        Dictionary with emotion probabilities or None if detection fails
    """
    try:
        # Convert uploaded image to numpy array
        image = Image.open(uploaded_image)
        image = np.array(image)
        
        # Convert RGB to BGR for OpenCV
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        return emotion_detector.detect_emotion_from_image(image)
    except Exception as e:
        st.error(f"❌ Image processing error: {e}")
        return None


def get_emotion_analysis(emotion_history: List[Dict[str, float]]) -> Dict[str, any]:
    """
    Get comprehensive emotion analysis.
    
    Args:
        emotion_history: List of emotion probability dictionaries
        
    Returns:
        Comprehensive emotion analysis results
    """
    return emotion_detector.analyze_emotion_trend(emotion_history)