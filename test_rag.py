from app.scraper import RecursiveScraper
from app.chunker import TextChunker
from app.embeddings import EmbeddingModel
from app.vector_store import VectorStore
from app.rag_pipeline import RAGPipeline
import os


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    url = "https://moviesmod.town/download-the-night-agent-hindi-480p-720p-1080p/"
    # Scrape
    scraper = RecursiveScraper(url, max_depth=0, max_pages=1)
    docs = scraper.scrape()

    # Chunk
    chunker = TextChunker(chunk_size=300, overlap=20)
    chunks = chunker.chunk_documents(docs)

    # Embed
    embedder = EmbeddingModel()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.encode(texts)

    # Vector store
    dimension = embeddings.shape[1]
    store = VectorStore(dimension)
    store.add_embeddings(embeddings, chunks)

    # RAG
    rag = RAGPipeline(embedder, store)

    question = "What is MoviesMod?,why do we use it?"
    answer, sources = rag.answer_query(question)

    print("\nANSWER:\n")
    print(answer)

    print("\nSOURCES USED:")
    unique_sources = list(set([s["source_url"] for s in sources]))

    for s in unique_sources:
        print("-", s)