from fastapi import APIRouter, HTTPException
from ..schemas import IngestRequest
from ..utils.io import load_products
from ..services.recommender import recommender
import os

router = APIRouter(prefix="/ingest", tags=["ingest"])

GDRIVE_URL = "https://drive.google.com/uc?export=download&id=1uD1UMXT2-13GQkb_H9NmEOyUVI-zKyl6"

@router.post("")
def ingest(req: IngestRequest):
    try:
        path = req.csv_path
        if req.csv_path.strip().lower() == "gdrive":
            os.makedirs("/content/data", exist_ok=True)
            csv_out = "/content/data/products.csv"
            try:
                import gdown
                gdown.download(GDRIVE_URL, csv_out, quiet=False)
            except Exception:
                import requests
                r = requests.get(GDRIVE_URL)
                open(csv_out, "wb").write(r.content)
            path = csv_out
        df = load_products(path)
        if len(df)==0:
            raise HTTPException(status_code=400, detail="CSV has no rows.")
        recommender.ingest(df)
        return {"ok": True, "rows": len(df), "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
