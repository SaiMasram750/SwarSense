"""
Test file for SwarSense application.
Basic tests to ensure core functionality works.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.phoneme_check import get_phonemes, calculate_pronunciation_score
from backend.emotion_detect import EmotionDetector
from config import PRONUNCIATION_SETTINGS, EMOTION_SETTINGS


class TestPronunciationAnalysis(unittest.TestCase):
    """Test pronunciation analysis functionality."""
    
    def test_get_phonemes(self):
        """Test phoneme extraction."""
        # Test with a simple word
        phonemes = get_phonemes("hello")
        self.assertIsNotNone(phonemes)
        self.assertIsInstance(phonemes, str)
    
    def test_pronunciation_scoring(self):
        """Test pronunciation scoring."""
        # Test with identical phonemes
        score, feedback = calculate_pronunciation_score("HH AH0 L OW1", "HH AH0 L OW1")
        self.assertEqual(score, 100.0)
        self.assertIn("Excellent", feedback)
        
        # Test with different phonemes
        score, feedback = calculate_pronunciation_score("HH AH0 L OW1", "HH EH0 L OW1")
        self.assertLess(score, 100.0)
        self.assertIsInstance(feedback, str)


class TestEmotionDetection(unittest.TestCase):
    """Test emotion detection functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.emotion_detector = EmotionDetector()
    
    def test_emotion_detector_initialization(self):
        """Test emotion detector initialization."""
        self.assertIsNotNone(self.emotion_detector)
        self.assertIsInstance(self.emotion_detector.emotion_labels, list)
        self.assertEqual(len(self.emotion_detector.emotion_labels), 7)
    
    def test_get_dominant_emotion(self):
        """Test dominant emotion extraction."""
        emotion_probs = {
            "Happy": 0.8,
            "Neutral": 0.1,
            "Sad": 0.1
        }
        emotion, confidence = self.emotion_detector.get_dominant_emotion(emotion_probs)
        self.assertEqual(emotion, "Happy")
        self.assertEqual(confidence, 0.8)


class TestConfiguration(unittest.TestCase):
    """Test configuration settings."""
    
    def test_pronunciation_settings(self):
        """Test pronunciation settings."""
        self.assertIn("min_score_threshold", PRONUNCIATION_SETTINGS)
        self.assertGreater(PRONUNCIATION_SETTINGS["min_score_threshold"], 0)
    
    def test_emotion_settings(self):
        """Test emotion settings."""
        self.assertIn("emotion_labels", EMOTION_SETTINGS)
        self.assertIsInstance(EMOTION_SETTINGS["emotion_labels"], list)
        self.assertGreater(len(EMOTION_SETTINGS["emotion_labels"]), 0)


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)