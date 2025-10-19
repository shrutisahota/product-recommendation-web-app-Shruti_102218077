# Shruti_102218077 – AI/ML Product Recommendation App

This repo contains a **FastAPI backend** + a **React frontend** for a furniture product recommendation system (ML/NLP/CV/GenAI) with a vector store.

## Quick Start (Colab Backend)

1. Upload this folder to Colab or mount Drive.
2. Open `run_colab_backend.ipynb` and run all cells.
3. Copy the **public ngrok URL** printed in the notebook.
4. Call `POST /ingest` with `{"csv_path":"gdrive"}` to auto-download the dataset.
5. Use `/recommend`, `/generate`, `/analytics`, `/groups` from your frontend via the public URL.

### Sample curl
```
curl -X POST <PUBLIC_URL>/recommend -H "Content-Type: application/json" -d '{"query":"modern wooden chair","top_k":5}'
```

## Local Run (optional)
```
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Deploy (Render/Railway/HF Spaces)
- Use `Dockerfile` or `Procfile`.
- Set `PORT` env if required by platform.
- Expose `uvicorn app.main:app`.

## LangChain Usage
- GenAI descriptions are generated via a `transformers` pipeline **wrapped by LangChain** (`HuggingFacePipeline`) in `app/services/llm.py`.

## Vector DB Options
- Default: **FAISS (local)**.
- Optional: **Pinecone** — set `VECTOR_BACKEND=pinecone` and provide `PINECONE_API_KEY`, `PINECONE_ENV`, `PINECONE_INDEX` in `.env`. Implemented in `app/services/vectorstore.py`.

## NLP Grouping
- Endpoint: `GET /groups?k=8` returns cluster groups using **KMeans** on sentence embeddings.

## CV Model
- Backend loads TorchScript model from `CV_MODEL_PATH` (default `/content/models/cv.pt`) if present; falls back to metadata heuristic if absent.
- Train and export the model using `model_training.ipynb`.

