# Voice Features - Code Structure Reference

## Project Structure After Updates

```
Fin-Chat/
├── app/
│   ├── chatbot.py                    [MODIFIED] - Added voice UI
│   ├── chatbot_core.py               [unchanged]
│   ├── config.py                     [MODIFIED] - Added voice config
│   ├── evaluation.py                 [unchanged]
│   ├── fallback_responses.py          [unchanged]
│   ├── language_utils.py              [unchanged]
│   ├── llm_client.py                  [unchanged]
│   ├── prompt_builder.py              [unchanged]
│   ├── rag_retriever.py               [unchanged]
│   ├── voice_processor.py             [NEW] ⭐ Voice processing
│   ├── audio_utils.py                 [NEW] ⭐ Audio utilities
│   └── __pycache__/
│
├── VOICE_FEATURES_IMPLEMENTATION.md   [NEW] - Detailed documentation
├── QUICK_VOICE_SETUP.md               [NEW] - Quick start guide
├── requirements.txt                   [MODIFIED] - Added dependencies
└── ... (other files unchanged)
```

---

## Voice Module Architecture

### voice_processor.py
```
VoiceProcessor (Main Class)
├── SpeechRecognizer
│   ├── recognize_from_microphone()     → Records and converts speech to text
│   ├── recognize_from_audio_bytes()    → Processes uploaded audio
│   └── set_language()                   → Configure recognition language
│
├── TextToSpeech
│   ├── speak()                         → Play text as audio
│   ├── speak_to_file()                 → Save text as audio file
│   ├── set_voice()                     → Select voice
│   ├── set_language()                  → Configure TTS language
│   └── get_available_voices()          → List system voices
│
└── Methods
    ├── process_voice_input()           → Record from microphone
    ├── process_uploaded_audio()        → Process uploaded files
    ├── speak_response()                → Speak chatbot response
    └── get_system_info()               → System information
```

### audio_utils.py
```
AudioHandler (Static Methods)
├── validate_audio_file()               → Check format and size
├── get_audio_duration()                → Extract duration
├── convert_to_wav()                    → Format conversion
├── trim_audio_silence()                → Remove silence
├── normalize_audio()                   → Normalize levels
└── estimate_speech_quality()           → Quality metrics

StreamlitAudioHelper (Static Methods)
├── save_uploaded_audio()               → Save uploaded file
├── create_audio_player_html()          → Generate HTML player
└── format_audio_info()                 → Display metadata
```

---

## Configuration Structure (config.py)

```python
# Voice Features (NEW)
✓ ENABLE_VOICE_INPUT                   # Main feature toggle
✓ ENABLE_TEXT_TO_SPEECH                # TTS toggle

# Speech Recognition (NEW)
✓ SPEECH_RECOGNITION_LANGUAGE          # Default: 'en-US'
✓ SPEECH_RECOGNITION_TIMEOUT           # Default: 10 seconds
✓ SPEECH_RECOGNITION_PHRASE_LIMIT      # Default: 15 seconds

# Language Support (NEW)
✓ VOICE_LANGUAGES = {
    'en-US': 'English (US)',
    'en-GB': 'English (UK)',
    'ny': 'Chichewa (Malawi)'
  }

# Text-to-Speech Settings (NEW)
✓ TTS_VOICE_RATE                       # Default: 150 WPM
✓ TTS_VOLUME                           # Default: 0.9 (0.0-1.0)
✓ TTS_SAVE_RESPONSES                   # Default: False
✓ TTS_TEMP_DIR                         # Directory for audio files

# Audio Processing (NEW)
✓ AUDIO_SAMPLE_RATE                    # Default: 16000 Hz
✓ AUDIO_CHANNELS                       # Default: 1 (mono)
✓ AUDIO_SAMPLE_WIDTH                   # Default: 2 (16-bit)
✓ AUDIO_MAX_FILE_SIZE                  # Default: 100 MB
✓ AUDIO_FORMAT                         # Default: 'wav'

# Feature Flags (NEW)
✓ ALLOW_AUDIO_FILE_UPLOAD              # Default: True
✓ SHOW_AUDIO_QUALITY_METRICS           # Default: False
✓ VOICE_INPUT_ENABLED_BY_DEFAULT       # Default: True
```

---

## Chatbot.py - UI Components Added

### 1. Sidebar Voice Settings Panel
```python
Location: show_chatbot_page() → sidebar

Components:
├── Checkbox: Enable Voice Input
├── Selectbox: Voice Input Language
├── Checkbox: Enable Text-to-Speech
├── Slider: Speech Speed (50-300 WPM)
├── Slider: Speaker Volume (0.0-1.0)
└── Checkbox: Allow Audio File Upload
```

### 2. Voice Input Section (Below Chat History)
```python
Location: show_chatbot_page() → main area

Components:
├── Button: 🎙️ Record Audio
├── Button: 📁 Upload Audio
└── Button: ⏹️ Cancel

Sub-interfaces:
├── Recording Interface
│   ├── Info message
│   └── START RECORDING button
│
└── Upload Interface
    ├── File uploader widget
    └── Real-time recognition feedback
```

### 3. Text-to-Speech Output Section
```python
Location: show_chatbot_page() → response display

Components:
├── Button: 🔊 Speak Response
└── Button: 💾 Save as Audio File

Features:
├── Real-time TTS feedback
├── Error handling
└── Success notifications
```

### 4. Session State Variables (NEW)
```python
st.session_state variables added:
├── 'voice_input'        # Current voice input text
├── 'show_recording'     # Recording interface visibility
├── 'show_upload'        # Upload interface visibility
└── 'enable_voice'       # Voice features enabled flag
```

---

## Dependencies Added to requirements.txt

```
# Speech Recognition
speech-recognition==3.10.1
SpeechRecognition==3.10.1

# Text-to-Speech
pyttsx3==2.90

# Audio Processing
librosa==0.10.1
```

---

## Data Flow Diagrams

### Voice Input Flow
```
User clicks "Record Audio"
    ↓
VoiceProcessor.recognize_from_microphone()
    ↓
Google Speech Recognition API
    ↓
Recognized text returned
    ↓
Display in chat as user message
    ↓
Process through chatbot_core
    ↓
Generate response
```

### Audio File Upload Flow
```
User clicks "Upload Audio"
    ↓
File uploader widget
    ↓
AudioHandler.validate_audio_file()
    ↓
StreamlitAudioHelper.save_uploaded_audio()
    ↓
VoiceProcessor.process_uploaded_audio()
    ↓
Google Speech Recognition API
    ↓
Recognized text returned
    ↓
Same as voice input flow above
```

### Text-to-Speech Flow
```
Chatbot generates response
    ↓
User clicks "Speak Response"
    ↓
VoiceProcessor.speak_response()
    ↓
pyttsx3 TTS engine
    ↓
Audio output via speakers
    ↓
Success notification displayed
```

### Audio File Save Flow
```
User clicks "Save as Audio"
    ↓
Create temp audio directory
    ↓
VoiceProcessor.speak_response_to_file()
    ↓
pyttsx3 renders to WAV file
    ↓
File saved in temp_audio/
    ↓
Success notification with file info
```

---

## Key Integration Points

### 1. chatbot.py → voice_processor.py
```python
# In voice input section
voice_processor = VoiceProcessor(enable_tts=False)
voice_processor.set_language(language_code)
result = voice_processor.process_voice_input(timeout=10)
```

### 2. chatbot.py → audio_utils.py
```python
# In audio upload section
file_path = StreamlitAudioHelper.save_uploaded_audio(uploaded_file)
is_valid, msg = AudioHandler.validate_audio_file(file_path)
duration = AudioHandler.get_audio_duration(file_path)
```

### 3. chatbot.py → config.py
```python
# Voice settings
st.session_state.enable_voice = Config.VOICE_INPUT_ENABLED_BY_DEFAULT
voice_language = st.selectbox(
    "Voice Input Language",
    options=list(Config.VOICE_LANGUAGES.keys()),
    format_func=lambda x: Config.VOICE_LANGUAGES[x]
)
```

---

## Error Handling Structure

```python
try:
    # Voice operation (record, upload, TTS)
    result = voice_processor.process_voice_input()
    
    if result['success']:
        st.success("✅ Operation successful")
    else:
        st.error(f"❌ {result['error']}")
        
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
```

---

## Testing Entry Points

### Manual Testing
```
1. Settings → Enable Voice Input → Save
2. Select language from dropdown
3. Click "🎙️ Record Audio"
4. Click "🔴 START RECORDING"
5. Speak test phrase
6. Verify text appears in chat
7. Enable "Text-to-Speech"
8. Click "🔊 Speak Response"
9. Verify audio plays
```

### Unit Testing (For Developers)
```python
# Test SpeechRecognizer
from app.voice_processor import SpeechRecognizer
sr = SpeechRecognizer('en-US')
success, text = sr.recognize_from_microphone(timeout=5)

# Test TextToSpeech
from app.voice_processor import TextToSpeech
tts = TextToSpeech()
tts.speak("Test message")

# Test AudioHandler
from app.audio_utils import AudioHandler
is_valid, msg = AudioHandler.validate_audio_file('test.wav')
quality = AudioHandler.estimate_speech_quality(audio_data, sample_rate)
```

---

## Performance Considerations

- **Microphone Recording**: ~2-15 seconds per query
- **Speech Recognition**: ~2-5 seconds via Google API
- **Text-to-Speech**: ~1-3 seconds for average response
- **File Upload**: Depends on file size (max 100MB)
- **Memory Usage**: ~50-100MB for libraries

---

## Browser Compatibility

✅ Chrome/Chromium - Full support
✅ Firefox - Full support
✅ Safari - Full support (iOS may require permission)
✅ Edge - Full support

---

## Known Limitations

1. **Offline Speech Recognition**: Requires internet (Google API)
2. **TTS Language Support**: Limited to system voices
3. **Chichewa Voice**: May use English voice (system dependent)
4. **Audio Format Conversion**: Requires ffmpeg for some formats
5. **Real-time Processing**: Network latency affects responsiveness

---

## Future Enhancement Hooks

```python
# In config.py - Ready for future features
ALTERNATIVE_SPEECH_SERVICES = ['azure', 'aws']  # Not yet implemented
OFFLINE_SPEECH_RECOGNITION = False              # Not yet implemented
VOICE_PROFILES = {}                             # Not yet implemented
CONVERSATION_HISTORY_AUDIO = False              # Not yet implemented
VOICE_EMOTIONS = False                          # Not yet implemented
```

