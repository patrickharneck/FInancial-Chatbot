"""
RAG retrieval system with FAISS and reranking
Handles document indexing, retrieval, and reranking
Supports both PDF and CSV document sources
"""

import json
import re
import faiss
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict, Optional
from config import Config
from language_utils import LanguageDetector, RealtimeTranslator, translate_response_if_needed
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from pathlib import Path

class DocumentLoader:
    """Load and prepare document corpus from multiple sources"""
    
    @staticmethod
    def load_from_faiss(corpus_path: str, index_path: str) -> tuple:
        """
        Load corpus from FAISS index and meta JSON
        
        Returns:
            Tuple of (corpus_texts, corpus_metadata, faiss_index)
        """
        try:
            print(f"📁 Loading corpus from: {corpus_path}")
            print(f"📁 Loading index from: {index_path}")
            
            with open(corpus_path, 'r', encoding='utf-8') as f:
                corpus_info = json.load(f)
            
            corpus_texts = [rec['content'] for rec in corpus_info['records']]
            corpus_metadata = corpus_info['records']
            
            # Ensure language field exists
            for meta in corpus_metadata:
                if 'language' not in meta:
                    meta['language'] = 'English' if meta.get('lang_code') == 'en' else 'Chichewa'
            
            print(f"🔍 Loading FAISS index...")
            faiss_index = faiss.read_index(str(index_path))
            print(f"✅ FAISS index loaded with {faiss_index.ntotal} vectors")
            
            return corpus_texts, corpus_metadata, faiss_index
            
        except Exception as e:
            print(f"❌ Error loading FAISS index: {e}")
            raise
    
    @staticmethod
    def load_corpus(source_paths: list, source_type: str = "pdf") -> tuple:
        """
        Universal corpus loader supporting multiple source types
        
        Args:
            source_paths: List of file paths
            source_type: "pdf" or "csv"
            
        Returns:
            Tuple of (corpus_texts, corpus_metadata)
        """
        if source_type == "pdf":
            return DocumentLoader.load_from_pdf(source_paths)
        elif source_type == "csv":
            return DocumentLoader.load_from_csv(source_paths)
        else:
            print(f"⚠️ Source type '{source_type}' not supported")
            return [], []

    @staticmethod
    def load_from_pdf(pdf_paths: list) -> tuple:
        """
        Load corpus from PDF documents
        
        Args:
            pdf_paths: List of PDF file paths
            
        Returns:
            Tuple of (corpus_texts, corpus_metadata)
        """
        corpus_texts = []
        corpus_metadata = []
        
        for pdf_path in pdf_paths:
            try:
                if not Path(pdf_path).exists():
                    print(f"❌ PDF file not found: {pdf_path}")
                    continue
                    
                print(f"📄 Loading PDF: {Path(pdf_path).name}")
                loader = PyPDFLoader(str(pdf_path))
                documents = loader.load()
                
                # Optional: Split large pages into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    separators=["\n\n", "\n", ". ", " ", ""]
                )
                
                for doc in documents:
                    # Split if content is too large
                    if len(doc.page_content) > 1500:
                        chunks = text_splitter.split_text(doc.page_content)
                        for i, chunk in enumerate(chunks):
                            corpus_texts.append(chunk)
                            corpus_metadata.append({
                                'source': Path(pdf_path).name,
                                'page': doc.metadata.get('page', 0) + 1,
                                'chunk': i + 1,
                                'language': 'English', 
                                'lang_code': 'en',
                                'category': 'financial_literacy',
                                'document_type': 'pdf'
                            })
                    else:
                        corpus_texts.append(doc.page_content)
                        corpus_metadata.append({
                            'source': Path(pdf_path).name,
                            'page': doc.metadata.get('page', 0) + 1,
                            'language': 'English', 
                            'lang_code': 'en',
                            'category': 'financial_literacy',
                            'document_type': 'pdf'
                        })
                
                print(f"✅ Loaded {len(documents)} pages from: {Path(pdf_path).name}")
                
            except Exception as e:
                print(f"❌ Error loading {pdf_path}: {e}")
        
        print(f"📊 Total: {len(corpus_texts)} text chunks from {len(pdf_paths)} PDF(s)")
        return corpus_texts, corpus_metadata

    @staticmethod
    def load_from_csv(csv_paths: list) -> tuple:
        """
        Load corpus from CSV files
        
        Expected CSV columns:
        - 'question' or 'query': The question/query text
        - 'answer' or 'response' or 'content': The answer/content text
        - 'language' (optional): Language of the content
        - 'category' (optional): Category/topic
        
        Args:
            csv_paths: List of CSV file paths
            
        Returns:
            Tuple of (corpus_texts, corpus_metadata)
        """
        corpus_texts = []
        corpus_metadata = []
        
        for csv_path in csv_paths:
            try:
                if not Path(csv_path).exists():
                    print(f"❌ CSV file not found: {csv_path}")
                    continue
                
                print(f"📊 Loading CSV: {Path(csv_path).name}")
                df = pd.read_csv(csv_path, encoding='utf-8')
                
                # Detect column names (flexible column matching)
                question_col = None
                answer_col = None
                
                # Find question column
                for col in ['question', 'query', 'Question', 'Query', 'q']:
                    if col in df.columns:
                        question_col = col
                        break
                
                # Find answer column
                for col in ['answer', 'response', 'content', 'Answer', 'Response', 'Content', 'a']:
                    if col in df.columns:
                        answer_col = col
                        break
                
                if not answer_col:
                    print(f"⚠️ No answer/content column found in {csv_path}")
                    print(f"Available columns: {df.columns.tolist()}")
                    continue
                
                # Process each row
                for idx, row in df.iterrows():
                    # Build content text
                    content_parts = []
                    
                    if question_col and pd.notna(row[question_col]):
                        content_parts.append(f"Question: {row[question_col]}")
                    
                    if pd.notna(row[answer_col]):
                        content_parts.append(f"Answer: {row[answer_col]}")
                    
                    if not content_parts:
                        continue
                    
                    content = "\n".join(content_parts)
                    corpus_texts.append(content)
                    
                    # Detect language
                    lang_code = 'en'
                    language = 'English'
                    
                    if 'language' in df.columns and pd.notna(row['language']):
                        lang_str = str(row['language']).lower()
                        if 'chichewa' in lang_str or 'chewa' in lang_str or 'ny' in lang_str:
                            lang_code = 'ny'
                            language = 'Chichewa'
                    
                    # Build metadata
                    metadata = {
                        'source': Path(csv_path).name,
                        'row': idx + 1,
                        'language': language,
                        'lang_code': lang_code,
                        'document_type': 'csv',
                        'content': row[answer_col],  # Store answer for easy access
                        'original_answer': row[answer_col]
                    }
                    
                    # Add optional fields
                    if question_col:
                        metadata['question'] = row[question_col]
                    
                    if 'category' in df.columns and pd.notna(row['category']):
                        metadata['category'] = row['category']
                    else:
                        metadata['category'] = 'general'
                    
                    # Add any other columns as metadata
                    for col in df.columns:
                        if col not in [question_col, answer_col, 'language', 'category'] and pd.notna(row[col]):
                            metadata[col] = row[col]
                    
                    corpus_metadata.append(metadata)
                
                print(f"✅ Loaded {len(df)} rows from: {Path(csv_path).name}")
                
            except Exception as e:
                print(f"❌ Error loading {csv_path}: {e}")
        
        print(f"📊 Total: {len(corpus_texts)} entries from {len(csv_paths)} CSV(s)")
        return corpus_texts, corpus_metadata


class Reranker:
    """DistilBERT-based reranker for retrieved documents"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.enabled = False
    
    def load(self) -> bool:
        """
        Load reranker model
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not Path(self.model_path).exists():
                print(f"❌ Reranker model path not found: {self.model_path}")
                return False
            
            print(f"🔄 Loading reranker from: {self.model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(str(self.model_path))
            self.model = AutoModelForSequenceClassification.from_pretrained(
                str(self.model_path)
            )
            self.model.to(self.device)
            self.model.eval()
            self.enabled = False
            print("✅ Reranker loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load reranker: {e}")
            self.enabled = False
            return False
    
    def rerank(
        self, 
        query: str, 
        retrieved_docs: List[Dict], 
        top_k: int = 3
    ) -> List[Dict]:
        """
        Rerank retrieved documents using DistilBERT
        
        Args:
            query: Original query
            retrieved_docs: List of retrieved documents
            top_k: Number of top documents to return
            
        Returns:
            Reranked documents
        """
        if not self.enabled or self.model is None:
            return retrieved_docs[:top_k]
        
        try:
            # Prepare query-document pairs
            pairs = []
            for doc in retrieved_docs:
                meta = doc['metadata']
                answer = meta.get('original_answer') or meta.get('answer', '') or meta.get('content', '')
                pairs.append({
                    'query': f"query: {query}",
                    'document': f"passage: {answer}",
                    'original_doc': doc
                })
            
            # Encode pairs
            texts = [(p['query'], p['document']) for p in pairs]
            encoded = self.tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=256,
                return_tensors='pt'
            ).to(self.device)
            
            # Get reranking scores
            with torch.no_grad():
                outputs = self.model(**encoded)
                rerank_scores = torch.softmax(outputs.logits, dim=-1)[:, 1].cpu().numpy()
            
            # Combine scores
            for i, pair in enumerate(pairs):
                original_doc = pair['original_doc']
                original_doc['rerank_score'] = float(rerank_scores[i])
                original_doc['final_score'] = (
                    0.3 * original_doc['similarity_score'] + 
                    0.7 * original_doc['rerank_score']
                )
            
            # Sort by final score
            reranked = sorted(
                retrieved_docs,
                key=lambda x: x.get('final_score', x['similarity_score']),
                reverse=True
            )
            
            return reranked[:top_k]
            
        except Exception as e:
            print(f"⚠️ Reranking failed: {e}")
            return retrieved_docs[:top_k]


class RAGRetriever:
    """Complete RAG retrieval system with real-time translation support"""
    
    def __init__(self, enable_translation: bool = True):
        self.embedder = None
        self.vector_index = None
        self.corpus_texts = []
        self.corpus_metadata = []
        self.reranker = None
        self.language_detector = LanguageDetector()
        self.system_type = "unknown"
        
        # Real-time translation
        self.enable_translation = enable_translation and Config.ENABLE_REALTIME_TRANSLATION
        self.translator = None
        if self.enable_translation:
            self.translator = RealtimeTranslator()
            if not self.translator.enabled:
                print("Warning: Translation requested but not available")
                self.enable_translation = False
    
    def initialize(self) -> bool:
        """
        Initialize the RAG system
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load embedding model
            device = 'cpu'
            print(f"🔄 Loading embedding model: {Config.EMBEDDING_MODEL}")
            self.embedder = SentenceTransformer(
                Config.EMBEDDING_MODEL,
                device=device
            )
            print(f"✅ Loaded embedding model: {Config.EMBEDDING_MODEL}")
            
            # Check if FAISS files exist
            faiss_index_exists = Path(Config.FAISS_INDEX_PATH).exists()
            corpus_json_exists = Path(Config.CORPUS_JSON_PATH).exists()
            
            print(f"📁 FAISS index exists: {faiss_index_exists}")
            print(f"📁 Corpus JSON exists: {corpus_json_exists}")
            
            # Try to load FAISS index
            if faiss_index_exists and corpus_json_exists:
                print("🔄 Loading FAISS index and corpus...")
                self.corpus_texts, self.corpus_metadata, self.vector_index = \
                    DocumentLoader.load_from_faiss(
                        str(Config.CORPUS_JSON_PATH),
                        str(Config.FAISS_INDEX_PATH)
                    )
                self.system_type = "faiss"
                print(f"✅ Loaded {len(self.corpus_texts)} documents from FAISS index")
            else:
                print("⚠️ FAISS files not found, checking for fallback sources...")
                if not faiss_index_exists:
                    print(f"❌ FAISS index not found at: {Config.FAISS_INDEX_PATH}")
                if not corpus_json_exists:
                    print(f"❌ Corpus JSON not found at: {Config.CORPUS_JSON_PATH}")
                
                # Try loading from available sources
                loaded = False
                
                # 1. Try PDF files
                pdf_files = ["FINANCIAL LITERACY.pdf"]
                pdf_paths = [Config.DATA_DIR / pdf for pdf in pdf_files]
                pdf_paths_exist = [p for p in pdf_paths if p.exists()]
                
                if pdf_paths_exist:
                    try:
                        print(f"🔄 Loading documents from {len(pdf_paths_exist)} PDF file(s)...")
                        self.corpus_texts, self.corpus_metadata = \
                            DocumentLoader.load_from_pdf(pdf_paths_exist)
                        
                        if self.corpus_texts:
                            loaded = True
                            self.system_type = "pdf_fallback"
                    except Exception as e:
                        print(f"❌ PDF loading failed: {e}")
                
                # 2. Try CSV files if PDF loading failed or no PDFs found
                if not loaded:
                    csv_files = ["Financial Literacy_FAQs_Cleaned.csv"]
                    csv_paths = [Config.DATA_DIR / csv for csv in csv_files]
                    csv_paths_exist = [p for p in csv_paths if p.exists()]
                    
                    if csv_paths_exist:
                        try:
                            print(f"🔄 Loading documents from {len(csv_paths_exist)} CSV file(s)...")
                            self.corpus_texts, self.corpus_metadata = \
                                DocumentLoader.load_from_csv(csv_paths_exist)
                            
                            if self.corpus_texts:
                                loaded = True
                                self.system_type = "csv_fallback"
                        except Exception as e:
                            print(f"❌ CSV loading failed: {e}")
                
                # 3. Create FAISS index from loaded content
                if loaded and self.corpus_texts:
                    try:
                        print("🔄 Creating FAISS index from loaded content...")
                        embeddings = self.embedder.encode(self.corpus_texts)
                        self.vector_index = faiss.IndexFlatIP(embeddings.shape[1])
                        faiss.normalize_L2(embeddings)
                        self.vector_index.add(embeddings)
                        self.system_type += "_with_index"
                        print(f"✅ Created FAISS index with {len(self.corpus_texts)} documents")
                    except Exception as e:
                        print(f"❌ FAISS index creation failed: {e}")
                else:
                    self.system_type = "no_data"
                    print("❌ No documents loaded from any source")
            
            # Load reranker
            self.reranker = Reranker(Config.RERANKER_MODEL_PATH)
            self.reranker.load()
            
            print(f"🎯 RAG system type: {self.system_type}")
            print(f"📚 Total documents: {len(self.corpus_texts)}")
            print(f"🔍 Vector index available: {self.vector_index is not None}")
            print(f"🔄 Reranker enabled: {self.reranker.enabled}")
            
            return len(self.corpus_texts) > 0 and self.vector_index is not None
            
        except Exception as e:
            print(f"❌ RAG initialization failed: {e}")
            return False
    
    def retrieve(
        self, 
        query: str, 
        top_k: int = Config.DEFAULT_TOP_K,
        use_reranking: bool = True,
        translate_query: bool = True
    ) -> List[Dict]:
        """
        Retrieve relevant documents for a query with optional translation
        
        Args:
            query: Search query (can be English or Chichewa)
            top_k: Number of documents to return
            use_reranking: Whether to use reranker
            translate_query: If True, translate Chichewa queries to English for retrieval
            
        Returns:
            List of retrieved documents with metadata
        """
        try:
            # Check if system is ready
            if not self.vector_index:
                print("❌ Vector index not available, using keyword fallback")
                return self._keyword_fallback(query, top_k)
            
            if not self.corpus_texts:
                print("❌ No documents available")
                return []
            
            # Detect language
            query_lang = self.language_detector.detect_language(query)
            original_query = query
            
            # Translate Chichewa query to English for retrieval (if enabled)
            if query_lang == 'ny' and translate_query and self.enable_translation:
                print(f"🌍 Detected Chichewa query, translating to English...")
                translated_query = self.translator.translate_to_english(query)
                print(f"📝 Translated query: {translated_query}")
                query = translated_query
            
            # Enhance query
            enhanced_query = self.language_detector.enhance_query(query)
            
            # Retrieve more documents if reranking
            initial_k = top_k * 3 if (use_reranking and self.reranker.enabled) else top_k
            initial_k = min(initial_k, len(self.corpus_texts))
            
            print(f"🔍 Searching for: {enhanced_query}")
            print(f"📊 Retrieving {initial_k} documents from {len(self.corpus_texts)} total")
            
            # Get embeddings and search
            query_embedding = self.embedder.encode(
                [enhanced_query], 
                convert_to_numpy=True
            )
            faiss.normalize_L2(query_embedding)
            
            scores, indices = self.vector_index.search(query_embedding, initial_k)
            
            # Build results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.corpus_texts):
                    results.append({
                        'metadata': self.corpus_metadata[idx],
                        'similarity_score': float(score),
                        'index': idx,
                        'original_query': original_query,
                        'translated_query': query if query != original_query else None,
                        'query_language': query_lang,
                        'content': self.corpus_texts[idx]
                    })
            
            if not results:
                print("❌ No results from vector search, using keyword fallback")
                return self._keyword_fallback(original_query, top_k)
            
            # Boost same-language documents
            results = self._boost_same_language(results, query_lang)
            
            # Rerank if enabled
            if use_reranking and self.reranker.enabled:
                print("🔄 Reranking documents...")
                results = self.reranker.rerank(original_query, results, top_k)
                for r in results:
                    r['reranked'] = True
            else:
                results = results[:top_k]
                for r in results:
                    r['reranked'] = False
            
            print(f"✅ Retrieved {len(results)} documents")
            return results
            
        except Exception as e:
            print(f"❌ Retrieval failed: {e}")
            return self._keyword_fallback(query, top_k)
    
    def _boost_same_language(
        self, 
        results: List[Dict], 
        query_lang: str
    ) -> List[Dict]:
        """Boost documents in the same language as query"""
        for result in results:
            if result['metadata'].get('lang_code') == query_lang:
                result['similarity_score'] *= 1.3
        
        return sorted(
            results, 
            key=lambda x: x['similarity_score'], 
            reverse=True
        )
    
    def _keyword_fallback(self, query: str, top_k: int) -> List[Dict]:
        """Keyword-based fallback retrieval"""
        if not self.corpus_texts:
            return []
            
        print(f"🔤 Using keyword fallback for: {query}")
        query_lang = self.language_detector.detect_language(query)
        query_terms = set(re.findall(r'\w+', query.lower()))
        
        scored_docs = []
        for i, metadata in enumerate(self.corpus_metadata):
            content = self.corpus_texts[i].lower()
            content_terms = set(re.findall(r'\w+', content))
            
            overlap = len(query_terms & content_terms)
            lang_bonus = 0.5 if metadata.get('lang_code') == query_lang else 0
            
            if overlap > 0 or lang_bonus > 0:
                score = (overlap / max(len(query_terms), 1)) + lang_bonus
                scored_docs.append({
                    'metadata': metadata,
                    'similarity_score': score,
                    'index': i,
                    'content': self.corpus_texts[i],
                    'reranked': False
                })
        
        results = sorted(
            scored_docs, 
            key=lambda x: x['similarity_score'], 
            reverse=True
        )[:top_k]
        
        print(f"✅ Keyword fallback found {len(results)} documents")
        return results
    
    def generate_response_with_translation(
        self,
        query: str,
        retrieved_docs: List[Dict],
        response_language: str = 'auto'
    ) -> str:
        """
        Generate response with automatic translation based on query language
        
        Args:
            query: Original user query
            retrieved_docs: Retrieved documents from RAG system
            response_language: 'auto', 'en', or 'ny'
            
        Returns:
            Response in appropriate language
        """
        # Detect query language
        query_lang = self.language_detector.detect_language(query)
        
        # Prepare context from retrieved documents
        context = "\n\n".join([doc['content'] for doc in retrieved_docs[:3]])
        
        # Generate prompt based on language
        if query_lang == 'ny' or response_language == 'ny':
            prompt = f"""
            Muyankhe funso lotsatira m'Chichewa pokhazikika:
            
            Funso: {query}
            
            Zambiri zothandiza:
            {context}
            
            Muyankhe m'Chichewa. Perekani mayankho athyathyathya, owongoka, ndipo ogwirizana ndi mafunso.
            """
        else:
            prompt = f"""
            Answer the following question based on the context:
            
            Question: {query}
            
            Context:
            {context}
            
            Provide a clear, accurate, and concise answer that directly addresses the question.
            """
        
        # Generate response using your LLM
        try:
            english_response = self._call_llm(prompt)
            
            final_response = translate_response_if_needed(
                query, 
                english_response, 
                self.translator, 
                self.language_detector
            )
            
            return final_response

        except Exception as e:
            print(f"❌ Response generation failed: {e}")
            return "Pepani, sindinathe kuyankha funso lanu panopa." if query_lang == 'ny' else "Sorry, I couldn't generate a response at this time."
    
    def search_faqs(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search FAQs using semantic search and return formatted results
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of formatted FAQ results
        """
        try:
            # Use the existing retrieve method
            raw_results = self.retrieve(
                query=query,
                top_k=top_k,
                use_reranking=True,
                translate_query=True
            )
            
            # Format results for FAQ display
            formatted_results = []
            for result in raw_results:
                metadata = result['metadata']
                
                # Extract question and answer
                question = self._extract_faq_question(metadata, result['content'])
                answer = self._extract_faq_answer(metadata, result['content'])
                
                formatted_result = {
                    'question': question,
                    'answer': answer,
                    'similarity_score': result['similarity_score'],
                    'language': metadata.get('language', 'English'),
                    'category': metadata.get('category', 'general'),
                    'source': metadata.get('source', 'Unknown'),
                    'confidence': self._calculate_search_confidence(result),
                    'metadata': metadata
                }
                formatted_results.append(formatted_result)
            
            return formatted_results
            
        except Exception as e:
            print(f"❌ FAQ search failed: {e}")
            return []
    
    def _extract_faq_question(self, metadata: Dict, content: str) -> str:
        """Extract question from FAQ data"""
        # Try metadata first
        if 'question' in metadata and metadata['question']:
            return str(metadata['question'])
        
        # Try to extract from content
        content_lower = content.lower()
        if 'question:' in content_lower:
            parts = content.split('Question:', 1)
            if len(parts) > 1:
                question_part = parts[1].split('\n', 1)[0].strip()
                return question_part
        
        # Fallback: use first line or truncate content
        lines = content.split('\n', 1)
        if len(lines) > 0:
            first_line = lines[0].strip()
            if len(first_line) < 100:  # Reasonable question length
                return first_line
        
        # Last resort: truncate content
        return content[:100] + "..." if len(content) > 100 else content
    
    def _extract_faq_answer(self, metadata: Dict, content: str) -> str:
        """Extract answer from FAQ data"""
        # Try metadata first
        if 'answer' in metadata and metadata['answer']:
            return str(metadata['answer'])
        if 'content' in metadata and metadata['content']:
            return str(metadata['content'])
        if 'original_answer' in metadata and metadata['original_answer']:
            return str(metadata['original_answer'])
        
        # Try to extract from content
        content_lower = content.lower()
        if 'answer:' in content_lower:
            parts = content.split('Answer:', 1)
            if len(parts) > 1:
                return parts[1].strip()
        
        # Return full content as answer
        return content
    
    def _calculate_search_confidence(self, result: Dict) -> float:
        """Calculate display confidence from similarity score"""
        score = result.get('similarity_score', 0.0)
        # Convert FAISS similarity to percentage (assuming normalized vectors)
        return min(100.0, max(0.0, score * 100))
                
    def _call_llm(self, prompt: str) -> str:
        """
        Call Groq API to generate response
        Replace with your actual LLM implementation
        """
        return "This is a placeholder response. Replace with actual LLM call."