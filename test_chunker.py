from app.scraper import RecursiveScraper
from app.chunker import TextChunker

if __name__ == "__main__":
    url = "https://code.visualstudio.com/"    
    scraper = RecursiveScraper(url, max_depth=0, max_pages=1)
    docs = scraper.scrape()

    chunker = TextChunker(chunk_size=300, overlap=20)
    chunks = chunker.chunk_documents(docs)

    print("Total chunks:", len(chunks))
    print("=" * 80)
    print(chunks[0]["text"][:500])