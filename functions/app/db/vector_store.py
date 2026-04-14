import os
import pickle
import faiss
import numpy as np
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# The slow import is now moved inside the function to speed up startup
# from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

class SafeTextLoader(TextLoader):
    def __init__(self, file_path, **kwargs):
        super().__init__(file_path, encoding="utf-8", **kwargs)

    def load(self):
        try:
            return super().load()
        except UnicodeDecodeError:
            with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            return [{"page_content": text, "metadata": {"source": self.file_path}}]

class VectorStoreManager:
    def __init__(self):
        self.index_path = settings.FAISS_INDEX_PATH
        self.chunks_path = settings.TEXT_CHUNKS_PATH
        self._embeddings_model = None
        self.index = None
        self.text_chunks = None

    def _get_embeddings_model(self):
        if self._embeddings_model is None:
            # Import the library only when it's first needed
            from langchain_huggingface import HuggingFaceEmbeddings
            print("Lazily loading HuggingFaceEmbeddings model from local files...")
            
            # THIS IS THE KEY CHANGE: Load the model from the local directory
            # that we copied into the container.
            self._embeddings_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",

                model_kwargs={'device': 'cpu'}
            )
            print("Embeddings model loaded.")
        return self._embeddings_model

    def load(self):
        if not os.path.exists(self.index_path) or not os.path.exists(self.chunks_path):
            return False
        print("Loading FAISS index and text chunks...")
        self.index = faiss.read_index(self.index_path)
        with open(self.chunks_path, "rb") as f:
            self.text_chunks = pickle.load(f)
        print("Vector store loaded successfully.")
        return True
    
    # ... The rest of the file (search, build_and_save, etc.) remains unchanged ...
    def search(self, query: str, k: int = 5):

        if self.index is None or self.text_chunks is None:
            raise RuntimeError("Vector store is not loaded. Call load() first.")
        embeddings_model = self._get_embeddings_model()
        query_embedding = embeddings_model.embed_query(query)
        query_embedding_np = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query_embedding_np, k)
        print(f"🔎 FAISS search returned {len(indices[0])} chunks (k={k})")

        return [self.text_chunks[i] for i in indices[0]]

    def _load_documents(self):
        print(f"Loading documents from '{settings.DOCS_DIRECTORY}'...")
        try:
            loader = DirectoryLoader(
                settings.DOCS_DIRECTORY,
                glob="**/*",
                loader_map={".pdf": PyPDFLoader, ".txt": SafeTextLoader, ".md": SafeTextLoader},
                show_progress=True
            )
        except TypeError:
            print("⚠️ loader_map not supported. Falling back to loader_cls=SafeTextLoader")
            loader = DirectoryLoader(
                settings.DOCS_DIRECTORY, glob="**/*", loader_cls=SafeTextLoader
            )
        documents = loader.load()
        print(f"Loaded {len(documents)} document(s).")
        return documents

    def _split_text(self, documents):
        print("Splitting documents into text chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} text chunks.")
        return chunks

    def build_and_save(self):
        if not os.path.exists(settings.VECTOR_STORE_DIRECTORY):
            os.makedirs(settings.VECTOR_STORE_DIRECTORY)
        documents = self._load_documents()
        if not documents:
            print("No documents found. Aborting vector store build.")
            return
        self.text_chunks = self._split_text(documents)
        print("Generating embeddings for text chunks...")
        embeddings_model = self._get_embeddings_model()
        embeddings = embeddings_model.embed_documents(
            [chunk.page_content for chunk in self.text_chunks]
        )
        embedding_dim = len(embeddings[0])
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(np.array(embeddings, dtype=np.float32))
        print(f"Saving FAISS index to '{self.index_path}'...")
        faiss.write_index(self.index, self.index_path)
        print(f"Saving text chunks to '{self.chunks_path}'...")
        with open(self.chunks_path, "wb") as f:
            pickle.dump(self.text_chunks, f)
        print("\n✅ Vector store built and saved successfully.\n")

if __name__ == "__main__":
    manager = VectorStoreManager()
    manager.build_and_save()

