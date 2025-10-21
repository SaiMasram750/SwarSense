import base64
from typing import Optional

import streamlit as st

from backend.process_audio import transcribe_audio
from backend.phoneme_check import compare_pronunciation
from backend.emotion_detect import detect_emotion


st.set_page_config(page_title="SwarSense – Emotion-Aware Coach", layout="wide")
st.title("SwarSense – Emotion-Aware Communication Coach")


def render_tts_player(audio_mp3: bytes, label: str = "Pronunciation") -> None:
    """Render an in-page audio player for provided MP3 bytes."""
    if not audio_mp3:
        st.warning("Audio not available.")
        return
    b64 = base64.b64encode(audio_mp3).decode("ascii")
    st.audio(f"data:audio/mp3;base64,{b64}")


with st.sidebar:
    st.header("Practice Settings")
    word = st.text_input("Target word", help="Enter a word to practice")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Play target") and word:
            tts_result = compare_pronunciation(word, word, play_only=True)
            render_tts_player(tts_result.get("audio_mp3", b""), label="Target")
    with col_b:
        st.markdown("[Open Webcam Emotion Detector](backend/model.html)")


left, right = st.columns([2, 1], gap="large")

with left:
    st.subheader("Pronunciation Practice")
    audio_file = st.file_uploader("Upload your speech (WAV)", type=["wav"]) 
    if audio_file and word:
        st.audio(audio_file)
        user_text: Optional[str] = transcribe_audio(audio_file)
        if user_text:
            st.write(f"You said: **{user_text}**")
            cmp = compare_pronunciation(user_text, word)
            if cmp.get("error"):
                st.error(cmp["error"]) 
            else:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric("Pronunciation score", f"{cmp['score']}%")
                with col2:
                    st.caption("Phoneme comparison")
                    st.code(
                        f"Target: {' '.join(cmp['target_phonemes'])}\n"
                        f"Spoken: {' '.join(cmp['user_phonemes'])}"
                    )
                with st.expander("Suggestions and tips"):
                    tips = []
                    for op in cmp["ops"]:
                        if op["op"] == "replace":
                            tips.append(f"Replace {op['spoken']} with {op['target']}")
                        elif op["op"] == "delete":
                            tips.append(f"Emphasize missing {op['target']}")
                        elif op["op"] == "insert":
                            tips.append(f"Reduce extra {op['spoken']}")
                    if tips:
                        st.write("\n".join(f"- {t}" for t in tips))
                        if cmp['score'] < 70:
                            st.info("Try slowing down and articulating stressed vowels.")
                        elif cmp['score'] < 90:
                            st.info("Great! Focus on consonant clusters for polish.")
                    else:
                        st.success("Great match!")
        else:
            st.warning("Could not transcribe audio. Please try another recording.")

with right:
    st.subheader("Emotion Feedback")
    st.caption("Webcam detector runs in browser. You can annotate your session with a self-reported emotion below.")
    emotion = detect_emotion()
    if emotion:
        st.success(f"Detected emotion: {emotion}")
    note = st.text_area("Session notes", placeholder="Confidence tips, speaking rate, pauses…")
    if st.button("Save session"):
        st.session_state.setdefault("sessions", []).append({
            "word": word,
            "notes": note,
            "emotion": emotion,
        })
        st.success("Session saved in memory (export coming soon)")

    if st.session_state.get("sessions"):
        if st.button("Export sessions as CSV"):
            import csv
            import io
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=["word", "emotion", "notes"]) 
            writer.writeheader()
            for row in st.session_state["sessions"]:
                writer.writerow(row)
            st.download_button(
                "Download CSV",
                buffer.getvalue(),
                file_name="swar_sessions.csv",
                mime="text/csv",
            )
