from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Classifier Service")

class ClassifyRequest(BaseModel):
    title: str
    body: str

class ClassifyResponse(BaseModel):
    category: str
    confidence: float

@app.post("/classify", response_model=ClassifyResponse)
async def classify(request: ClassifyRequest):
    return {"category": "bug", "confidence": 0.85}

@app.get("/health")
async def health():
    return {"status": "ok"}
