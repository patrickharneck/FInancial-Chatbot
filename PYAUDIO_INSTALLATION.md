# PyAudio Installation Guide

## Issue
Error: `Could not find PyAudio; check installation`

This occurs because the `speech_recognition` library requires PyAudio to access your microphone.

---

## Quick Fix

### Windows
```bash
pip install PyAudio
```

If that doesn't work, try:
```bash
pip install pipwin
pipwin install PyAudio
```

### macOS
```bash
# Using Homebrew (install if needed: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)")
brew install portaudio
pip install PyAudio
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install portaudio19-dev
pip install PyAudio
```

### Linux (Fedora/RHEL)
```bash
sudo dnf install portaudio-devel
pip install PyAudio
```

---

## Verify Installation

```bash
python -c "import pyaudio; print('✅ PyAudio installed successfully')"
```

---

## If Installation Fails

### Option 1: Use Pre-built Wheel (Windows)
Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```bash
pip install PyAudio-0.2.13-cp310-cp310-win_amd64.whl
```

### Option 2: Use Conda (if you have Anaconda)
```bash
conda install -c conda-forge pyaudio
```

### Option 3: Alternative - Use WebRTC for Audio
If PyAudio continues to fail, you can use this alternative:
```bash
pip install webrtcvad
pip install sounddevice
```

Then update voice_processor.py to use sounddevice instead (advanced).

---

## After Installing PyAudio

1. Restart your terminal/IDE
2. Run the chatbot again:
   ```bash
   pip install -r requirements.txt
   streamlit run app/chatbot.py
   ```
3. Test voice input with the microphone button

---

## Troubleshooting

### Still Getting Error?
- **Check Python Version**: PyAudio requires Python 3.6+
  ```bash
  python --version
  ```

- **Check if pip is up to date**:
  ```bash
  pip install --upgrade pip
  ```

- **Try upgrading setuptools**:
  ```bash
  pip install --upgrade setuptools
  ```

- **Verify microphone access**: Check system settings to ensure your microphone is working

### Still No Microphone?
You can still use the chatbot with:
- ✅ Text input (typing)
- ✅ Audio file upload (already recorded audio files)
- ✅ Text-to-speech output (hearing responses)

Only microphone recording requires PyAudio.

---

## Contact

If installation problems persist:
1. Check your Python version (3.8+)
2. Verify pip is working: `pip --version`
3. Try in a fresh Python virtual environment
4. Check the [PyAudio documentation](http://people.csail.mit.edu/hubert/pyaudio/)

