"""
Pronunciation analysis module for SwarSense.
Handles phoneme comparison, pronunciation scoring, and audio feedback.
"""

import pronouncing
from gtts import gTTS
import playsound
import os
import streamlit as st
import tempfile
import difflib
from typing import Optional, Dict, List, Tuple
import re


class PronunciationAnalyzer:
    """Handles pronunciation analysis and feedback."""
    
    def __init__(self):
        """Initialize the pronunciation analyzer."""
        self.temp_dir = tempfile.gettempdir()
    
    def get_phonemes(self, word: str) -> Optional[str]:
        """
        Get phonemes for a word using the pronouncing library.
        
        Args:
            word: Word to get phonemes for
            
        Returns:
            Phoneme string or None if not found
        """
        try:
            phones = pronouncing.phones_for_word(word.lower().strip())
            return phones[0] if phones else None
        except Exception as e:
            st.error(f"❌ Error getting phonemes for '{word}': {e}")
            return None
    
    def calculate_pronunciation_score(self, user_phonemes: str, target_phonemes: str) -> Tuple[float, str]:
        """
        Calculate pronunciation score based on phoneme similarity.
        
        Args:
            user_phonemes: User's phoneme string
            target_phonemes: Target phoneme string
            
        Returns:
            Tuple of (score, feedback)
        """
        if not user_phonemes or not target_phonemes:
            return 0.0, "Could not analyze pronunciation"
        
        # Calculate similarity using difflib
        similarity = difflib.SequenceMatcher(None, user_phonemes, target_phonemes).ratio()
        score = similarity * 100
        
        # Generate feedback based on score
        if score >= 90:
            feedback = "Excellent pronunciation! 🎉"
        elif score >= 80:
            feedback = "Good pronunciation! 👍"
        elif score >= 70:
            feedback = "Fair pronunciation, keep practicing! 💪"
        elif score >= 50:
            feedback = "Needs improvement. Try again! 🔄"
        else:
            feedback = "Significant improvement needed. Practice more! 📚"
        
        return score, feedback
    
    def get_pronunciation_tips(self, user_phonemes: str, target_phonemes: str) -> List[str]:
        """
        Get specific pronunciation tips based on phoneme differences.
        
        Args:
            user_phonemes: User's phoneme string
            target_phonemes: Target phoneme string
            
        Returns:
            List of pronunciation tips
        """
        tips = []
        
        if not user_phonemes or not target_phonemes:
            return ["Could not analyze pronunciation for tips"]
        
        # Find differences
        diff = list(difflib.unified_diff(
            target_phonemes.split(),
            user_phonemes.split(),
            lineterm=""
        ))
        
        if len(diff) > 2:  # More than just headers
            tips.append("Focus on the specific sound differences:")
            for line in diff[2:]:  # Skip headers
                if line.startswith('-'):
                    tips.append(f"• Missing: {line[1:].strip()}")
                elif line.startswith('+'):
                    tips.append(f"• Extra: {line[1:].strip()}")
        
        # General tips based on common issues
        if len(user_phonemes) < len(target_phonemes) * 0.8:
            tips.append("Try to pronounce all syllables clearly")
        
        if len(user_phonemes) > len(target_phonemes) * 1.2:
            tips.append("Try to pronounce more concisely")
        
        return tips if tips else ["Keep practicing to improve your pronunciation!"]
    
    def play_correct_pronunciation(self, word: str) -> bool:
        """
        Play the correct pronunciation of a word.
        
        Args:
            word: Word to play pronunciation for
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create temporary file for audio
            temp_file = os.path.join(self.temp_dir, f"pronunciation_{hash(word)}.mp3")
            
            # Generate speech
            tts = gTTS(text=word, lang='en', slow=False)
            tts.save(temp_file)
            
            # Play audio
            playsound.playsound(temp_file)
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error playing pronunciation: {e}")
            return False
    
    def analyze_pronunciation(self, user_word: str, target_word: str) -> Dict[str, any]:
        """
        Comprehensive pronunciation analysis.
        
        Args:
            user_word: Word spoken by user
            target_word: Target word to compare against
            
        Returns:
            Dictionary with analysis results
        """
        # Get phonemes
        user_phonemes = self.get_phonemes(user_word)
        target_phonemes = self.get_phonemes(target_word)
        
        if not target_phonemes:
            return {
                "error": f"Could not find phonemes for target word '{target_word}'",
                "score": 0,
                "feedback": "Target word not found in dictionary"
            }
        
        if not user_phonemes:
            return {
                "error": f"Could not find phonemes for user word '{user_word}'",
                "score": 0,
                "feedback": "User word not found in dictionary"
            }
        
        # Calculate score and feedback
        score, feedback = self.calculate_pronunciation_score(user_phonemes, target_phonemes)
        
        # Get tips
        tips = self.get_pronunciation_tips(user_phonemes, target_phonemes)
        
        return {
            "user_phonemes": user_phonemes,
            "target_phonemes": target_phonemes,
            "score": score,
            "feedback": feedback,
            "tips": tips,
            "is_correct": score >= 80
        }


# Global pronunciation analyzer instance
pronunciation_analyzer = PronunciationAnalyzer()


def get_phonemes(word: str) -> Optional[str]:
    """
    Convenience function to get phonemes for a word.
    
    Args:
        word: Word to get phonemes for
        
    Returns:
        Phoneme string or None if not found
    """
    return pronunciation_analyzer.get_phonemes(word)


def compare_pronunciation(user_word: str, target_word: str, play_only: bool = False) -> Optional[Dict[str, any]]:
    """
    Compare user pronunciation with target word.
    
    Args:
        user_word: Word spoken by user
        target_word: Target word to compare against
        play_only: If True, only play the correct pronunciation
        
    Returns:
        Analysis results or None if play_only is True
    """
    if play_only:
        pronunciation_analyzer.play_correct_pronunciation(target_word)
        return None
    
    # Perform comprehensive analysis
    analysis = pronunciation_analyzer.analyze_pronunciation(user_word, target_word)
    
    # Display results
    if "error" in analysis:
        st.error(f"❌ {analysis['error']}")
        return analysis
    
    # Display phonemes
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Target phonemes:** {analysis['target_phonemes']}")
    with col2:
        st.write(f"**Your phonemes:** {analysis['user_phonemes']}")
    
    # Display score and feedback
    score = analysis['score']
    st.metric("Pronunciation Score", f"{score:.1f}%", delta=f"{score-50:.1f}%")
    
    if analysis['is_correct']:
        st.success(f"✅ {analysis['feedback']}")
    else:
        st.warning(f"⚠️ {analysis['feedback']}")
    
    # Display tips
    if analysis['tips']:
        with st.expander("💡 Pronunciation Tips"):
            for tip in analysis['tips']:
                st.write(f"• {tip}")
    
    return analysis


def get_pronunciation_tips(user_word: str, target_word: str) -> List[str]:
    """
    Get pronunciation tips for a word comparison.
    
    Args:
        user_word: Word spoken by user
        target_word: Target word to compare against
        
    Returns:
        List of pronunciation tips
    """
    user_phonemes = pronunciation_analyzer.get_phonemes(user_word)
    target_phonemes = pronunciation_analyzer.get_phonemes(target_word)
    
    if user_phonemes and target_phonemes:
        return pronunciation_analyzer.get_pronunciation_tips(user_phonemes, target_phonemes)
    
    return ["Could not analyze pronunciation for tips"]


def play_correct_pronunciation(word: str) -> bool:
    """
    Play the correct pronunciation of a word.
    
    Args:
        word: Word to play pronunciation for
        
    Returns:
        True if successful, False otherwise
    """
    return pronunciation_analyzer.play_correct_pronunciation(word)
