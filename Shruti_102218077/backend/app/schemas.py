from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class IngestRequest(BaseModel):
    csv_path: str = Field(..., description="Path to dataset CSV (or 'gdrive' to auto-download)")

class RecommendRequest(BaseModel):
    query: Optional[str] = None
    product_id: Optional[str] = None
    top_k: int = 10

class RecommendItem(BaseModel):
    uniq_id: str
    title: str
    brand: Optional[str]
    description: Optional[str]
    price: Optional[float]
    categories: Optional[str]
    image_url: Optional[str]
    score: float

class RecommendResponse(BaseModel):
    items: List[RecommendItem]

class GenRequest(BaseModel):
    title: str
    material: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    tone: str = "friendly"

class ClassifyRequest(BaseModel):
    image_url: str

class ClassifyResponse(BaseModel):
    predicted_label: str
    confidence: float

class AnalyticsResponse(BaseModel):
    n_rows: int
    n_brands: int
    price_stats: Dict[str, float | None]
    top_categories: List[Dict[str, int | str]]
