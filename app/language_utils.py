# language_utils.py
"""
Language detection and processing utilities
Handles Chichewa/English detection, query enhancement, and real-time translation
"""

import re
from config import Config
import signal

try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    print("Warning: deep_translator not installed. Install with: pip install deep-translator")


class LanguageDetector:
    """Detect and process languages (English and Chichewa)"""
    
    def __init__(self):
        self.chichewa_keywords = Config.CHICHEWA_KEYWORDS
        
        # Chichewa indicators with weights
        self.chichewa_indicators = {
            # Question words (high weight)
            'kodi': 3, 'bwanji': 3, 'chifukwa': 3, 'liti': 3,
            # Common verbs/words (medium weight)
            'ndikufuna': 2, 'ndili': 2, 'ndiri': 2, 'mukhala': 2,
            'pepani': 2, 'chonde': 2, 'zikomo': 2,
            # Financial terms (medium weight)
            'ndalama': 2, 'ngongole': 2, 'bajeti': 2, 'chinyengo': 2,
            'mtengo': 2, 'kusunga': 2, 'bizinesi': 2, 'malonda': 2,
            # Common particles (low weight)
            'ndi': 1, 'pa': 1, 'ku': 1, 'wa': 1, 'za': 1,
            'mu': 1, 'la': 1, 'ya': 1
        }
        
        # English indicators
        self.english_indicators = [
            'the', 'is', 'are', 'what', 'how', 'can', 'will',
            'please', 'help', 'need', 'want', 'account', 'loan'
        ]
    
    def detect_language(self, text: str) -> str:
        """
        Detect if text is Chichewa (ny) or English (en)
        
        Args:
            text: Input text to analyze
            
        Returns:
            Language code: 'ny' for Chichewa, 'en' for English
        """
        text_lower = text.lower()
        
        # Calculate Chichewa score
        chichewa_score = sum(
            weight for word, weight in self.chichewa_indicators.items() 
            if word in text_lower
        )
        
        # Calculate English score
        english_score = sum(
            1 for word in self.english_indicators 
            if word in text_lower
        )
        
        # Decision: need at least score of 2 for Chichewa
        if chichewa_score >= 2 and chichewa_score > english_score:
            return 'ny'
        else:
            return 'en'
    
    def enhance_query(self, query: str) -> str:
        """
        Enhance query with bilingual terms for better retrieval
        
        Args:
            query: Original query
            
        Returns:
            Enhanced query with additional keywords
        """
        query_lower = query.lower()
        enhanced_terms = []
        
        # Add related keywords from mapping
        for concept, keywords in self.chichewa_keywords.items():
            if any(kw in query_lower for kw in keywords):
                enhanced_terms.extend(keywords)
        
        # Combine original query with enhanced terms (deduplicated)
        enhanced = query + " " + " ".join(set(enhanced_terms))
        return enhanced
    
    def validate_chichewa_response(
        self, 
        response: str, 
        min_chichewa_words: int = 3
    ) -> bool:
        """
        Validate that a response contains sufficient Chichewa content
        
        Args:
            response: Response text to validate
            min_chichewa_words: Minimum number of Chichewa words required
            
        Returns:
            True if response is valid Chichewa, False otherwise
        """
        chichewa_words = [
            'ndalama', 'ngongole', 'bajeti', 'kusunga', 'bizinesi', 'banki',
            'kodi', 'bwanji', 'ndi', 'ku', 'pa', 'za', 'chifukwa', 'kwa',
            'yambani', 'yankho', 'chindikiro', 'funso', 'zikomo', 'chonde'
        ]
        
        response_lower = response.lower()
        
        # Count Chichewa words
        chichewa_count = sum(
            1 for word in chichewa_words 
            if word in response_lower
        )
        
        # Count English words
        english_count = sum(
            1 for word in self.english_indicators 
            if word in response_lower
        )
        
        # Valid if: has enough Chichewa words AND not dominated by English
        return (
            chichewa_count >= min_chichewa_words and 
            english_count < chichewa_count
        )


class QueryProcessor:
    """Process and analyze queries"""
    
    def __init__(self):
        self.detector = LanguageDetector()
    
    def process(self, query: str) -> dict:
        """
        Process query and extract metadata
        
        Args:
            query: Input query
            
        Returns:
            Dictionary with query metadata
        """
        return {
            'original_query': query,
            'enhanced_query': self.detector.enhance_query(query),
            'language': self.detector.detect_language(query),
            'query_terms': set(re.findall(r'\w+', query.lower()))
        }


class RealtimeTranslator:
    """
    Handles on-demand translation for Chichewa support
    Uses Google Translate API via deep_translator
    """
    
    def __init__(self):
        if not TRANSLATION_AVAILABLE:
            print("Warning: Translation not available. Install deep-translator package.")
            self.enabled = False
            return
        
        try:
            self.en_to_ny = GoogleTranslator(source='en', target='ny')
            self.ny_to_en = GoogleTranslator(source='ny', target='en')
            self.financial_glossary = Config.FINANCIAL_GLOSSARY
            self.enabled = True
        except Exception as e:
            print(f"Translation initialization failed: {e}")
            self.enabled = False
    
    def translate_to_english(self, text: str) -> str:
        """
        Translate Chichewa to English
        
        Args:
            text: Chichewa text
            
        Returns:
            English translation
        """
        if not self.enabled:
            return text
        
        try:
            if not text or len(text.strip()) < 2:
                return text
            
            translated = self.ny_to_en.translate(text)
            return translated if translated else text
            
        except Exception as e:
            print(f"Translation error (NY→EN): {e}")
            return text
    
    def translate_to_chichewa(self, text: str) -> str:
        """
        Translate English to Chichewa with glossary enhancement
        
        Args:
            text: English text
            
        Returns:
            Chichewa translation
        """
        if not self.enabled:
            return text
        
        try:
            if not text or len(text.strip()) < 2:
                return text
            
            # Translate
            translated = self.en_to_ny.translate(text)
            
            # Apply financial glossary for key terms
            for en_term, ny_term in self.financial_glossary.items():
                pattern = r'\b' + re.escape(en_term) + r'\b'
                translated = re.sub(pattern, ny_term, translated, flags=re.IGNORECASE)
            
            return translated if translated else text
            
        except Exception as e:
            print(f"Translation error (EN→NY): {e}")
            return text
    
    def translate_response(self, response: str, source_lang: str, target_lang: str) -> dict:
        """
        Translate response with metadata and timeout handling
        Args:
            response: Original response text
            source_lang: Source language code
            target_lang: Target language code"""
        if not self.enabled:
            return {
                'translated_text': response,
                'original_text': response,
                'translation_success': False,
                'error': 'Translation not available'
            }
    
        if source_lang == target_lang:
            return {
                'translated_text': response,
                'original_text': response,
                'translation_success': True,
                'error': None
            }
    
        try:
            # Add timeout handling
            def timeout_handler(signum, frame):
                raise TimeoutError("Translation timeout")
        
            # Set timeout to 10 seconds per translation
            if hasattr(signal, 'SIGALRM'):  # Unix-like systems
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
        
            try:
                if target_lang == 'ny':
                    translated = self.translate_to_chichewa(response)
                else:
                    translated = self.translate_to_english(response)
            
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)  # Cancel alarm
            
                return {
                    'translated_text': translated,
                    'original_text': response,
                    'translation_success': True,
                    'error': None,
                    'source_lang': source_lang,
                    'target_lang': target_lang
                }
        
            except TimeoutError:
                print("⚠️ Translation timeout - chunk too long")
                return {
                    'translated_text': response,
                    'original_text': response,
                    'translation_success': False,
                    'error': 'Translation timeout'
                }
            
        except Exception as e:
            return {
                'translated_text': response,
                'original_text': response,
                'translation_success': False,
                'error': str(e)
            }

def translate_response_if_needed(query: str, english_response: str, translator, language_detector) -> str:
    """
    Quick wrapper to translate responses to Chichewa
    
    Args:
        query: Original user query
        english_response: Response generated in English
        translator: RealtimeTranslator instance
        language_detector: LanguageDetector instance
        
    Returns:
        Response in Chichewa if query was in Chichewa, otherwise original English response
    """
    query_lang = language_detector.detect_language(query)
    
    if query_lang == 'ny' and translator and translator.enabled:
        print("🌍 Translating response to Chichewa...")
        return translator.translate_to_chichewa(english_response)
    else:
        return english_response