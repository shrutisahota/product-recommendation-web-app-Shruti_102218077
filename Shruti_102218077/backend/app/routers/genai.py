from fastapi import APIRouter
from ..schemas import GenRequest
from ..services.llm import generate_description

router = APIRouter(prefix="/generate", tags=["genai"])

@router.post("")
def generate(req: GenRequest):
    text = generate_description(req.title, req.material, req.category, req.brand, req.tone)
    return {"description": text}
