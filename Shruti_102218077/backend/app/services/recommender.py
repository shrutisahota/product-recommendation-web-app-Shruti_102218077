import pandas as pd
from .text_embed import embed_texts
from .vectorstore import VectorStore

class Recommender:
    def __init__(self):
        self.df: pd.DataFrame|None = None
        self.vs: VectorStore|None = None
        self.embeddings = None

    def ingest(self, df: pd.DataFrame):
        self.df = df.reset_index(drop=True)
        texts = df["text_blob"].fillna("").tolist()
        self.embeddings = embed_texts(texts)
        self.vs = VectorStore(dim=self.embeddings.shape[1])
        self.vs.add(self.embeddings, list(range(len(self.df))))

    def _pack(self, idx: int, score: float):
        row = self.df.iloc[idx]
        return {
            "uniq_id": str(row.get("uniq_id")),
            "title": row.get("title"),
            "brand": row.get("brand"),
            "description": row.get("description"),
            "price": None if pd.isna(row.get("price")) else float(row.get("price")),
            "categories": row.get("categories"),
            "image_url": (row.get("images") or "").split(",")[0].strip(),
            "score": float(score),
        }

    def query(self, text: str, top_k=10):
        q = embed_texts([text])
        D, I = self.vs.search(q, top_k=top_k)
        sims = D[0]; ids = I[0]
        items = [self._pack(int(i), float(sims[k])) for k,i in enumerate(ids) if i!=-1]
        return items

    def by_product(self, uniq_id: str, top_k=10):
        if self.df is None: return []
        hit = self.df.index[self.df["uniq_id"].astype(str)==str(uniq_id)]
        if len(hit)==0:
            return self.query(uniq_id, top_k)
        idx = int(hit[0])
        vec = self.embeddings[idx:idx+1]
        D, I = self.vs.search(vec, top_k=top_k+1)
        sims, ids = D[0], I[0]
        out = []
        for s,i in zip(sims, ids):
            if i==-1 or i==idx: 
                continue
            out.append(self._pack(int(i), float(s)))
            if len(out)>=top_k: break
        return out

recommender = Recommender()
