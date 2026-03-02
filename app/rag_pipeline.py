import os
from dotenv import load_dotenv
from groq import Groq


class RAGPipeline:
    def __init__(self, embedder, vector_store):
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")

        self.client = Groq(api_key=api_key)

        self.embedder = embedder
        self.vector_store = vector_store

    def answer_query(self, query, top_k=3):
        # Embed query
        query_embedding = self.embedder.encode([query])

        # Retrieve relevant chunks
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

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",  # free + fast model
                messages=[
                    {"role": "system", "content": "You are a factual assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=250
            )

            answer = response.choices[0].message.content
            return answer, retrieved_chunks

        except Exception as e:
            return f"⚠️ API Error: {str(e)}", retrieved_chunks