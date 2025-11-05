# 🎤 SwarSense - Emotion-Aware Communication Coach

SwarSense is a multimodal emotion-aware communication coach that analyzes user pronunciation and facial expressions from video/audio input and provides feedback on confidence, confusion, or fear.

## ✨ Features

- **🎤 Pronunciation Analysis**: Get detailed feedback on your pronunciation with phoneme comparison
- **😊 Emotion Detection**: Analyze facial expressions to understand your emotional state
- **📊 Analytics**: Track your progress over time with comprehensive analytics
- **💡 Tips & Recommendations**: Receive personalized tips to improve your communication skills
- **🎵 Audio Playback**: Listen to correct pronunciations
- **📱 Responsive UI**: Beautiful, modern interface built with Streamlit

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Audio Processing**: SpeechRecognition, PyAudio
- **Pronunciation**: Pronouncing library
- **Emotion Detection**: OpenCV, Computer Vision
- **Text-to-Speech**: Google Text-to-Speech
- **Machine Learning**: TensorFlow (for emotion detection)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/SaiMasram750/SwarSense.git
cd SwarSense
```

2. Install dependencies:
```bash
pip install -r requirement.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 📖 Usage

### Pronunciation Practice
1. Enter a word you want to practice
2. Click "Play Correct Pronunciation" to hear the correct pronunciation
3. Upload an audio file or record live audio
4. Get detailed feedback on your pronunciation with phoneme comparison
5. View tips for improvement

### Emotion Detection
1. Upload an image with a face
2. Get emotion analysis with confidence scores
3. View recommendations based on detected emotions
4. Track emotional trends over time

### Analytics
1. View your pronunciation practice history
2. Track your progress with score analytics
3. Monitor emotional expression patterns
4. Get personalized recommendations

## 🏗️ Project Structure

```
SwarSense/
├── app.py                 # Main Streamlit application
├── backend/
│   ├── process_audio.py  # Audio processing and transcription
│   ├── phoneme_check.py  # Pronunciation analysis
│   ├── emotion_detect.py # Emotion detection
│   └── model.html        # Teachable Machine integration
├── requirement.txt       # Python dependencies
└── README.md            # Project documentation
```

## 🔧 Backend Modules

### Audio Processing (`process_audio.py`)
- Handles audio transcription using Google Speech Recognition
- Supports multiple audio formats (WAV, MP3, M4A)
- Live audio recording capabilities
- Error handling and validation

### Pronunciation Analysis (`phoneme_check.py`)
- Phoneme comparison using the Pronouncing library
- Pronunciation scoring algorithm
- Detailed feedback and tips
- Audio playback for correct pronunciation

### Emotion Detection (`emotion_detect.py`)
- Facial emotion detection using OpenCV
- Emotion trend analysis
- Personalized recommendations
- Confidence scoring

## 📊 Features for Hackathon Demo

- **Real-time Analysis**: Instant feedback on pronunciation and emotions
- **Progress Tracking**: Comprehensive analytics and session statistics
- **User-Friendly Interface**: Modern, responsive design
- **Multiple Input Methods**: File upload, live recording, image upload
- **Personalized Tips**: Context-aware recommendations
- **Session Management**: Track progress across multiple sessions

## 🎯 Demo Scenarios

1. **Pronunciation Practice**: Practice difficult words with instant feedback
2. **Emotion Awareness**: Understand your emotional state during communication
3. **Progress Tracking**: Monitor improvement over time
4. **Interactive Learning**: Engaging interface with tips and recommendations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- SpeechRecognition library for audio processing
- Pronouncing library for phoneme analysis
- OpenCV for computer vision
- Streamlit for the web interface
- Google Text-to-Speech for audio generation

## 📞 Contact

For questions or support, please open an issue on GitHub or contact the maintainers.

---

Made with ❤️ for better communication