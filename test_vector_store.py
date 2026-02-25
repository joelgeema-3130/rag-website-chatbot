from app.scraper import RecursiveScraper
from app.chunker import TextChunker
from app.embeddings import EmbeddingModel
from app.vector_store import VectorStore
import numpy as np
import os


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    # Step 1: Scrape
    scraper = RecursiveScraper(
        "https://en.wikipedia.org/wiki/Wikipedia",
        max_depth=0,
        max_pages=1
    )
    docs = scraper.scrape()

    # Step 2: Chunk
    chunker = TextChunker(chunk_size=300, overlap=20)
    chunks = chunker.chunk_documents(docs)

    print("Total chunks:", len(chunks))

    # Step 3: Embed
    embedder = EmbeddingModel()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.encode(texts)

    print("Embedding shape:", embeddings.shape)

    # Step 4: FAISS
    dimension = embeddings.shape[1]
    store = VectorStore(dimension)
    store.add_embeddings(embeddings, chunks)

    # Step 5: Test search
    query = "What is Wikipedia?"
    query_embedding = embedder.encode([query])

    results = store.search(query_embedding, top_k=3)

    print("\nTop results:")
    for r in results:
        print("Source:", r["source_url"])
        print(r["text"][:200])
        print("-" * 50)

    # Save index
    store.save()