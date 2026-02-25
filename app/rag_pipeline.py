import os
from dotenv import load_dotenv
from google import genai


class RAGPipeline:
    def __init__(self, embedder, vector_store):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        # Initialize Gemini client
        self.client = genai.Client(api_key=api_key)

        self.embedder = embedder
        self.vector_store = vector_store

    def answer_query(self, query, top_k=3):
        # 1️⃣ Embed query
        query_embedding = self.embedder.encode([query])

        # 2️⃣ Retrieve relevant chunks
        retrieved_chunks = self.vector_store.search(query_embedding, top_k=top_k)

        context = "\n\n".join(
            [f"Source: {c['source_url']}\n{c['text']}" for c in retrieved_chunks]
        )

        prompt = f"""
            You are a precise and factual AI assistant.

            Answer ONLY using the provided context.
            Do NOT use outside knowledge.
            If the answer is not found, say:
            "Answer not found in the provided website."

            Context:
            {context}

            Question:
            {query}
        """

        # 3️⃣ Call Gemini
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 250
            }
        )

        return response.text, retrieved_chunks