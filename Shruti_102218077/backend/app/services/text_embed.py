from sentence_transformers import SentenceTransformer
from ..config import settings

_model = None

def get_text_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.SENTENCE_MODEL)
    return _model

def embed_texts(texts):
    model = get_text_model()
    return model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
