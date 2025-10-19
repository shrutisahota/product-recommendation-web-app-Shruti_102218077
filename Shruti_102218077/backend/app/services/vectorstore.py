import numpy as np
from ..config import settings

class FaissStore:
    def __init__(self, dim: int):
        import faiss
        self.faiss = faiss
        self.index = self.faiss.IndexFlatIP(dim)
        self.ids = []

    def add(self, embeddings: np.ndarray, ids: list[int]):
        self.index.add(embeddings.astype('float32'))
        self.ids.extend(ids)

    def search(self, query_vecs: np.ndarray, top_k=10):
        D, I = self.index.search(query_vecs.astype('float32'), top_k)
        return D, I

class PineconeStore:
    def __init__(self, dim: int):
        from pinecone import Pinecone, ServerlessSpec
        api_key = settings.PINECONE_API_KEY
        if not api_key:
            raise RuntimeError("PINECONE_API_KEY not set")
        pc = Pinecone(api_key=api_key)
        index_name = settings.PINECONE_INDEX
        existing = [i.name for i in pc.list_indexes()]
        if index_name not in existing:
            pc.create_index(name=index_name, dimension=dim, metric="cosine",
                            spec=ServerlessSpec(cloud="aws", region=settings.PINECONE_ENV or "us-east-1"))
        self.index = pc.Index(index_name)
        self.ids = []

    def add(self, embeddings: np.ndarray, ids: list[int]):
        vectors = [{"id": str(i), "values": vec.tolist()} for i, vec in zip(ids, embeddings)]
        self.index.upsert(vectors=vectors)
        self.ids.extend(ids)

    def search(self, query_vecs: np.ndarray, top_k=10):
        q = query_vecs[0].tolist()
        res = self.index.query(vector=q, top_k=top_k, include_values=False, include_metadata=False)
        # Convert cosine distance to similarity approximation: similarity ~ 1 - distance
        import numpy as np
        sims = np.array([[m.score for m in res.matches]], dtype="float32")
        ids = np.array([[int(m.id) for m in res.matches]], dtype="int32")
        return sims, ids

class VectorStore:
    def __init__(self, dim: int):
        backend = settings.VECTOR_BACKEND.lower()
        if backend == "pinecone":
            self.impl = PineconeStore(dim)
        else:
            self.impl = FaissStore(dim)

    def add(self, emb, ids):
        self.impl.add(emb, ids)

    def search(self, q, top_k=10):
        return self.impl.search(q, top_k)
