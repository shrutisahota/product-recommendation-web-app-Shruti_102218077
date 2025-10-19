from transformers import pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from ..config import settings

_pipe = None
_lc_llm = None

def _init():
    global _pipe, _lc_llm
    model = settings.GENAI_MODEL
    _pipe = pipeline("text2text-generation", model=model)
    _lc_llm = HuggingFacePipeline(pipeline=_pipe)

def generate_description(title: str, material: str|None, category: str|None, brand: str|None, tone="friendly"):
    global _lc_llm
    if _lc_llm is None:
        _init()
    prompt = (
        f"Write a {tone} 2-3 sentence product description for:\n"
        f"Title: {title}\n"
        f"Brand: {brand or 'Unknown'}\n"
        f"Material: {material or 'Not specified'}\n"
        f"Category: {category or 'Furniture'}\n"
        f"Highlight comfort, design, and use-cases in plain English."
    )
    return _lc_llm.invoke(prompt).strip()
