from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI(title="Router Service")

services_db = {
    "github_api": {"service_id": "github_api", "cost_per_action": 1}
}
keys_db = {}
user_usage_db = {}
USER_FLAT_CAP = 100

class RequestActionRequest(BaseModel):
    user_id: str
    service_id: str
    action_type: str

class ResourceKeyCreate(BaseModel):
    service_id: str
    owner_user_id: str
    poolable: bool
    capacity_per_period: int

@app.post("/keys")
async def register_key(key: ResourceKeyCreate):
    key_id = str(uuid.uuid4())
    keys_db[key_id] = {
        "key_id": key_id,
        "service_id": key.service_id,
        "owner_user_id": key.owner_user_id,
        "poolable": key.poolable,
        "capacity_per_period": key.capacity_per_period,
        "used_this_period": 0
    }
    return {"key_id": key_id, "status": "created"}

@app.post("/request-action")
async def request_action(req: RequestActionRequest):
    usage_key = f"{req.user_id}_{req.service_id}"
    user_usage = user_usage_db.get(usage_key, {"user_id": req.user_id, "service_id": req.service_id, "used_this_period": 0})
    cost = services_db.get(req.service_id, {}).get("cost_per_action", 1)
    
    if user_usage["used_this_period"] + cost > USER_FLAT_CAP:
        return {"status": "queued", "reason": "user_cap_exceeded"}

    available_keys = [k for k in keys_db.values() if k["service_id"] == req.service_id and k["poolable"] and (k["used_this_period"] + cost <= k["capacity_per_period"])]
    
    if not available_keys:
        return {"status": "queued", "reason": "no_capacity"}

    available_keys.sort(key=lambda x: x["used_this_period"])
    chosen_key = available_keys[0]

    chosen_key["used_this_period"] += cost
    user_usage["used_this_period"] += cost
    user_usage_db[usage_key] = user_usage

    return {"key_id": chosen_key["key_id"], "status": "granted"}

@app.get("/health")
async def health():
    return {"status": "ok"}
