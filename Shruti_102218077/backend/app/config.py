import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    VECTOR_BACKEND = os.getenv("VECTOR_BACKEND", "faiss")
    SENTENCE_MODEL = os.getenv("SENTENCE_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    GENAI_MODEL    = os.getenv("GENAI_MODEL", "google/flan-t5-small")
    CV_BACKBONE    = os.getenv("CV_BACKBONE", "resnet50")

    # Pinecone
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV     = os.getenv("PINECONE_ENV")
    PINECONE_INDEX   = os.getenv("PINECONE_INDEX", "ikarus-products")

    # Qdrant (placeholder)
    QDRANT_URL     = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

settings = Settings()
