import streamlit as st
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scraper import RecursiveScraper
from app.chunker import TextChunker
from app.embeddings import EmbeddingModel
from app.vector_store import VectorStore
from app.rag_pipeline import RAGPipeline


st.set_page_config(page_title="RAG Website Chatbot", layout="wide")

st.title("🌐 RAG-Powered Website Chatbot")
st.markdown("Ask questions based only on a website's content.")


# ---------------------------
# SESSION STATE INITIALIZATION
# ---------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "embedder" not in st.session_state:
    st.session_state.embedder = None

if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None


# ---------------------------
# URL INPUT
# ---------------------------

url = st.text_input("Enter Website URL:")

if st.button("🔍 Process Website"):

    if not url:
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Scraping and processing website..."):

            scraper = RecursiveScraper(url, max_depth=1, max_pages=10)
            docs = scraper.scrape()

            chunker = TextChunker(chunk_size=300, overlap=20)
            chunks = chunker.chunk_documents(docs)

            embedder = EmbeddingModel()
            texts = [chunk["text"] for chunk in chunks]
            embeddings = embedder.encode(texts)

            dimension = embeddings.shape[1]
            store = VectorStore(dimension)
            store.add_embeddings(embeddings, chunks)

            rag = RAGPipeline(embedder, store)

            st.session_state.vector_store = store
            st.session_state.embedder = embedder
            st.session_state.rag_pipeline = rag

        st.success("Website processed successfully! You can now ask questions.")


# ---------------------------
# QUESTION INPUT
# ---------------------------

if st.session_state.rag_pipeline:

    question = st.text_input("Ask a question about the website:")

    if st.button("💬 Get Answer") and question:

        with st.spinner("Generating answer..."):

            start_time = time.time()

            answer, sources = st.session_state.rag_pipeline.answer_query(question)

            latency = time.time() - start_time

        st.subheader("📌 Answer")
        st.write(answer)

        st.subheader("📚 Sources Used")

        unique_sources = list(set([s["source_url"] for s in sources]))
        for s in unique_sources:
            st.write(f"- {s}")

        st.caption(f"⏱ Response Time: {latency:.2f} seconds")