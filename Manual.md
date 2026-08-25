# Manual for Financial Literacy Chatbot

This manual provides comprehensive documentation for users and administrators of the Financial Literacy Chatbot. It covers system functions, user journeys and data management.

## 1. System Overview

The Financial Literacy Chatbot is an AI-powered assistant that provides answers to financial questions in English and Chichewa. The system uses a sophisticated retrieval and reranking pipeline:

- **Embedding Model**: E5 multilingual embeddings for semantic search
- **Vector Database**: FAISS for efficient similarity matching
- **Reranking**: Fine-tuned mBERT model for answer quality
- **Fallback**: Groq LLM for answer generation when confidence is low
- **Web Interface**: Streamlit-based chat UI

---

## 2. Key Functions

### Core Functions

- **`answer_query(query, top_k=5)`**: Main function that processes user queries through the complete pipeline
- **`retrieve_candidates(query, top_k=5)`**: Semantic search using E5 embeddings and FAISS
- **`rerank(query, candidates)`**: Reranks candidates using fine-tuned mBERT model
- **`detect_language(query)`**: Automatically detects English or Chichewa input

### Administrative Functions

- **Corpus Management**: Tools to rebuild and clean the knowledge base
- **Embedding Generation**: Regenerate vector embeddings from updated data
- **System Validation**: Smoke tests to verify pipeline functionality

---

## 3. User Journeys

### Chatbot Web Interface

#### User Flow

1. **Access**: User navigates to the Streamlit web interface
2. **Input**: Types financial question in English or Chichewa
3. **Processing**: System automatically detects language and processes query
4. **Response**: Displays best answer with confidence score
5. **Debug**: Optional expandable section shows candidate answers and scores

#### Data Captured

- User question text
- Detected language (en/ny/und)
- Top 5 candidate answers with similarity scores
- Final selected answer with confidence
- Processing timestamps

### 4. Data Architecture

    # Core Data Files
    -models/corpus.json: Processed Q&A chunks with metadata
    -models/corpus_embeddings.npy: E5 embeddings for semantic search
    -models/faiss.index: FAISS vector index for fast retrieval
    -models/reranker/: Fine-tuned mBERT model files (optional)
    # Source Data
    -data/FINANCIAL LITERACY.pdf
    -Add more data sources to make it efficient and comprehensive
    
#### 5. Process Flow

┌───────────────────────────────────────────────────┐
│                    USER QUERY                     │
│         "Kodi ndisunge bwanji ndalama?"           │
└────────────────────┬──────────────────────────────┘
                     ▼
         ┌───────────────────────┐
         │  Language Detection   │
         │  Detected: Chichewa   │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Query Enhancement    │
         │  + bilingual keywords │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  E5 Embedding Model   │
         │  query: text → vector │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   FAISS Vector Index  │
         │   1000 docs embedded  │
         │   • 500 English       │
         │   • 500 Chichewa      │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Semantic Search      │
         │  Find 5 nearest docs  │
         │  (cross-lingual!)     │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Language Boosting    │
         │  Chichewa docs +30%   │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Confidence Check     │
         │  Score > threshold?   │
         └─────┬─────────────┬───┘
               │             │
        YES   ─┤             ├─ NO
               │             │
               ▼             ▼
    ┌──────────────┐  ┌─────────────────┐
    │ Direct Answe │  │  Groq LLM Gen   │
    │  (from doc)  │  │  (synthesize)   │
    └───────┬──────┘  └────────┬────────┘
            │                  │
            └────────┬─────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   FINAL RESPONSE      │
         │   (in Chichewa)       │
         └───────────────────────┘

