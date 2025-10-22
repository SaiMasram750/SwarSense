"""
Demo script for SwarSense functionality.
This script demonstrates the core features without running the full Streamlit app.
"""

from backend.phoneme_check import get_phonemes, pronunciation_analyzer
from backend.emotion_detect import EmotionDetector
import numpy as np

def demo_pronunciation():
    """Demo pronunciation analysis functionality."""
    print("🎤 Pronunciation Analysis Demo")
    print("=" * 40)
    
    # Test words
    test_words = ["hello", "world", "pronunciation", "communication"]
    
    for word in test_words:
        phonemes = get_phonemes(word)
        print(f"Word: {word}")
        print(f"Phonemes: {phonemes}")
        print("-" * 20)
    
    # Test pronunciation comparison
    print("\nPronunciation Comparison Demo:")
    user_phonemes = "HH AH0 L OW1"  # "hello"
    target_phonemes = "HH AH0 L OW1"  # "hello"
    
    score, feedback = pronunciation_analyzer.calculate_pronunciation_score(user_phonemes, target_phonemes)
    print(f"User phonemes: {user_phonemes}")
    print(f"Target phonemes: {target_phonemes}")
    print(f"Score: {score:.1f}%")
    print(f"Feedback: {feedback}")

def demo_emotion_detection():
    """Demo emotion detection functionality."""
    print("\n😊 Emotion Detection Demo")
    print("=" * 40)
    
    # Initialize emotion detector
    emotion_detector = EmotionDetector()
    
    # Test emotion analysis
    mock_emotions = {
        'Happy': 0.7,
        'Neutral': 0.2,
        'Sad': 0.1
    }
    
    emotion, confidence = emotion_detector.get_dominant_emotion(mock_emotions)
    print(f"Detected emotion: {emotion}")
    print(f"Confidence: {confidence:.1%}")
    
    # Test recommendations
    recommendations = emotion_detector._get_emotion_recommendations(emotion, confidence)
    print(f"Recommendations:")
    for rec in recommendations:
        print(f"  • {rec}")

def demo_session_stats():
    """Demo session statistics."""
    print("\n📊 Session Statistics Demo")
    print("=" * 40)
    
    # Mock session data
    session_stats = {
        'total_words_practiced': 15,
        'average_pronunciation_score': 78.5,
        'total_emotions_detected': 8,
        'session_duration': 25.5
    }
    
    print(f"Words practiced: {session_stats['total_words_practiced']}")
    print(f"Average score: {session_stats['average_pronunciation_score']:.1f}%")
    print(f"Emotions detected: {session_stats['total_emotions_detected']}")
    print(f"Session duration: {session_stats['session_duration']:.1f} minutes")

def main():
    """Run all demos."""
    print("🎤 SwarSense - Emotion-Aware Communication Coach")
    print("=" * 50)
    print("Demo of core functionality\n")
    
    try:
        demo_pronunciation()
        demo_emotion_detection()
        demo_session_stats()
        
        print("\n✅ All demos completed successfully!")
        print("\nTo run the full application, use:")
        print("streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    main()