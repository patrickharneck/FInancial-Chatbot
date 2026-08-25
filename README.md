
# Project 1: Financial Literacy Chatbot (Africa-Focused)
    Objective
    Create a financial literacy dataset (English + one African language) and build a simple chatbot to answer common questions on savings, mobile money, credit, and fraud prevention.

Dataset Creation
    •	Compile FAQs and guides from central banks, NGOs, and donor toolkits.
    •	Curate 500–700 Q&A pairs in plain English.
    •	Translate ~100 Q&As into Swahili or Chichewa for multilingual proof of concept (can finalize languages upon discussion).
Tasks
    •	Collect and clean documents.
    •	Draft and structure Q&As in CSV/JSON.
    •	Translate and validate a subset.
    •	Fine-tune a small model (TinyLlama/mBERT).
    •	Build a prototype chatbot (Streamlit/Gradio).
Outputs
    •	Financial literacy dataset (English + African language).
    •	Dataset card (sources, scope, metadata).
    •	Fine-tuned model with evaluation results.
    •	Chatbot demo answering financial FAQs.

# Project Overview
This project provides a financial literacy chatbot that answers common questions about savings, mobile money, credit, and fraud prevention, with support for English and Chichewa. It uses a retrieval + reranking pipeline with e5-embedder.
**Fin-Chat** is an AI-powered chatbot designed to help users improve their **financial literacy** through interactive, multilingual question-answering.  
It retrieves and explains key financial concepts from curated documents (like PDF textbooks, guides, and articles) using **Retrieval-Augmented Generation (RAG)**.

Whether you’re learning about and want to know **budgeting, saving, investing,**, **Fraud**or **debt management**, Fin-Chat serves up clear, contextual answers — with support for **Chichewa** and **English**.



## ⚙️ Features

✅ **RAG-based knowledge retrieval** – Combines document embeddings and generative AI for accurate responses.  
✅ **Multilingual Support** – English 🇬🇧 + Chichewa 🇲🇼.  
✅ **FAISS Vector Indexing** – Fast, semantic retrieval for large financial datasets.  
✅ **PDF / DOCX ingestion** – Add your own financial materials and Fin-Chat will learn from them.  
✅ **Contextual AI responses** – Long, detailed, and user-focused explanations.   

# 1. Prerequisites
- **Python 3.10+** (recommended)
- **4GB+ Ram**

# 🚀 Setup Instructions

```
# Clone the repo
git clone https://github.com/Microsave-Consulting/AfricaInterns_01_FinancialLiteracyChatbot-.git
cd fin-chat

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the chatbot
python app/chatbot.py
```

# Tech Stack
| Component | Description |
|------------|-------------|
| **Python 3.10+** | Core language |
| **LangChain / LlamaIndex** | RAG pipeline |
| **FAISS** | Vector store for embeddings |
| **Hugging Face Transformers** | Text embedding and generation |
| **Streamlit / FastAPI** | Chat interface |
| **Gloq API** | Hosted LLM services for text generation|`
|**Google tanslator** | Handles English ↔ Chichewa translations


# Project Structure
Fin-Chat/
│
├── app/
│   ├── chatbot.py             # Main chatbot logic
│   ├── rag_retriever.py       # Handles vector retrieval
│   ├── language_utils.py      # Language and text helpers
│   ├── evaluation.py          # Model and retrieval evaluation tools
│   ├── config.py              # Configuration settings and constants
│   ├── fallback_response.py   # Handles default / fallback responses
│   ├── llm_client.py          # Connects to LLM APIs (OpenAI, local, etc.)
│   └── prompt_builder.py      # Builds structured prompts for LLM
│
├── data/                      # Financial literacy materials (PDFs, etc.)
│
├── models/                    # FAISS and embedding models stored here
│
├── notebooks/                 # Jupyter notebooks (e.g. document loading & corpus creation)
│   └── financial_literacy_chatbot.ipynb
│
├── requirements.txt
├── design.md                  # System architecture and design overview
├── Manual.md                  # User manual and usage instructions
└── README.md