# Voice Features - Installation & Testing Guide

## 📋 What Was Changed

### Files Created (2)
✅ `app/voice_processor.py` - Core voice processing module
✅ `app/audio_utils.py` - Audio utilities and helpers

### Files Modified (3)
✅ `app/config.py` - Added voice configuration options
✅ `app/chatbot.py` - Added voice UI components
✅ `requirements.txt` - Added voice dependencies

### Documentation Created (3)
✅ `VOICE_FEATURES_IMPLEMENTATION.md` - Complete documentation
✅ `QUICK_VOICE_SETUP.md` - Quick start guide
✅ `VOICE_CODE_REFERENCE.md` - Code structure reference

---

## 🚀 Getting Started

### Step 1: Install Dependencies
```bash
# Navigate to project directory
cd e:\Fin-Chat

# Install new voice packages
pip install -r requirements.txt
```

Or install just the new packages:
```bash
pip install speech-recognition pyttsx3 librosa
```

**Installed Packages:**
- `SpeechRecognition` (3.10.1) - Google Speech Recognition
- `pyttsx3` (2.90) - Text-to-Speech Engine
- `librosa` (0.10.1) - Audio Processing

---

### Step 2: Verify Installation
```bash
# Test imports in Python
python -c "import speech_recognition; import pyttsx3; print('✅ Voice packages installed successfully')"
```

---

### Step 3: Run the Chatbot
```bash
# Start Streamlit app
streamlit run app/chatbot.py
```

---

### Step 4: Test Voice Features
In the Streamlit app:

1. **Sidebar Settings** → Enable Voice Input ✓
2. Select Language (English US/GB or Chichewa)
3. Enable Text-to-Speech ✓
4. **Test Input**: Click "🎙️ Record Audio" → Click "START RECORDING" → Speak
5. **Test Output**: Ask a question → Click "🔊 Speak Response" → Listen
6. **Test Audio Upload**: Click "📁 Upload Audio" → Select audio file

---

## ✨ New Features Available

### Voice Input Options
- **🎙️ Record from Microphone**: Capture live speech
- **📁 Upload Audio File**: Use pre-recorded audio (WAV, MP3, M4A, OGG, FLAC)
- **Automatic Speech Recognition**: Google Speech Recognition API

### Voice Output Options
- **🔊 Speak Response**: Hear chatbot's answer aloud
- **💾 Save as Audio**: Download response as WAV file
- **Speed Control**: Adjust speech rate (50-300 WPM)
- **Volume Control**: Adjust speaker volume (0.0-1.0)

### Multi-Language Support
- English (US & UK)
- Chichewa (Malawi)
- Extensible for more languages

---

## 🎤 User Interface Changes

### New Sidebar Settings Section
```
⚙️ Settings
├── Use Groq LLM
├── Confidence threshold
├── Response Settings
│
└── 🎤 Voice Input Settings [NEW]
    ├── ☑ Enable Voice Input
    ├── Voice Input Language ▼
    ├── ☑ Enable Text-to-Speech
    ├── Speech Speed ▬▬▬
    ├── Speaker Volume ▬▬▬
    └── ☑ Allow Audio File Upload
```

### New Chat Interface Section
```
💬 Chat / Lankhulani

[Chat history displays here]

---
🎤 Voice Input [NEW]
[🎙️ Record Audio] [📁 Upload Audio] [⏹️ Cancel]

Ask about money... [text input box]

---
Assistant response here

🔊 Speak Response | 💾 Save
ℹ️ Response Details
```

---

## 🔧 Configuration Reference

All settings in `app/config.py`:

```python
# Main toggles
ENABLE_VOICE_INPUT = True                    # Enable/disable all voice
ENABLE_TEXT_TO_SPEECH = True                 # Enable/disable TTS

# Languages
VOICE_LANGUAGES = {
    'en-US': 'English (US)',
    'en-GB': 'English (UK)',
    'ny': 'Chichewa (Malawi)'
}

# Speech recognition
SPEECH_RECOGNITION_TIMEOUT = 10              # Seconds to wait for audio
SPEECH_RECOGNITION_LANGUAGE = 'en-US'        # Default language

# Text-to-speech
TTS_VOICE_RATE = 150                        # Words per minute
TTS_VOLUME = 0.9                            # 0.0 to 1.0

# Audio files
ALLOW_AUDIO_FILE_UPLOAD = True              # Allow file uploads
AUDIO_MAX_FILE_SIZE = 100                   # MB
AUDIO_FORMAT = 'wav'                        # Audio format
```

---

## 🧪 Testing Checklist

### Microphone Input Test
- [ ] Click "🎙️ Record Audio"
- [ ] Speak a test phrase
- [ ] Text appears in chat
- [ ] Response is generated

### File Upload Test
- [ ] Click "📁 Upload Audio"
- [ ] Select an audio file
- [ ] File is recognized and converted
- [ ] Response appears in chat

### Text-to-Speech Test
- [ ] Enable "Text-to-Speech" in settings
- [ ] Ask a question
- [ ] Click "🔊 Speak Response"
- [ ] Hear the response aloud

### Volume & Speed Test
- [ ] Adjust "Speech Speed" slider
- [ ] Adjust "Speaker Volume" slider
- [ ] Verify changes take effect

### Language Switching Test
- [ ] Change "Voice Input Language" to English (UK)
- [ ] Record/upload test audio
- [ ] Switch to Chichewa
- [ ] Record/upload different test audio

### Audio Save Test
- [ ] Click "💾" button next to "Speak Response"
- [ ] Wait for success message
- [ ] Audio file saved to `temp_audio/` folder

---

## 🐛 Troubleshooting

### Issue: "No module named 'speech_recognition'"
```bash
# Solution: Install the package
pip install SpeechRecognition
```

### Issue: "No module named 'pyttsx3'"
```bash
# Solution: Install the package
pip install pyttsx3
```

### Issue: Microphone not detected
- Check system audio settings
- Ensure microphone is connected and enabled
- Test microphone in system settings first
- Restart Streamlit app

### Issue: Speech not recognized
- Speak more clearly and slowly
- Ensure internet connection (Google API)
- Check language setting matches your speech
- Be closer to microphone, reduce background noise

### Issue: Text-to-speech not working
- Verify speakers are connected and unmuted
- Check volume slider (not at 0)
- Ensure "Enable Text-to-Speech" is checked
- Test speakers in system settings first

### Issue: Audio file upload fails
- Check file format (WAV, MP3, M4A, OGG, FLAC)
- Verify file size < 100MB
- Ensure file is valid audio format

### Issue: Import errors in Python
```bash
# Solution: Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📊 System Requirements

### Hardware
- **Microphone**: For voice input (USB or built-in)
- **Speakers/Headphones**: For text-to-speech output
- **Internet**: For Google Speech Recognition API

### Software
- **Python**: 3.8+
- **Streamlit**: 1.50.0+
- **OS**: Windows, macOS, or Linux

### Network
- **Internet Connection**: Required for:
  - Google Speech Recognition API
  - Initial package downloads

---

## 📁 Project Structure After Setup

```
Fin-Chat/
├── app/
│   ├── chatbot.py                    (with voice UI)
│   ├── chatbot_core.py
│   ├── config.py                     (with voice config)
│   ├── evaluation.py
│   ├── fallback_responses.py
│   ├── language_utils.py
│   ├── llm_client.py
│   ├── prompt_builder.py
│   ├── rag_retriever.py
│   ├── voice_processor.py            (NEW)
│   ├── audio_utils.py                (NEW)
│   └── __pycache__/
│
├── data/
│   ├── financial_faqs_chichewa_revised.csv
│   ├── financial_faqs_chichewa.csv
│   ├── Financial_Literacy_FAQs_500.csv
│   ├── Financial_Literacy_FAQs_Cleaned.csv
│   └── sources.csv
│
├── models/
│   ├── corpus_dual_complete.json
│   ├── faiss_dual_index.idx
│   ├── e5_embedder/
│   └── ...
│
├── temp_audio/                       (NEW - Created at runtime)
│   └── response_*.wav
│
├── VOICE_FEATURES_IMPLEMENTATION.md  (NEW)
├── QUICK_VOICE_SETUP.md              (NEW)
├── VOICE_CODE_REFERENCE.md           (NEW)
├── requirements.txt                  (UPDATED)
├── README.md
├── Design.md
├── Manual.md
└── ...
```

---

## 🎯 Next Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test Microphone**
   - Check microphone works in system settings
   - Test with another audio app

3. **Run Chatbot**
   ```bash
   streamlit run app/chatbot.py
   ```

4. **Enable Voice Features**
   - In Settings sidebar, check "Enable Voice Input"
   - Test recording, upload, and TTS

5. **Customize Settings** (if needed)
   - Edit `app/config.py` for preferences
   - Adjust language support
   - Change audio parameters

6. **Use Voice Features**
   - Start asking questions via microphone
   - Listen to responses via speaker
   - Save important responses as audio files

---

## 💡 Tips & Best Practices

### For Best Voice Recognition
- Minimize background noise
- Speak clearly and at normal pace
- Use microphone 15-30cm away
- Ensure stable internet connection

### For Best Text-to-Speech
- Adjust speech speed to your preference
- Keep volume between 0.5-1.0
- Use in quiet environment to hear clearly
- Test on different devices

### For Audio Files
- Use clear, quality audio recordings
- Avoid heavily compressed formats
- Keep files < 100MB
- Use supported formats (WAV, MP3, M4A, OGG, FLAC)

---

## 🔗 Related Documentation

- [VOICE_FEATURES_IMPLEMENTATION.md](VOICE_FEATURES_IMPLEMENTATION.md) - Complete technical documentation
- [QUICK_VOICE_SETUP.md](QUICK_VOICE_SETUP.md) - Quick reference guide
- [VOICE_CODE_REFERENCE.md](VOICE_CODE_REFERENCE.md) - Code structure and architecture

---

## ❓ FAQ

**Q: Do I need an API key for voice features?**
A: No API key required. Speech Recognition uses Google's free API. Text-to-speech uses local pyttsx3 engine.

**Q: Can I use voice offline?**
A: Not yet. Speech recognition requires internet for Google API. Text-to-speech works offline.

**Q: What languages are supported?**
A: English (US/UK) and Chichewa by default. More can be added in config.

**Q: Can I change the voice (male/female)?**
A: Yes, through `TextToSpeech.set_voice()` method. Available voices depend on system.

**Q: How do I add more languages?**
A: Edit `Config.VOICE_LANGUAGES` in `app/config.py` and add language codes.

---

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review error messages in Streamlit console
3. Check system audio settings
4. Verify internet connection
5. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

---

**Version**: 1.0
**Date**: February 4, 2026
**Status**: Ready for Production ✅

