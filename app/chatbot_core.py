# chatbot_core.py
"""
Main chatbot logic combining all components
Handles query processing, response generation, and orchestration
"""
import re
import traceback
import time
from typing import Dict, Optional
from config import Config
from llm_client import GroqClient
from language_utils import LanguageDetector, QueryProcessor, RealtimeTranslator
from rag_retriever import RAGRetriever
from prompt_builder import PromptBuilder
from fallback_responses import FallbackResponses


class BilingualChatbot:
    """
    Main chatbot class that orchestrates all components
    Supports real-time translation for Chichewa queries
    """
    
    def __init__(self, enable_translation: bool = True):
        # Core components
        self.rag_retriever = RAGRetriever(enable_translation=enable_translation)
        self.language_detector = LanguageDetector()
        self.query_processor = QueryProcessor()
        self.prompt_builder = PromptBuilder()
        
        # Real-time translation
        self.enable_translation = enable_translation and Config.ENABLE_REALTIME_TRANSLATION
        self.translator: Optional[RealtimeTranslator] = None
        if self.enable_translation:
            self.translator = RealtimeTranslator()
            if not self.translator.enabled:
                print("Warning: Translation not available")
                self.enable_translation = False
        
        # LLM client (optional)
        self.llm_client: Optional[GroqClient] = None
        self.groq_enabled = False
        
        # Configuration
        self.confidence_threshold = Config.DEFAULT_CONFIDENCE_THRESHOLD
        self.response_length_threshold = Config.DEFAULT_RESPONSE_LENGTH
        
        # State
        self.conversation_history = []
        self.system_ready = False
    
    def initialize(self, groq_api_key: Optional[str] = None) -> bool:
        """
        Initialize the chatbot system
        
        Args:
            groq_api_key: Optional Groq API key for LLM features
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Initialize RAG retriever
            if not self.rag_retriever.initialize():
                return False
            
            # Initialize LLM client if API key provided
            if groq_api_key:
                self.llm_client = GroqClient(groq_api_key)
                self.groq_enabled = True
            
            self.system_ready = True
            return True
            
        except Exception as e:
            print(f"Chatbot initialization failed: {e}")
            return False

    def _check_response_quality(self, text: str) -> bool:
        """
        Check if a response is of acceptable quality
        
        Args:
            text: Response text to check
            
        Returns:
            True if quality is acceptable, False otherwise
        """
        if not text or len(text.strip()) < 10:
            return False
        
        # Check for excessive repetition (common in bad LLM outputs)
        words = text.lower().split()
        if len(words) < 5:
            return False
        
        # Count consecutive repeated words
        max_consecutive = 1
        current_consecutive = 1
        for i in range(1, len(words)):
            if words[i] == words[i-1]:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 1
        
        # If more than 5 consecutive repeated words, it's bad
        if max_consecutive > 5:
            return False
        
        # Check for repetitive phrases (3+ word sequences)
        phrase_counts = {}
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
        
        # If any phrase repeats more than 3 times, it's suspicious
        if phrase_counts and max(phrase_counts.values()) > 3:
            return False
        
        return True

    def _expand_response(self, response: str, query: str, context: str, max_attempts: int = 2) -> str:
        """
        Safely expand a response if it's too short, with quality checks
        
        Args:
            response: Original response
            query: User query
            context: Retrieved context
            max_attempts: Maximum expansion attempts
            
        Returns:
            Expanded response (or original if expansion fails)
        """
        if not self.groq_enabled or not self.llm_client:
            return response
        
        for attempt in range(max_attempts):
            try:
                expansion_prompt = f"""The following answer is too brief. Please expand it with more detail and examples while staying accurate to the source material.

Original Question: {query}

Current Answer: {response}

Source Context: {context[:2000]}

Please provide a more detailed, comprehensive answer (minimum {self.response_length_threshold} words). Stay factual and based on the context provided."""

                expanded = self.llm_client.generate(expansion_prompt, temperature=0.3)
                
                # Quality check
                if expanded and self._check_response_quality(expanded) and len(expanded.split()) >= self.response_length_threshold:
                    return expanded
                
            except Exception as e:
                print(f"⚠️ Expansion attempt {attempt + 1} failed: {e}")
        
        # If all attempts fail, return original
        return response

    def _translate_to_chichewa(self, text: str) -> str:
        """
        Safely translate text to Chichewa with quality checks and retry logic
        """
        if not text or not self.enable_translation or not self.translator:
            return text
    
        try:
            # Check if text has numbered lists
            has_numbered_lists = bool(re.search(r'\d+\.\s+\w', text))
        
            if has_numbered_lists:
                print("📋 Detected numbered lists, translating item by item...")
            
                # More robust regex to capture list items
                # Pattern: number followed by dot, space, and content until next number or end
                pattern = r'(\d+\.)\s+((?:(?!\d+\.).)+)'
                matches = list(re.finditer(pattern, text, re.DOTALL))
            
                if matches:
                    translated_parts = []
                    last_end = 0
                
                    # Translate text before first numbered item
                    if matches[0].start() > 0:
                        prefix = text[:matches[0].start()].strip()
                        if prefix:
                            translated_prefix = self._translate_chunk_with_retry(prefix)
                            translated_parts.append(translated_prefix + '\n\n')
                
                    # Translate each numbered item
                    for match in matches:
                        number = match.group(1)  # "1." "2." etc
                        content = match.group(2).strip()
                    
                        if content and len(content) > 3:  # Skip very short/empty content
                            translated_content = self._translate_chunk_with_retry(content)
                            if translated_content:
                                translated_parts.append(f"{number} {translated_content}\n\n")
                            else:
                                # If translation fails, keep English
                                translated_parts.append(f"{number} {content}\n\n")
                        else:
                            print(f"⚠️ Skipping empty/short list item: {number}")
                    
                        last_end = match.end()
                
                    # Translate any remaining text after last numbered item
                    if last_end < len(text):
                        suffix = text[last_end:].strip()
                        if suffix:
                            translated_suffix = self._translate_chunk_with_retry(suffix)
                            translated_parts.append('\n' + translated_suffix)
                
                    final_translation = ''.join(translated_parts).strip()
                
                    # Quality check
                    if self._check_response_quality(final_translation):
                        return final_translation
                    else:
                        print("⚠️ Translation quality check failed, returning English")
                        return text
                else:
                    # Regex didn't match - fall back to simple translation
                    return self._translate_chunk_with_retry(text) or text
        
            else:
                # No numbered lists - translate in paragraphs
                paragraphs = text.split('\n\n')
                translated_paragraphs = []
            
                for para in paragraphs:
                    if not para.strip():
                        translated_paragraphs.append(para)
                        continue
                
                    translated_para = self._translate_chunk_with_retry(para.strip())
                    if translated_para:
                        translated_paragraphs.append(translated_para)
                    else:
                        translated_paragraphs.append(para)
            
                return '\n\n'.join(translated_paragraphs)
                
        except Exception as e:
            print(f"⚠️ Translation error: {e}")
            traceback.print_exc()
            return text
  
    def _translate_chunk_with_retry(self, text: str, max_retries: int = 2) -> str:
        """
        Translate a chunk of text with retry logic
    
        Args:
        text: Text to translate
        max_retries: Maximum number of retry attempts
        
        Returns:
        Translated text or None if all attempts fail
        """
        if not text or len(text.strip()) < 3:
            return text
    
        for attempt in range(max_retries + 1):
            try:
            # Split very long chunks
                if len(text) > 800:
                # Split at sentence boundaries
                    sentences = re.split(r'([.!?]+\s+)', text)
                
                    mid_point = len(sentences) // 2
                    first_half = ''.join(sentences[:mid_point])
                    second_half = ''.join(sentences[mid_point:])
                
                    translated_first = self._translate_chunk_with_retry(first_half, 0)  # No recursion retries
                    translated_second = self._translate_chunk_with_retry(second_half, 0)
                
                    if translated_first and translated_second:
                        return translated_first + ' ' + translated_second
                    else:
                        return text
            
                # Translate with timeout
                translation_result = self.translator.translate_response(
                    text, 
                    source_lang='en', 
                    target_lang='ny'
                )
            
                if translation_result.get('translation_success'):
                    translated = translation_result.get('translated_text', '').strip()
                
                # Validation checks
                    if translated and len(translated) > len(text) * 0.2:  # At least 20% of original length
                        return translated
                    else:
                        print(f"⚠️ Translation too short on attempt {attempt + 1}, retrying...")
                else:
                    print(f"⚠️ Translation failed on attempt {attempt + 1}: {translation_result.get('error', 'Unknown error')}")
            
                # Wait before retry
                if attempt < max_retries:
                    time.sleep(0.5)
        
            except Exception as e:
                print(f"⚠️ Translation attempt {attempt + 1} error: {e}")
                if attempt < max_retries:
                    time.sleep(0.5)
    
        # All attempts failed
        print(f"❌ All translation attempts failed for chunk: {text[:50]}...")
        return None    
    
    def _translate_to_english(self, text: str) -> str:
        """
        Translate Chichewa text to English
        
        Args:
            text: Chichewa text to translate
            
        Returns:
            Translated English text (or original if translation fails)
        """
        if not text or not self.enable_translation or not self.translator:
            return text
        
        try:
            translation_result = self.translator.translate_response(
                text, 
                source_lang='ny', 
                target_lang='en'
            )
            
            if translation_result.get('translation_success'):
                return translation_result.get('translated_text', text)
            else:
                return text
                
        except Exception as e:
            print(f"⚠️ Translation error: {e}")
            return text

    def _detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code ('en' for English, 'ny' for Chichewa)
        """
        try:
            query_info = self.query_processor.process(text)
            return query_info.get('language', 'en')
        except Exception as e:
            print(f"⚠️ Language detection failed: {e}")
            return 'en'  # Default to English

    def _build_context(self, retrieved_docs: list) -> str:
        """
        Build context string from retrieved documents
        
        Args:
            retrieved_docs: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, doc in enumerate(retrieved_docs[:3]):  # Use top 3 docs
            content = doc.get('answer') or doc.get('content', '') or doc.get('text', '')
            if content:
                context_parts.append(f"Document {i+1}:\n{content}")
        
        return "\n\n".join(context_parts) if context_parts else "No context available"

    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create LLM prompt for response generation
        
        Args:
            query: User query
            context: Retrieved context
            
        Returns:
            Formatted prompt
        """
        return self.prompt_builder.build_rag_prompt(query, context, 'en')

    def _get_fallback_response(self, query: str, detected_lang: str) -> str:
        """
        Get appropriate fallback response based on language
        
        Args:
            query: Original query
            detected_lang: Detected language
            
        Returns:
            Fallback response text
        """
        try:
            fallback = FallbackResponses.get_fallback(query, detected_lang)
            if fallback and len(fallback.strip()) > 0:
                return fallback
        except Exception as e:
            print(f"⚠️ Fallback response failed: {e}")
        
        # Ultimate fallback
        if detected_lang == 'ny':
            return "Pepani, sindikupatsa yankho latsopano pachifukwa ichi. Mutha kufunsa zina za ndalama."
        else:
            return "I'm sorry, I cannot provide an answer for this question right now. Please try asking about financial topics."

    def _ensure_valid_answer(self, answer: str, detected_lang: str) -> str:
        """
        Ensure the answer is valid and non-empty
        
        Args:
            answer: Proposed answer
            detected_lang: Detected language
            
        Returns:
            Valid answer text
        """
        if answer and len(answer.strip()) > 10:
            return answer
        
        # Return appropriate fallback if answer is empty
        return self._get_fallback_response("", detected_lang)

    def process_query(self, query: str, confidence_threshold: float = 0.6) -> Dict:
        """
        Process user query through complete RAG pipeline with safeguards
        
        Args:
            query: User question
            confidence_threshold: Minimum confidence for RAG response
            
        Returns:
            Dictionary with answer and metadata
        """
        if not self.system_ready:
            return self._get_error_response("System not initialized")
        
        if not query or len(query.strip()) == 0:
            return self._get_error_response("Empty query")
        
        try:
            # Detect language
            detected_lang = self._detect_language(query)
            original_query = query
            query_language = detected_lang
            
            print(f"🔍 Detected language: {detected_lang}")
            
            # Translate to English if Chichewa
            english_query = query
            if detected_lang == 'ny':
                english_query = self._translate_to_english(query)
                if english_query != query:
                    print(f"🌐 Translated query to English: {english_query}")
            
            # Retrieve relevant documents
            retrieved_docs = self.rag_retriever.retrieve(
                english_query, 
                top_k=5, 
                use_reranking=True,
                translate_query=False  # We already translated if needed
            )
            
            print(f"📚 Retrieved {len(retrieved_docs)} documents")
            
            if not retrieved_docs:
                fallback = self._get_fallback_response(query, detected_lang)
                return {
                    'answer': fallback,
                    'response_type': 'fallback',
                    'confidence': 0.0,
                    'source_docs': [],
                    'language': 'Chichewa' if detected_lang == 'ny' else 'English',
                    'query_language': query_language,
                    'translated': detected_lang == 'ny',
                    'threshold_met': False,
                    'word_count': len(fallback.split())
                }
            
            # Check confidence from best document
            best_doc = retrieved_docs[0]
            top_confidence = best_doc.get('final_score', 
                         best_doc.get('similarity_score', 
                         best_doc.get('score', 0)))
            
            print(f"🎯 Top confidence score: {top_confidence}")
            
            if top_confidence < confidence_threshold:
                # Low confidence - return direct excerpt with fallback guarantee
                answer = best_doc.get('answer', '') or best_doc.get('content', '') or ''
                if not answer:
                    # Try to get text from metadata
                    answer = best_doc.get('metadata', {}).get('answer', '') or best_doc.get('metadata', {}).get('content', '')
                
                # Ensure we have some content
                if not answer:
                    answer = self._get_fallback_response(query, detected_lang)
                else:
                    answer = answer[:500]  # Limit length
                
                # Translate if needed
                if detected_lang == 'ny':
                    answer = self._translate_to_chichewa(answer)
                
                # Final validation
                answer = self._ensure_valid_answer(answer, detected_lang)
                
                return {
                    'answer': answer,
                    'response_type': 'low_confidence_excerpt',
                    'confidence': top_confidence,
                    'source_docs': retrieved_docs[:3],
                    'language': 'Chichewa' if detected_lang == 'ny' else 'English',
                    'query_language': query_language,
                    'translated': detected_lang == 'ny',
                    'threshold_met': False,
                    'word_count': len(answer.split())
                }
            
            # High confidence - generate with LLM if available
            if self.groq_enabled and self.llm_client:
                try:
                    context = self._build_context(retrieved_docs)
                    prompt = self._create_prompt(english_query, context)
                    
                    print("🤖 Generating response with LLM...")
                    
                    # Generate response (ALWAYS in English first)
                    llm_response = self.llm_client.generate(prompt, temperature=0.1)
                    
                    # Quality check
                    if not llm_response or not self._check_response_quality(llm_response):
                        print("⚠️ LLM response failed quality check, using document content")
                        # Fall back to direct excerpt from best document
                        llm_response = best_doc.get('answer', '') or best_doc.get('content', '') or context[:1000]
                    
                    word_count = len(llm_response.split())
                    threshold_met = word_count >= self.response_length_threshold
                    original_answer = llm_response
                    
                    # Check if expansion is needed
                    if not threshold_met and self.response_length_threshold > 0:
                        print("📈 Expanding short response...")
                        expanded = self._expand_response(llm_response, english_query, context)
                        
                        # Quality check expansion
                        if expanded and self._check_response_quality(expanded):
                            llm_response = expanded
                            word_count = len(llm_response.split())
                            threshold_met = word_count >= self.response_length_threshold
                    
                    # Translate ONLY if Chichewa was detected
                    final_answer = llm_response
                    if detected_lang == 'ny':
                        print("🌍 Translating response to Chichewa...")
                        final_answer = self._translate_to_chichewa(llm_response)
                    
                    # Final validation
                    final_answer = self._ensure_valid_answer(final_answer, detected_lang)
                    word_count = len(final_answer.split())
                    
                    return {
                        'answer': final_answer,
                        'response_type': 'llm_generated',
                        'confidence': top_confidence,
                        'source_docs': retrieved_docs[:3],
                        'language': 'Chichewa' if detected_lang == 'ny' else 'English',
                        'query_language': query_language,
                        'translated': detected_lang == 'ny',
                        'original_answer': original_answer if detected_lang == 'ny' else None,
                        'threshold_met': threshold_met,
                        'word_count': word_count
                    }
                    
                except Exception as e:
                    print(f"⚠️ LLM generation failed: {e}")
                    # Fall through to RAG response
            
            # RAG response (no LLM or LLM failed)
            answer = best_doc.get('answer', '') or best_doc.get('content', '')
            if not answer:
                answer = self._get_fallback_response(query, detected_lang)
            
            if detected_lang == 'ny':
                answer = self._translate_to_chichewa(answer)
            
            # Final validation
            answer = self._ensure_valid_answer(answer, detected_lang)
            word_count = len(answer.split())
            
            return {
                'answer': answer,
                'response_type': 'rag_only',
                'confidence': top_confidence,
                'source_docs': retrieved_docs[:3],
                'language': 'Chichewa' if detected_lang == 'ny' else 'English',
                'query_language': query_language,
                'translated': detected_lang == 'ny',
                'threshold_met': False,
                'word_count': word_count
            }
            
        except Exception as e:
            print(f"❌ Query processing error: {e}")
            fallback = self._get_fallback_response(query, 'en')  # Default to English fallback
            return {
                'answer': fallback,
                'response_type': 'error_fallback',
                'confidence': 0.0,
                'source_docs': [],
                'language': 'English',
                'query_language': 'en',
                'translated': False,
                'threshold_met': False,
                'word_count': len(fallback.split()),
                'error': str(e)
            }
    
    def _get_error_response(self, error_msg: str = "") -> Dict:
        """Generate error response"""
        error_response = f"⚠️ Sorry, I'm having technical difficulties. {error_msg}".strip()
        return {
            'answer': error_response,
            'language': 'en',
            'confidence': 0.0,
            'sources_count': 0,
            'response_type': 'Error',
            'sources': [],
            'reranked': False,
            'retrieved_docs': [],
            'threshold_met': False,
            'word_count': len(error_response.split())
        }
    
    def get_system_info(self) -> Dict:
        """Get system information and statistics"""
        if not self.system_ready:
            return {'status': 'Not initialized'}
        
        return {
            'status': 'Active',
            'documents_count': len(self.rag_retriever.corpus_texts),
            'system_type': self.rag_retriever.system_type,
            'reranker_enabled': self.rag_retriever.reranker.enabled,
            'llm_enabled': self.groq_enabled,
            'translation_enabled': self.enable_translation,
            'languages': ['English', 'Chichewa'],
            'translation_mode': 'Real-time' if self.enable_translation else 'Disabled'
        }