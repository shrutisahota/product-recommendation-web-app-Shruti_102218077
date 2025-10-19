from fastapi import APIRouter, HTTPException
from ..schemas import AnalyticsResponse
from ..services.recommender import recommender

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("", response_model=AnalyticsResponse)
def analytics():
    if recommender.df is None:
        raise HTTPException(status_code=400, detail="Ingest first.")
    df = recommender.df
    price = df["price"].dropna()
    price_stats = {
        "min": float(price.min()) if len(price) else None,
        "max": float(price.max()) if len(price) else None,
        "mean": float(price.mean()) if len(price) else None,
        "median": float(price.median()) if len(price) else None,
    }
    cat_counts = (df["categories"].fillna("Unknown")
                    .str.split(",").explode().str.strip()
                    .value_counts().head(10))
    top_categories = [{"category": k, "count": int(v)} for k,v in cat_counts.items()]
    n_brands = df["brand"].fillna("Unknown").nunique()
    return {
        "n_rows": int(len(df)),
        "n_brands": int(n_brands),
        "price_stats": price_stats,
        "top_categories": top_categories
    }
