from app.db.vector_store import VectorStoreManager

print("🔥 Loading FAISS vector store (singleton)")

vector_store = VectorStoreManager()

if not vector_store.load():
    raise RuntimeError("FAISS vector store not found")

print("✅ FAISS loaded into memory")
