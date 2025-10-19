from fastapi import APIRouter
from ..schemas import ClassifyRequest, ClassifyResponse
from ..services.cv_model import predict_from_metadata
from ..services.recommender import recommender

router = APIRouter(prefix="/classify", tags=["cv"])

@router.post("", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    title, cats = None, None
    if recommender.df is not None and "images" in recommender.df.columns:
        df = recommender.df
        hit = df.index[df["images"].astype(str).str.contains(req.image_url, na=False)]
        if len(hit)>0:
            row = df.iloc[int(hit[0])]
            title, cats = row.get("title"), row.get("categories")
    label, conf = predict_from_metadata(title or "", cats or "")
    return {"predicted_label": label, "confidence": conf}
