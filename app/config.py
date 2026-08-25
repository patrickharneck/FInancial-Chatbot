# config.py
"""
Configuration management for the RAG Financial Chatbot
Handles all paths, constants, and system configuration
"""

import os
from pathlib import Path

try:
    import streamlit as st
except ImportError:
    st = None

class Config:
    """Central configuration class"""
    
    # Path Configuration - CORRECTED FOR YOUR STRUCTURE
    SCRIPT_DIR = Path(__file__).parent.resolve()
    PROJECT_ROOT = SCRIPT_DIR.parent.parent
    MODELS_DIR = PROJECT_ROOT / "models" 
    DATA_DIR = PROJECT_ROOT / "data"    
    
    # Model Configuration
    EMBEDDING_MODEL = 'intfloat/multilingual-e5-base'
    RERANKER_MODEL_PATH = MODELS_DIR / 'distilbert-reranker-rag-trainer'# not used in this version
    
    # Alternative fix - convert absolute strings to Path objects
    FAISS_INDEX_PATH = Path("E:/Fin-Chat/models/faiss_dual_index.idx")
    CORPUS_JSON_PATH = Path("E:/Fin-Chat/models/corpus_dual_complete.json")
  
    # RAG Configuration
    DEFAULT_TOP_K = 5
    DEFAULT_CONFIDENCE_THRESHOLD = 0.55
    SIMILARITY_THRESHOLD = 0.55
    
    # LLM Configuration
    GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
    GROQ_MODELS = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant']
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 3000
    DEFAULT_TIMEOUT = 45
    
    # Response Length Configuration
    MIN_RESPONSE_LENGTH = 80
    MAX_RESPONSE_LENGTH = 400
    DEFAULT_RESPONSE_LENGTH = 150
    
    # Language Detection
    CHICHEWA_KEYWORDS = {
        'savings': ['kusunga', 'ndalama zosungidwa', 'sunga', 'investimenti'],
        'budget': ['bajeti', 'ndondomeko ya ndalama', 'kukonzekera'],
        'loan': ['ngongole', 'kubwereka', 'kubweza', 'kulipira'],
        'fraud': ['chinyengo', 'tetezani', 'opeza', 'chitetezo'],
        'mobile_money': ['ndalama zam\'manja', 'mpamba', 'airtel money', 'tnm mpamba'],
        'bank': ['banki', 'akaunti', 'kusungamo ndalama'],
        'interest': ['ndalama zochuluka', 'mtengo', 'phindu'],
        'security': ['chitetezo', 'teteza', 'kuteteza'],
        'investment': ['kusunga ndalama', 'kuika ndalama'],
        'business': ['bizinesi', 'malonda']
    }
    
    # Real-time Translation Configuration
    ENABLE_REALTIME_TRANSLATION = True
    TRANSLATION_TIMEOUT = 30  # seconds
    
    # Financial glossary for better translation accuracy
    FINANCIAL_GLOSSARY = {
        "bank": "banki",
        "account": "akaunti",
        "savings": "ndalama zosungidwa",
        "budget": "bajeti",
        "loan": "ngongole",
        "money": "ndalama",
        "interest": "chiwongoladzanja",
        "fraud": "chinyengo",
        "mobile money": "ndalama zam'manja",
        "PIN": "nambala yachinsinsi",
        "business": "bizinesi",
        "investment": "ndalama zogulitsa",
        "save": "kusunga",
        "borrow": "kubwereka",
        "pay": "kulipira",
        "security": "chitetezo"
    }
    
    # Voice Input Configuration
    ENABLE_VOICE_INPUT = True
    ENABLE_TEXT_TO_SPEECH = True
    
    # Speech recognition settings
    SPEECH_RECOGNITION_LANGUAGE = 'en-US'  # Default language for speech recognition
    SPEECH_RECOGNITION_TIMEOUT = 10  # Seconds to wait for audio input
    SPEECH_RECOGNITION_PHRASE_LIMIT = 15  # Maximum seconds for speech
    
    # Supported languages for voice input
    VOICE_LANGUAGES = {
        'en-US': 'English (US)',
        'en-GB': 'English (UK)',
        'ny': 'Chichewa (Malawi)'
    }
    
    # Text-to-Speech settings
    TTS_VOICE_RATE = 150  # Words per minute
    TTS_VOLUME = 0.9  # 0.0 to 1.0
    TTS_SAVE_RESPONSES = False  # Save responses as audio files
    TTS_TEMP_DIR = PROJECT_ROOT / "temp_audio"  # Directory for temporary audio files
    
    # Audio processing settings
    AUDIO_SAMPLE_RATE = 16000  # Hz
    AUDIO_CHANNELS = 1  # Mono
    AUDIO_SAMPLE_WIDTH = 2  # 16-bit
    AUDIO_MAX_FILE_SIZE = 100  # MB
    AUDIO_FORMAT = 'wav'
    
    # Feature flags
    ALLOW_AUDIO_FILE_UPLOAD = True
    SHOW_AUDIO_QUALITY_METRICS = False
    VOICE_INPUT_ENABLED_BY_DEFAULT = True
    
    # Feedback System Configuration
    FEEDBACK_STORAGE_PATH = PROJECT_ROOT / "data" / "feedback.json"
    
    @classmethod
    def get_groq_api_key(cls):
        """Get the Groq API key from the environment or Streamlit secrets."""
        api_key = os.environ.get('GROQ_API_KEY')
        if api_key:
            return api_key.strip()

        if st is not None:
            try:
                api_key = st.secrets.get('GROQ_API_KEY')
                if api_key:
                    return str(api_key).strip()
            except Exception:
                pass

        return None
    
    @classmethod
    def validate_paths(cls):
        """Validate that required paths exist"""
        return {
            'models_dir': cls.MODELS_DIR.exists(),
            'data_dir': cls.DATA_DIR.exists(),
            'faiss_index': cls.FAISS_INDEX_PATH.exists(),
            'corpus_json': cls.CORPUS_JSON_PATH.exists(),
        }