from fastapi import APIRouter, HTTPException, Query
from ..services.recommender import recommender
from sklearn.cluster import KMeans
import numpy as np

router = APIRouter(prefix="/groups", tags=["nlp"])

@router.get("")
def groups(k: int = Query(6, ge=2, le=50)):
    if recommender.df is None or recommender.embeddings is None:
        raise HTTPException(status_code=400, detail="Ingest first.")
    X = recommender.embeddings
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(X)
    out = []
    for c in range(k):
        idxs = np.where(labels==c)[0][:10]
        items = [{
            "uniq_id": str(recommender.df.iloc[i]["uniq_id"]),
            "title": recommender.df.iloc[i]["title"],
            "brand": recommender.df.iloc[i]["brand"]
        } for i in idxs]
        out.append({"cluster": int(c), "size": int((labels==c).sum()), "samples": items})
    return {"clusters": out}
