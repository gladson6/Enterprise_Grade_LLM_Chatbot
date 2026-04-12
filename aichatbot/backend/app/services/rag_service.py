from app.db.vector_store import VectorStoreManager
from app.models.schemas import ChatMessage
from typing import List

class RAGService:
    """
    The Retrieval-Augmented Generation (RAG) service.
    """
    def __init__(self, vector_store_manager: VectorStoreManager):
        self.vector_store = vector_store_manager
        # This check now provides a much more helpful error message.
        if not self.vector_store.load():
             raise RuntimeError(
                 "\n\n--- VECTOR STORE NOT FOUND ---\n"
                 "The FAISS vector store is missing. Please build it before starting the server.\n"
                 "From your project's ROOT directory (the one containing 'frontend' and 'backend'), run the following command:\n\n"
                 "python backend/app/db/vector_store.py\n"
             )

    def get_relevant_context(self, query: str):
        """Retrieves relevant document chunks and their sources."""
        retrieved_docs = self.vector_store.search(query)
        context_str = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
        sources = list(set([doc.metadata.get("source", "Unknown") for doc in retrieved_docs]))
        return context_str, sources
