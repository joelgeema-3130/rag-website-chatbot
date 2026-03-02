# 🌐 RAG-Powered Website Chatbot

## 📌 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG) chatbot** that can ingest any given website URL, recursively scrape its content, and answer user questions strictly based on the collected information.

The system combines:

- Recursive web scraping
- Intelligent text chunking
- Local semantic embeddings
- FAISS vector search
- Gemini LLM (for grounded answer generation)
- Streamlit frontend interface

The goal is to build a **cost-efficient, production-style AI system** that minimizes hallucination and ensures answers are grounded in real website content.

---

## 🧠 Solution Approach

The system follows a structured RAG pipeline:

Website URL\\
↓
Recursive Scraper (domain-restricted)
↓
HTML Cleaning & Structured Extraction
↓
Sentence-aware Chunking (with overlap)
↓
Local Embeddings (Sentence Transformers)
↓
FAISS Vector Database
↓
Top-K Semantic Retrieval
↓
Gemini LLM (Grounded Prompt)
↓
Answer + Source Attribution


### Key Design Decisions

- **Local embeddings** to reduce API cost
- **FAISS for fast similarity search**
- **Top-k retrieval (default = 3)** to control context size
- **Low temperature (0.2)** to improve factual grounding
- **Strict prompt instructions** to reduce hallucination
- **Session-based caching in Streamlit**

This ensures:
- Low API usage
- High factual accuracy
- Scalable design
- Clean separation of components

---

## ⚙️ Features

- Domain-restricted recursive scraping
- Structured extraction (headings, paragraphs, tables)
- Sentence-aware chunking with overlap
- Semantic search using FAISS
- Gemini-powered grounded responses
- Source citation display
- Response latency measurement
- Clean Streamlit UI

---

## 🛠️ Tech Stack

- Python 3.10+
- Sentence Transformers
- FAISS (CPU)
- Google Gemini API (`google-genai`)
- Streamlit
- BeautifulSoup
- Requests

---

## 📦 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/joelgeema-3130/rag-website-chatbot.git
cd rag-website-chatbot



# Create a README.md file for the RAG Website Chatbot project

import pypandoc

readme_content = """
# 🌐 RAG-Powered Website Chatbot  
### Retrieval-Augmented Generation over Live Websites using FAISS + OpenAI GPT (Groq)

---

## 🚀 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG) based chatbot** that:

- Accepts any public website URL  
- Recursively scrapes internal links  
- Extracts and cleans structured & unstructured content  
- Converts content into vector embeddings  
- Stores embeddings in FAISS  
- Retrieves relevant chunks at query time  
- Generates grounded responses using OpenAI GPT (via Groq API)  

The system reduces hallucination by ensuring answers are generated strictly from retrieved website context.

---

## 🧠 Problem Statement

Create a chatbot that can ingest any given URL and recursively scrape relevant content from linked pages, 
then use Retrieval-Augmented Generation (RAG) to answer user questions accurately based on the collected content. 
Ensure minimal latency and robust handling of structured and unstructured data.

---

## 🏗️ System Architecture

### 🔄 Workflow Pipeline

1. User inputs a website URL  
2. Recursive scraper collects internal links  
3. HTML content is extracted and cleaned  
4. Text is split into semantic chunks  
5. Chunks converted to embeddings  
6. Embeddings stored in FAISS index  
7. User asks a question  
8. Query embedding generated  
9. Top-K similar chunks retrieved  
10. GPT-4 (Groq) generates grounded answer  

---

## 🧩 Tech Stack

| Component             |               Technology |
|-----------------------|--------------------------|
| Frontend + Backend    |                Streamlit |
| LLM                   |      OpenAI via Groq API |
| Vector Store          |                    FAISS |
| Embeddings            |     LLM-based embeddings |
| Web Scraping          | Requests + BeautifulSoup |
| Language              |                   Python |

---



## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash

git clone https://github.com/joelgeema-3130/rag-website-chatbot.git
cd rag-website-chatbot

### 2️⃣ Create Virtual Environment
