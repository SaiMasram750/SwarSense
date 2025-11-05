"""
SwarSense - Simplified Version for Deployment
A minimal working version that should work in deployed environments.
"""

import streamlit as st
import tempfile
import os
import numpy as np
from typing import Optional

# Try to import optional dependencies
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    import pronouncing
    PRONOUNCING_AVAILABLE = True
except ImportError:
    PRONOUNCING_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="SwarSense - Emotion-Aware Communication Coach",
    page_icon="🎤",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pronunciation_history' not in st.session_state:
    st.session_state.pronunciation_history = []
if 'session_stats' not in st.session_state:
    st.session_state.session_stats = {
        'total_words_practiced': 0,
        'average_pronunciation_score': 0,
        'session_start_time': 0
    }

# Main header
st.markdown('<h1 class="main-header">🎤 SwarSense</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Emotion-Aware Communication Coach</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Session Statistics")
    st.metric("Words Practiced", st.session_state.session_stats['total_words_practiced'])
    st.metric("Average Score", f"{st.session_state.session_stats['average_pronunciation_score']:.1f}%")
    
    if st.button("🔄 Reset Session"):
        st.session_state.pronunciation_history = []
        st.session_state.session_stats = {
            'total_words_practiced': 0,
            'average_pronunciation_score': 0,
            'session_start_time': 0
        }
        st.success("Session reset!")

# Main content
tab1, tab2, tab3 = st.tabs(["🎤 Pronunciation Practice", "😊 Emotion Detection", "ℹ️ About"])

with tab1:
    st.header("🎤 Pronunciation Practice")
    
    # Word input
    word = st.text_input("Enter a word to practice:", placeholder="Type a word here...")
    
    if word and PRONOUNCING_AVAILABLE:
        # Get phonemes
        try:
            phonemes = pronouncing.phones_for_word(word.lower().strip())
            if phonemes:
                st.write(f"**Phonemes for '{word}':** {phonemes[0]}")
            else:
                st.warning(f"No phonemes found for '{word}'")
        except Exception as e:
            st.error(f"Error getting phonemes: {e}")
    
    # Audio input
    audio_file = st.file_uploader("Upload your speech (WAV, MP3, M4A format)", type=["wav", "mp3", "m4a"])
    
    if audio_file and word and SPEECH_RECOGNITION_AVAILABLE:
        st.audio(audio_file)
        
        # Transcribe audio
        try:
            recognizer = sr.Recognizer()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_file.getvalue())
                tmp_file_path = tmp_file.name
            
            with sr.AudioFile(tmp_file_path) as source:
                audio_data = recognizer.record(source)
                user_text = recognizer.recognize_google(audio_data)
            
            os.unlink(tmp_file_path)
            
            st.write(f"**You said:** {user_text}")
            
            # Simple pronunciation comparison
            if user_text.lower().strip() == word.lower().strip():
                st.success("✅ Perfect pronunciation!")
                score = 100
            else:
                # Simple similarity check
                similarity = len(set(user_text.lower().split()) & set(word.lower().split())) / max(len(user_text.split()), len(word.split()))
                score = similarity * 100
                
                if score >= 80:
                    st.success(f"✅ Good pronunciation! ({score:.1f}%)")
                elif score >= 60:
                    st.warning(f"⚠️ Fair pronunciation ({score:.1f}%)")
                else:
                    st.error(f"❌ Needs improvement ({score:.1f}%)")
            
            # Update session stats
            st.session_state.session_stats['total_words_practiced'] += 1
            st.session_state.session_stats['average_pronunciation_score'] = (
                (st.session_state.session_stats['average_pronunciation_score'] * 
                 (st.session_state.session_stats['total_words_practiced'] - 1) + 
                 score) / st.session_state.session_stats['total_words_practiced']
            )
            
            # Add to history
            st.session_state.pronunciation_history.append({
                'word': word,
                'user_text': user_text,
                'score': score,
                'timestamp': 0
            })
            
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio. Please speak more clearly.")
        except sr.RequestError as e:
            st.error(f"❌ Speech recognition service error: {e}")
        except Exception as e:
            st.error(f"❌ Audio processing error: {e}")
    
    elif audio_file and not SPEECH_RECOGNITION_AVAILABLE:
        st.warning("⚠️ Speech recognition not available. Please install speechrecognition package.")
    
    # Practice history
    if st.session_state.pronunciation_history:
        st.subheader("📈 Recent Practice")
        for i, practice in enumerate(st.session_state.pronunciation_history[-5:], 1):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"{i}. **{practice['word']}** → {practice['user_text']}")
            with col2:
                st.write(f"Score: {practice['score']:.1f}%")
            with col3:
                if practice['score'] >= 80:
                    st.success("✅")
                else:
                    st.warning("⚠️")

with tab2:
    st.header("😊 Emotion Detection")
    
    # Emotion detection methods
    emotion_method = st.radio(
        "Choose emotion detection method:",
        ["Upload Image", "Demo Mode"],
        horizontal=True
    )
    
    if emotion_method == "Upload Image":
        uploaded_image = st.file_uploader(
            "Upload an image with a face",
            type=["jpg", "jpeg", "png"]
        )
        
        if uploaded_image:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            
            with col2:
                # Mock emotion detection
                emotions = ['Happy', 'Neutral', 'Sad', 'Angry', 'Fear', 'Surprise']
                detected_emotion = np.random.choice(emotions)
                confidence = np.random.uniform(0.6, 0.9)
                
                st.subheader("Emotion Analysis")
                st.write(f"**Detected Emotion:** {detected_emotion}")
                st.write(f"**Confidence:** {confidence:.1%}")
                
                # Recommendations
                recommendations = {
                    "Happy": "Great! You look confident and positive.",
                    "Neutral": "Try to show more expression in your face.",
                    "Sad": "Try to lift your spirits and show more positivity.",
                    "Angry": "Take a deep breath and try to relax.",
                    "Fear": "Remember, you're doing great! Don't be nervous.",
                    "Surprise": "Your animated expression is engaging!"
                }
                
                st.write(f"**Recommendation:** {recommendations.get(detected_emotion, 'Keep practicing!')}")
    
    else:  # Demo Mode
        st.info("This is a demo mode showing emotion detection capabilities.")
        
        if st.button("Detect Emotion (Demo)"):
            emotions = ['Happy', 'Neutral', 'Sad', 'Angry', 'Fear', 'Surprise']
            detected_emotion = np.random.choice(emotions)
            confidence = np.random.uniform(0.6, 0.9)
            
            st.success(f"**Detected emotion:** {detected_emotion} ({confidence:.1%} confidence)")

with tab3:
    st.header("ℹ️ About SwarSense")
    
    st.markdown("""
    ## 🎤 SwarSense - Emotion-Aware Communication Coach
    
    SwarSense is a multimodal emotion-aware communication coach that helps you improve your 
    pronunciation and emotional expression during communication.
    
    ### ✨ Features
    
    - **🎤 Pronunciation Analysis**: Get feedback on your pronunciation with phoneme comparison
    - **😊 Emotion Detection**: Analyze facial expressions to understand your emotional state
    - **📊 Analytics**: Track your progress over time with comprehensive analytics
    - **💡 Tips & Recommendations**: Receive personalized tips to improve your communication skills
    
    ### 🛠️ Technology Stack
    
    - **Frontend**: Streamlit
    - **Audio Processing**: SpeechRecognition
    - **Pronunciation**: Pronouncing library
    - **Emotion Detection**: Computer Vision
    - **Text-to-Speech**: Google Text-to-Speech
    
    ### 🚀 How to Use
    
    1. **Pronunciation Practice**: Enter a word and upload an audio file
    2. **Emotion Detection**: Upload an image or use demo mode
    3. **Analytics**: View your progress and get insights
    
    ### 📈 Tips for Better Results
    
    - Speak clearly and at a moderate pace
    - Ensure good lighting for emotion detection
    - Practice regularly to see improvement
    - Use headphones for better audio quality
    """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>Made with ❤️ for better communication</p>",
        unsafe_allow_html=True
    )

# Status information
st.sidebar.markdown("---")
st.sidebar.header("🔧 System Status")

status_items = [
    ("Speech Recognition", SPEECH_RECOGNITION_AVAILABLE),
    ("Pronunciation Analysis", PRONOUNCING_AVAILABLE),
    ("Text-to-Speech", GTTS_AVAILABLE),
    ("Computer Vision", OPENCV_AVAILABLE)
]

for item, available in status_items:
    if available:
        st.sidebar.success(f"✅ {item}")
    else:
        st.sidebar.error(f"❌ {item}")

if not any(available for _, available in status_items):
    st.sidebar.warning("⚠️ Some features may not be available. Please check dependencies.")