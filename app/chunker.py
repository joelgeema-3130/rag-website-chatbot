import re


class TextChunker:
    def __init__(self, chunk_size=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_documents(self, documents):
        """
        documents = [
            {"url": "...", "content": "..."}
        ]
        """
        chunks = []
        chunk_id = 0

        for doc in documents:
            sentences = self._split_into_sentences(doc["content"])
            current_chunk = []
            current_length = 0

            for sentence in sentences:
                sentence_length = len(sentence.split())

                if current_length + sentence_length > self.chunk_size:
                    chunk_text = " ".join(current_chunk)
                    chunks.append({
                        "chunk_id": chunk_id,
                        "text": chunk_text,
                        "source_url": doc["url"]
                    })
                    chunk_id += 1

                    # overlap
                    current_chunk = current_chunk[-self.overlap:]
                    current_length = sum(len(s.split()) for s in current_chunk)

                current_chunk.append(sentence)
                current_length += sentence_length

            if current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "source_url": doc["url"]
                })
                chunk_id += 1

        return chunks

    def _split_into_sentences(self, text):
        # Simple sentence split
        sentences = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sentences if s.strip()]