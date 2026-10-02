from fastapi import FastAPI, Depends, Header
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Backend Service")

class BulkActionRequest(BaseModel):
    issue_ids: List[str]
    action: str

def verify_token(authorization: Optional[str] = Header(None)):
    return "fake_user_123"

@app.get("/issues")
async def list_issues(category: Optional[str] = None):
    issues = [
        {"id": "1", "title": "App crashes on start", "category": "bug", "confidence": 0.9},
        {"id": "2", "title": "Add dark mode", "category": "feature", "confidence": 0.8}
    ]
    if category:
        issues = [i for i in issues if i["category"] == category]
    return issues

@app.post("/issues/bulk-action")
async def bulk_action(request: BulkActionRequest, user_id: str = Depends(verify_token)):
    return {"job_id": "job_123abc", "status": "queued"}

@app.get("/health")
async def health():
    return {"status": "ok"}
