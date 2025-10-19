from fastapi import FastAPI
from .routers import ingest, recommend, genai, classify, analytics, groups
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Shruti_102218077 AI/ML Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

app.include_router(ingest.router)
app.include_router(recommend.router)
app.include_router(genai.router)
app.include_router(classify.router)
app.include_router(analytics.router)
app.include_router(groups.router)

@app.get("/")
def root():
    return {"ok": True, "service": "Shruti_102218077 Backend"}
