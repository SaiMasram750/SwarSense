"""
SwarSense - Emotion-Aware Communication Coach
A multimodal emotion-aware communication coach that analyzes pronunciation and facial expressions.
"""

import streamlit as st
import time
import json
from typing import Dict, List, Optional
import numpy as np

# Import backend modules
from backend.process_audio import transcribe_audio, record_and_transcribe, audio_processor
from backend.phoneme_check import compare_pronunciation, get_pronunciation_tips, play_correct_pronunciation
from backend.emotion_detect import detect_emotion, detect_emotion_from_uploaded_image, get_emotion_analysis

# Page configuration
st.set_page_config(
    page_title="SwarSense - Emotion-Aware Communication Coach",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    .success-card {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .warning-card {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .error-card {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pronunciation_history' not in st.session_state:
    st.session_state.pronunciation_history = []
if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = []
if 'session_stats' not in st.session_state:
    st.session_state.session_stats = {
        'total_words_practiced': 0,
        'average_pronunciation_score': 0,
        'total_emotions_detected': 0,
        'session_start_time': time.time()
    }

# Main header
st.markdown('<h1 class="main-header">🎤 SwarSense</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Emotion-Aware Communication Coach</p>', unsafe_allow_html=True)

# Sidebar for session info
with st.sidebar:
    st.header("📊 Session Statistics")
    
    # Session stats
    session_duration = time.time() - st.session_state.session_stats['session_start_time']
    st.metric("Session Duration", f"{int(session_duration//60)}m {int(session_duration%60)}s")
    st.metric("Words Practiced", st.session_state.session_stats['total_words_practiced'])
    st.metric("Average Score", f"{st.session_state.session_stats['average_pronunciation_score']:.1f}%")
    st.metric("Emotions Detected", st.session_state.session_stats['total_emotions_detected'])
    
    # Quick actions
    st.header("🚀 Quick Actions")
    if st.button("🎵 Play Sample Word", use_container_width=True):
        sample_word = "hello"
        play_correct_pronunciation(sample_word)
        st.success(f"Playing pronunciation of '{sample_word}'")
    
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.pronunciation_history = []
        st.session_state.emotion_history = []
        st.session_state.session_stats = {
            'total_words_practiced': 0,
            'average_pronunciation_score': 0,
            'total_emotions_detected': 0,
            'session_start_time': time.time()
        }
        st.success("Session reset successfully!")
        st.rerun()

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎤 Pronunciation Practice", "😊 Emotion Detection", "📊 Analytics", "ℹ️ About"])

with tab1:
    st.header("🎤 Pronunciation Practice")
    
    # Input methods
    col1, col2 = st.columns([2, 1])
    
    with col1:
        word = st.text_input("Enter a word to practice:", placeholder="Type a word here...", key="practice_word")
    
    with col2:
        if st.button("🎵 Play Correct Pronunciation", use_container_width=True):
            if word:
                play_correct_pronunciation(word)
                st.success(f"Playing pronunciation of '{word}'")
            else:
                st.warning("Please enter a word first!")
    
    # Audio input methods
    st.subheader("📁 Upload Audio or Record Live")
    
    input_method = st.radio(
        "Choose input method:",
        ["Upload Audio File", "Record Live Audio"],
        horizontal=True
    )
    
    if input_method == "Upload Audio File":
        audio_file = st.file_uploader(
            "Upload your speech (WAV, MP3, M4A format)", 
            type=["wav", "mp3", "m4a"],
            help="Upload an audio file of you speaking the word"
        )
        
        if audio_file and word:
            # Display audio player
            st.audio(audio_file)
            
            # Show audio info
            duration = audio_processor.get_audio_duration(audio_file)
            st.info(f"Audio duration: {duration:.2f} seconds")
            
            # Transcribe and analyze
            with st.spinner("Transcribing audio..."):
                user_text = transcribe_audio(audio_file)
            
            if user_text:
                st.write(f"**You said:** {user_text}")
                
                # Analyze pronunciation
                with st.spinner("Analyzing pronunciation..."):
                    analysis = compare_pronunciation(user_text, word)
                
                if analysis:
                    # Update session stats
                    st.session_state.session_stats['total_words_practiced'] += 1
                    st.session_state.session_stats['average_pronunciation_score'] = (
                        (st.session_state.session_stats['average_pronunciation_score'] * 
                         (st.session_state.session_stats['total_words_practiced'] - 1) + 
                         analysis['score']) / st.session_state.session_stats['total_words_practiced']
                    )
                    
                    # Add to history
                    st.session_state.pronunciation_history.append({
                        'word': word,
                        'user_text': user_text,
                        'score': analysis['score'],
                        'timestamp': time.time()
                    })
    
    else:  # Record Live Audio
        col1, col2 = st.columns([1, 1])
        
        with col1:
            duration = st.slider("Recording duration (seconds)", 1, 10, 5)
        
        with col2:
            if st.button("🎤 Start Recording", use_container_width=True):
                if word:
                    with st.spinner("Recording..."):
                        user_text = record_and_transcribe(duration)
                    
                    if user_text:
                        st.write(f"**You said:** {user_text}")
                        
                        # Analyze pronunciation
                        with st.spinner("Analyzing pronunciation..."):
                            analysis = compare_pronunciation(user_text, word)
                        
                        if analysis:
                            # Update session stats
                            st.session_state.session_stats['total_words_practiced'] += 1
                            st.session_state.session_stats['average_pronunciation_score'] = (
                                (st.session_state.session_stats['average_pronunciation_score'] * 
                                 (st.session_state.session_stats['total_words_practiced'] - 1) + 
                                 analysis['score']) / st.session_state.session_stats['total_words_practiced']
                            )
                            
                            # Add to history
                            st.session_state.pronunciation_history.append({
                                'word': word,
                                'user_text': user_text,
                                'score': analysis['score'],
                                'timestamp': time.time()
                            })
                else:
                    st.warning("Please enter a word first!")

with tab2:
    st.header("😊 Emotion Detection")
    
    # Emotion detection methods
    emotion_method = st.radio(
        "Choose emotion detection method:",
        ["Upload Image", "Live Detection (Demo)", "Teachable Machine"],
        horizontal=True
    )
    
    if emotion_method == "Upload Image":
        uploaded_image = st.file_uploader(
            "Upload an image with a face",
            type=["jpg", "jpeg", "png"],
            help="Upload an image containing a face for emotion detection"
        )
        
        if uploaded_image:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            
            with col2:
                with st.spinner("Detecting emotions..."):
                    emotion_probs = detect_emotion_from_uploaded_image(uploaded_image)
                
                if emotion_probs:
                    # Display emotion probabilities
                    st.subheader("Emotion Analysis")
                    for emotion, prob in emotion_probs.items():
                        st.progress(prob, text=f"{emotion}: {prob:.2%}")
                    
                    # Get dominant emotion
                    dominant_emotion = max(emotion_probs, key=emotion_probs.get)
                    confidence = emotion_probs[dominant_emotion]
                    
                    st.success(f"**Dominant Emotion:** {dominant_emotion} ({confidence:.1%} confidence)")
                    
                    # Update session stats
                    st.session_state.session_stats['total_emotions_detected'] += 1
                    st.session_state.emotion_history.append({
                        'emotion_probs': emotion_probs,
                        'dominant_emotion': dominant_emotion,
                        'confidence': confidence,
                        'timestamp': time.time()
                    })
    
    elif emotion_method == "Live Detection (Demo)":
        st.info("This is a demo mode. In a real implementation, this would use your webcam.")
        
        if st.button("Detect Emotion (Demo)"):
            with st.spinner("Detecting emotions..."):
                emotion = detect_emotion()
            
            if emotion:
                st.success(f"**Detected emotion:** {emotion}")
                
                # Update session stats
                st.session_state.session_stats['total_emotions_detected'] += 1
                st.session_state.emotion_history.append({
                    'emotion_probs': {emotion: 1.0},
                    'dominant_emotion': emotion,
                    'confidence': 1.0,
                    'timestamp': time.time()
                })
    
    else:  # Teachable Machine
        st.subheader("Teachable Machine Integration")
        st.markdown("Use the webcam in your browser to detect emotions via Teachable Machine.")
        st.markdown("[Open Emotion Detector](backend/model.html)")
        
        # Display emotion analysis if available
        if st.session_state.emotion_history:
            latest_emotion = st.session_state.emotion_history[-1]
            st.info(f"Latest detected emotion: **{latest_emotion['dominant_emotion']}**")

with tab3:
    st.header("📊 Analytics & Insights")
    
    if not st.session_state.pronunciation_history and not st.session_state.emotion_history:
        st.info("No data available yet. Start practicing to see your analytics!")
    else:
        # Pronunciation analytics
        if st.session_state.pronunciation_history:
            st.subheader("🎤 Pronunciation Analytics")
            
            # Recent practice history
            st.write("**Recent Practice History:**")
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
            
            # Score distribution
            scores = [p['score'] for p in st.session_state.pronunciation_history]
            avg_score = np.mean(scores)
            max_score = np.max(scores)
            min_score = np.min(scores)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Score", f"{avg_score:.1f}%")
            with col2:
                st.metric("Best Score", f"{max_score:.1f}%")
            with col3:
                st.metric("Worst Score", f"{min_score:.1f}%")
        
        # Emotion analytics
        if st.session_state.emotion_history:
            st.subheader("😊 Emotion Analytics")
            
            # Emotion trend analysis
            emotion_analysis = get_emotion_analysis(st.session_state.emotion_history)
            
            st.write(f"**Dominant Emotion:** {emotion_analysis['dominant_emotion']}")
            st.write(f"**Confidence:** {emotion_analysis['confidence']:.1%}")
            st.write(f"**Trend:** {emotion_analysis['trend']}")
            
            # Recommendations
            if emotion_analysis['recommendations']:
                st.write("**Recommendations:**")
                for rec in emotion_analysis['recommendations']:
                    st.write(f"• {rec}")

with tab4:
    st.header("ℹ️ About SwarSense")
    
    st.markdown("""
    ## 🎤 SwarSense - Emotion-Aware Communication Coach
    
    SwarSense is a multimodal emotion-aware communication coach that helps you improve your 
    pronunciation and emotional expression during communication.
    
    ### ✨ Features
    
    - **🎤 Pronunciation Analysis**: Get detailed feedback on your pronunciation with phoneme comparison
    - **😊 Emotion Detection**: Analyze facial expressions to understand your emotional state
    - **📊 Analytics**: Track your progress over time with comprehensive analytics
    - **💡 Tips & Recommendations**: Receive personalized tips to improve your communication skills
    
    ### 🛠️ Technology Stack
    
    - **Frontend**: Streamlit
    - **Audio Processing**: SpeechRecognition, PyAudio
    - **Pronunciation**: Pronouncing library
    - **Emotion Detection**: OpenCV, Computer Vision
    - **Text-to-Speech**: Google Text-to-Speech
    
    ### 🚀 How to Use
    
    1. **Pronunciation Practice**: Enter a word and either upload an audio file or record live
    2. **Emotion Detection**: Upload an image or use the webcam integration
    3. **Analytics**: View your progress and get insights
    4. **Tips**: Follow the recommendations to improve your skills
    
    ### 📈 Tips for Better Results
    
    - Speak clearly and at a moderate pace
    - Ensure good lighting for emotion detection
    - Practice regularly to see improvement
    - Use headphones for better audio quality
    
    ### 🤝 Contributing
    
    This project is open source and contributions are welcome! Check out the 
    [GitHub repository](https://github.com/SaiMasram750/SwarSense) for more information.
    """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>Made with ❤️ for better communication</p>",
        unsafe_allow_html=True
    )
