"""
Simple pronunciation analysis module for SwarSense.
"""

from typing import Optional, Tuple

try:
    import pronouncing
    PRONOUNCING_AVAILABLE = True
except ImportError:
    PRONOUNCING_AVAILABLE = False

def get_phonemes(word: str) -> Optional[str]:
    """
    Get phonemes for a word.
    
    Args:
        word: Word to get phonemes for
        
    Returns:
        Phoneme string or None if not found
    """
    if not PRONOUNCING_AVAILABLE:
        return None
    
    try:
        phones = pronouncing.phones_for_word(word.lower().strip())
        return phones[0] if phones else None
    except Exception as e:
        print(f"Error getting phonemes: {e}")
        return None

def compare_pronunciation(user_word: str, target_word: str, play_only: bool = False) -> Optional[dict]:
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
        return None
    
    if not PRONOUNCING_AVAILABLE:
        return {"error": "Pronunciation analysis not available"}
    
    # Get phonemes
    user_phonemes = get_phonemes(user_word)
    target_phonemes = get_phonemes(target_word)
    
    if not target_phonemes:
        return {"error": f"Could not find phonemes for target word '{target_word}'"}
    
    if not user_phonemes:
        return {"error": f"Could not find phonemes for user word '{user_word}'"}
    
    # Simple comparison
    if user_phonemes == target_phonemes:
        score = 100.0
        feedback = "Excellent pronunciation! 🎉"
    else:
        # Simple similarity calculation
        user_parts = user_phonemes.split()
        target_parts = target_phonemes.split()
        common_parts = set(user_parts) & set(target_parts)
        score = (len(common_parts) / max(len(user_parts), len(target_parts))) * 100
        
        if score >= 90:
            feedback = "Excellent pronunciation! 🎉"
        elif score >= 80:
            feedback = "Good pronunciation! 👍"
        elif score >= 70:
            feedback = "Fair pronunciation, keep practicing! 💪"
        else:
            feedback = "Needs improvement. Try again! 🔄"
    
    return {
        "user_phonemes": user_phonemes,
        "target_phonemes": target_phonemes,
        "score": score,
        "feedback": feedback,
        "is_correct": score >= 80
    }

def play_correct_pronunciation(word: str) -> bool:
    """
    Play the correct pronunciation of a word.
    
    Args:
        word: Word to play pronunciation for
        
    Returns:
        True if successful, False otherwise
    """
    # This would require playsound or similar - simplified for deployment
    return False