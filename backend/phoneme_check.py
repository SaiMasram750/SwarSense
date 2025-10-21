import pronouncing
from gtts import gTTS
import playsound

def get_phonemes(word):
    phones = pronouncing.phones_for_word(word)
    return phones[0] if phones else None

def compare_pronunciation(user_word, target_word, play_only=False):
    import os
    import streamlit as st
    
    target_phonemes = get_phonemes(target_word)
    if play_only:
        tts = gTTS(text=target_word, lang='en')
        tts.save("correct.mp3")
        playsound.playsound("correct.mp3")
        # Clean up the temporary file
        if os.path.exists("correct.mp3"):
            os.remove("correct.mp3")
        return

    user_phonemes = get_phonemes(user_word)
    st.write(f"Target phonemes: **{target_phonemes}**")
    st.write(f"Your phonemes:   **{user_phonemes}**")
    if user_phonemes == target_phonemes:
        st.success("✅ Good pronunciation!")
    else:
        st.error("❌ Needs improvement.")
