# voice_processor.py
"""
Voice processing module for speech-to-text and text-to-speech functionality
Handles audio input from microphone, speech recognition, and voice output
"""

import io
import threading
from typing import Optional, Tuple
from pathlib import Path
import speech_recognition as sr
import pyttsx3
from config import Config


class SpeechRecognizer:
    """Handles speech-to-text conversion from audio input"""
    
    def __init__(self, language: str = 'en-US'):
        """
        Initialize speech recognizer
        
        Args:
            language: Language code (e.g., 'en-US', 'en-GB', 'ny' for Chichewa)
        """
        self.recognizer = sr.Recognizer()
        self.language = language
        
        # Try to initialize microphone, handle PyAudio errors gracefully
        try:
            self.microphone = sr.Microphone()
        except Exception as e:
            print(f"Warning: Microphone initialization failed: {e}")
            print("PyAudio may not be installed. Install with: pip install PyAudio")
            self.microphone = None
            self.microphone_error = str(e)
    
    def set_language(self, language: str) -> None:
        """
        Set recognition language
        
        Args:
            language: Language code
        """
        self.language = language
    
    def recognize_from_microphone(self, timeout: int = 10, phrase_time_limit: int = 15) -> Tuple[bool, str]:
        """
        Capture audio from microphone and convert to text
        
        Args:
            timeout: Seconds to wait for audio input
            phrase_time_limit: Maximum seconds for speech
            
        Returns:
            Tuple of (success: bool, text: str or error message)
        """
        if self.microphone is None:
            return False, "Microphone not available. Install PyAudio: pip install PyAudio"
        
        try:
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen to user
                audio_data = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio_data, language=self.language)
            return True, text
            
        except sr.UnknownValueError:
            return False, "Could not understand audio. Please speak clearly."
        except sr.RequestError as e:
            return False, f"Speech recognition error: {str(e)}"
        except OSError as e:
            if "PyAudio" in str(e) or "audio device" in str(e).lower():
                return False, "PyAudio not installed. Run: pip install PyAudio"
            return False, f"Audio device error: {str(e)}"
        except sr.WaitTimeoutError:
            return False, "No speech detected. Please try again."
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def recognize_from_audio_bytes(self, audio_bytes: bytes) -> Tuple[bool, str]:
        """
        Convert uploaded audio file to text
        
        Args:
            audio_bytes: Audio data as bytes
            
        Returns:
            Tuple of (success: bool, text: str or error message)
        """
        try:
            audio_data = sr.AudioData(
                audio_bytes,
                sample_rate=16000,
                sample_width=2
            )
            
            text = self.recognizer.recognize_google(audio_data, language=self.language)
            return True, text
            
        except sr.UnknownValueError:
            return False, "Could not understand audio content."
        except sr.RequestError as e:
            return False, f"Speech recognition failed: {str(e)}"
        except Exception as e:
            return False, f"Error processing audio: {str(e)}"


class TextToSpeech:
    """Handles text-to-speech conversion"""
    
    def __init__(self, voice_rate: int = 150, volume: float = 0.9):
        """
        Initialize text-to-speech engine
        
        Args:
            voice_rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        self.engine = pyttsx3.init()
        self.voice_rate = voice_rate
        self.volume = volume
        self._setup_engine()
    
    def _setup_engine(self) -> None:
        """Configure TTS engine settings"""
        self.engine.setProperty('rate', self.voice_rate)
        self.engine.setProperty('volume', self.volume)
    
    def set_voice(self, voice_index: int = 0) -> None:
        """
        Set voice by index
        
        Args:
            voice_index: Index of available voice (0=default, 1=alternative, etc.)
        """
        try:
            voices = self.engine.getProperty('voices')
            if 0 <= voice_index < len(voices):
                self.engine.setProperty('voice', voices[voice_index].id)
        except Exception as e:
            print(f"Error setting voice: {e}")
    
    def set_language(self, language: str) -> None:
        """
        Set TTS language by selecting appropriate voice
        
        Args:
            language: Language code ('en' for English, 'ny' for Chichewa, etc.)
        """
        # Note: pyttsx3 has limited language support. 
        # English voices are available on most systems
        # For other languages, we'll use the default English voice
        # A more advanced approach would use alternative TTS services
        try:
            voices = self.engine.getProperty('voices')
            
            # Prefer female voice for better clarity
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    return
            
            # Fallback to first available voice
            if voices:
                self.engine.setProperty('voice', voices[0].id)
        except Exception as e:
            print(f"Error setting language: {e}")
    
    def speak(self, text: str, wait: bool = True) -> None:
        """
        Convert text to speech and play audio
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to finish
        """
        try:
            self.engine.say(text)
            if wait:
                self.engine.runAndWait()
            else:
                self.engine.runAndWait()  # runAndWait is blocking, but we can use startLoop
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
    
    def speak_to_file(self, text: str, filepath: str) -> Tuple[bool, str]:
        """
        Convert text to speech and save to file
        
        Args:
            text: Text to speak
            filepath: Path to save audio file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            self.engine.save_to_file(text, filepath)
            self.engine.runAndWait()
            return True, f"Audio saved to {filepath}"
        except Exception as e:
            return False, f"Error saving audio: {str(e)}"
    
    def get_available_voices(self) -> list:
        """
        Get list of available voices on system
        
        Returns:
            List of voice information dictionaries
        """
        try:
            voices = self.engine.getProperty('voices')
            return [
                {
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages if hasattr(voice, 'languages') else []
                }
                for voice in voices
            ]
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []


class VoiceProcessor:
    """Main processor combining speech recognition and TTS"""
    
    def __init__(self, enable_tts: bool = True):
        """
        Initialize voice processor
        
        Args:
            enable_tts: Whether to enable text-to-speech
        """
        self.recognizer = SpeechRecognizer()
        self.tts = TextToSpeech() if enable_tts else None
        self.current_language = 'en-US'
        self.enable_tts = enable_tts
    
    def set_language(self, language_code: str) -> None:
        """
        Set processing language
        
        Args:
            language_code: Language code ('en-US' for English, 'ny' for Chichewa)
        """
        self.current_language = language_code
        self.recognizer.set_language(language_code)
        if self.tts:
            self.tts.set_language(language_code)
    
    def process_voice_input(self, timeout: int = 10) -> dict:
        """
        Process voice input from microphone
        
        Args:
            timeout: Seconds to wait for input
            
        Returns:
            Dictionary with:
            - 'success': bool
            - 'text': recognized text
            - 'error': error message (if any)
            - 'language': detected language
        """
        success, text = self.recognizer.recognize_from_microphone(timeout=timeout)
        
        return {
            'success': success,
            'text': text,
            'error': None if success else text,
            'language': self.current_language,
            'type': 'voice'
        }
    
    def process_uploaded_audio(self, audio_file_path: str) -> dict:
        """
        Process uploaded audio file
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Dictionary with recognition results
        """
        try:
            with open(audio_file_path, 'rb') as f:
                audio_bytes = f.read()
            
            success, text = self.recognizer.recognize_from_audio_bytes(audio_bytes)
            
            return {
                'success': success,
                'text': text,
                'error': None if success else text,
                'language': self.current_language,
                'type': 'uploaded_audio',
                'filepath': audio_file_path
            }
        except Exception as e:
            return {
                'success': False,
                'text': '',
                'error': f"Error reading audio file: {str(e)}",
                'language': self.current_language,
                'type': 'uploaded_audio'
            }
    
    def speak_response(self, text: str, wait: bool = True) -> bool:
        """
        Speak the chatbot response
        
        Args:
            text: Response text to speak
            wait: Whether to wait for speech to finish
            
        Returns:
            True if successful, False otherwise
        """
        if not self.tts or not self.enable_tts:
            return False
        
        try:
            self.tts.speak(text, wait=wait)
            return True
        except Exception as e:
            print(f"Error speaking response: {e}")
            return False
    
    def speak_response_to_file(self, text: str, filepath: str) -> bool:
        """
        Save response as audio file
        
        Args:
            text: Response text
            filepath: Path to save audio
            
        Returns:
            True if successful
        """
        if not self.tts:
            return False
        
        success, _ = self.tts.speak_to_file(text, filepath)
        return success
    
    def get_system_info(self) -> dict:
        """
        Get voice system information
        
        Returns:
            Dictionary with voice system details
        """
        voices = self.tts.get_available_voices() if self.tts else []
        
        return {
            'speech_recognition_enabled': True,
            'tts_enabled': self.enable_tts,
            'current_language': self.current_language,
            'available_voices': len(voices),
            'voices': voices
        }
