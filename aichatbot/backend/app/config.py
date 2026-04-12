import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
load_dotenv()

class Settings(BaseSettings):
    """Manages application settings read from environment variables."""

    # # --- LLM Configuration (Ollama) ---
    # OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    # LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "llama3:8b-instruct")


    # Your other settings might be here
    OPENROUTER_API_KEY: str
    LLM_MODEL_NAME: str = "anthropic/claude-3-haiku"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    YOUR_SITE_URL: str = "http://localhost:8000"
    YOUR_APP_NAME: str = "My IT Assistant"

    # --- Embedding Model Configuration ---
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

    # --- Vector Store Configuration ---
    DOCS_DIRECTORY: str = os.getenv("DOCS_DIRECTORY", "docs")
    VECTOR_STORE_DIRECTORY: str = os.getenv("VECTOR_STORE_DIRECTORY", "vector_store")
    FAISS_INDEX_PATH: str = os.path.join(VECTOR_STORE_DIRECTORY, "faiss_index")
    TEXT_CHUNKS_PATH: str = os.path.join(VECTOR_STORE_DIRECTORY, "text_chunks.pkl")

    # --- RAG Configuration ---
    K_RETRIEVED_DOCS: int = int(os.getenv("K_RETRIEVED_DOCS", 4))
    MAX_TOKENS_GENERATED: int = int(os.getenv("MAX_TOKENS_GENERATED", 1024))

    # --- Text Splitting Configuration ---
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 200))
    
    # --- Email Service Configuration ---
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAIL_SENDER_ADDRESS: str = os.getenv("EMAIL_SENDER_ADDRESS", "")
    EMAIL_RECIPIENT_ADDRESS: str = os.getenv("EMAIL_RECIPIENT_ADDRESS", "")


    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
