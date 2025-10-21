import streamlit as st
from backend.process_audio import transcribe_audio
from backend.phoneme_check import compare_pronunciation
from backend.emotion_detect import detect_emotion

st.title("SpeakEase – Emotion-Aware Communication Coach")

word = st.text_input("Enter a word to practice:")
if st.button("Play Correct Pronunciation"):
    compare_pronunciation(word, word, play_only=True)

audio_file = st.file_uploader("Upload your speech (WAV format)", type=["wav"])
if audio_file and word:
    st.audio(audio_file)
    user_text = transcribe_audio(audio_file)
    st.write(f"You said: **{user_text}**")
    compare_pronunciation(user_text, word)

st.subheader("Facial Emotion Detection")
st.markdown("Use webcam in browser to detect emotion via Teachable Machine.")
st.markdown("[Open Emotion Detector](backend/model.html)")

# Get emotion feedback
emotion = detect_emotion()
if emotion:
    st.write(f"Detected emotion: **{emotion}**")
