"""
SwarSense - Deployment Version
A simplified version that should work in deployed environments.
"""

import streamlit as st
import tempfile
import os
import numpy as np
from typing import Optional

# Try to import backend modules
try:
    from backend_simple.process_audio import transcribe_audio, record_and_transcribe
    from backend_simple.phoneme_check import compare_pronunciation, get_phonemes, play_correct_pronunciation
    from backend_simple.emotion_detect import detect_emotion, detect_emotion_from_uploaded_image, get_emotion_analysis
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False
    st.warning("⚠️ Backend modules not available. Using fallback functionality.")

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
    
    if word and BACKEND_AVAILABLE:
        # Get phonemes
        phonemes = get_phonemes(word)
        if phonemes:
            st.write(f"**Phonemes for '{word}':** {phonemes}")
        else:
            st.warning(f"No phonemes found for '{word}'")
    
    # Audio input
    audio_file = st.file_uploader("Upload your speech (WAV, MP3, M4A format)", type=["wav", "mp3", "m4a"])
    
    if audio_file and word and BACKEND_AVAILABLE:
        st.audio(audio_file)
        
        # Transcribe and analyze
        with st.spinner("Processing audio..."):
            user_text = transcribe_audio(audio_file)
        
        if user_text:
            st.write(f"**You said:** {user_text}")
            
            # Analyze pronunciation
            analysis = compare_pronunciation(user_text, word)
            
            if analysis and "error" not in analysis:
                # Display results
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Target phonemes:** {analysis['target_phonemes']}")
                with col2:
                    st.write(f"**Your phonemes:** {analysis['user_phonemes']}")
                
                # Display score and feedback
                score = analysis['score']
                st.metric("Pronunciation Score", f"{score:.1f}%")
                
                if analysis['is_correct']:
                    st.success(f"✅ {analysis['feedback']}")
                else:
                    st.warning(f"⚠️ {analysis['feedback']}")
                
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
            else:
                error_msg = analysis.get('error', 'Unknown error') if analysis else 'Analysis failed'
                st.error(f"❌ {error_msg}")
        else:
            st.error("❌ Could not transcribe audio. Please try again.")
    
    elif audio_file and not BACKEND_AVAILABLE:
        st.warning("⚠️ Backend modules not available. Please check the deployment.")
    
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
    
    if emotion_method == "Upload Image" and BACKEND_AVAILABLE:
        uploaded_image = st.file_uploader(
            "Upload an image with a face",
            type=["jpg", "jpeg", "png"]
        )
        
        if uploaded_image:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            
            with col2:
                with st.spinner("Detecting emotions..."):
                    emotion_probs = detect_emotion_from_uploaded_image(uploaded_image)
                
                if emotion_probs:
                    st.subheader("Emotion Analysis")
                    
                    # Display emotion probabilities
                    for emotion, prob in emotion_probs.items():
                        st.progress(prob, text=f"{emotion}: {prob:.2%}")
                    
                    # Get dominant emotion
                    dominant_emotion = max(emotion_probs, key=emotion_probs.get)
                    confidence = emotion_probs[dominant_emotion]
                    
                    st.success(f"**Dominant Emotion:** {dominant_emotion} ({confidence:.1%} confidence)")
                    
                    # Get recommendations
                    analysis = get_emotion_analysis([{'emotion_probs': emotion_probs}])
                    if analysis.get('recommendations'):
                        st.write("**Recommendations:**")
                        for rec in analysis['recommendations']:
                            st.write(f"• {rec}")
    
    else:  # Demo Mode
        st.info("This is a demo mode showing emotion detection capabilities.")
        
        if st.button("Detect Emotion (Demo)"):
            if BACKEND_AVAILABLE:
                with st.spinner("Detecting emotions..."):
                    emotion = detect_emotion()
                
                if emotion:
                    st.success(f"**Detected emotion:** {emotion}")
            else:
                # Fallback demo
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

if BACKEND_AVAILABLE:
    st.sidebar.success("✅ Backend modules loaded")
else:
    st.sidebar.error("❌ Backend modules not available")
    st.sidebar.info("Using fallback functionality")