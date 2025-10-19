from fastapi import APIRouter, HTTPException
from ..schemas import RecommendRequest, RecommendResponse
from ..services.recommender import recommender

router = APIRouter(prefix="/recommend", tags=["recommend"])

@router.post("", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    if recommender.df is None:
        raise HTTPException(status_code=400, detail="Index not built. Call /ingest first.")
    if not req.query and not req.product_id:
        raise HTTPException(status_code=400, detail="Provide query or product_id.")
    if req.query:
        items = recommender.query(req.query, top_k=req.top_k)
    else:
        items = recommender.by_product(req.product_id, top_k=req.top_k)
    return {"items": items}
