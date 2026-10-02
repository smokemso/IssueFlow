from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Executor Service")

class BulkActionRequest(BaseModel):
    issue_ids: List[str]
    action: str
    user_id: str

@app.post("/bulk-action")
async def execute_bulk_action(request: BulkActionRequest):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post("http://router:8000/request-action", json={
                "user_id": request.user_id,
                "service_id": "github_api",
                "action_type": request.action
            })
            router_response = resp.json()
        except Exception as e:
            logger.error(f"Failed to contact router: {e}")
            return {"status": "error", "message": "Router unavailable"}
        
    if router_response.get("status") != "granted":
        logger.info(f"Action queued: {router_response}")
        return {"status": "queued"}
    
    key_id = router_response.get("key_id")
    logger.info(f"WOULD DO: Using key {key_id} to perform '{request.action}' on issues {request.issue_ids}")
    return {"status": "success", "executed_action": request.action, "key_used": key_id}

@app.get("/health")
async def health():
    return {"status": "ok"}
