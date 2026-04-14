from app.db.vector_store import VectorStoreManager
from app.models.schemas import ChatMessage
from typing import List
import time



class RAGService:
    """
    The Retrieval-Augmented Generation (RAG) service.
    """

    def __init__(self, vector_store):
        self.vector_store = vector_store

        if not self.vector_store.load():
            raise RuntimeError(
                "\n\n--- VECTOR STORE NOT FOUND ---\n"
                "The FAISS vector store is missing. Please build it before starting the server.\n"
                "From your project's ROOT directory, run:\n\n"
                "python backend/app/db/vector_store.py\n"
            )

        # ✅ Cache must be initialized here
        self._cache = {}
        self._cache_ttl = 60  # seconds

    def get_relevant_context(self, query: str, max_chars: int = 2000):
        now = time.time()

        # 1️⃣ Cache hit
        if query in self._cache:
            cached_time, cached_result = self._cache[query]
            if now - cached_time < self._cache_ttl:
                print("⚡ RAG cache hit")
                return cached_result
            else:
                del self._cache[query]  # expired

        # 2️⃣ Cache miss → normal RAG
        retrieved_docs = self.vector_store.search(query)

        context_parts = []
        total_chars = 0
        sources = set()

        for doc in retrieved_docs:
            text = doc.page_content.strip()
            if not text:
                continue

            if total_chars + len(text) > max_chars:
                context_parts.append(text[: max_chars - total_chars])
                break

            context_parts.append(text)
            total_chars += len(text)
            sources.add(doc.metadata.get("source", "Unknown"))

        context_str = "\n\n---\n\n".join(context_parts)
        result = (context_str, list(sources))

        # 3️⃣ Store in cache
        self._cache[query] = (now, result)
        print("📦 RAG cache stored")
        print(f"🧠 Final context size: {len(context_str)} chars")
        print(f"📄 Sources used: {len(sources)}")

        return result


      