import httpx
from pydantic import BaseModel, Field
from pydantic import ValidationError 
from pathlib import Path
import json

import time, logging, functools, httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base = Path("data")
base.mkdir(parents=True, exist_ok=True)

#Validate the response with Pydantic
class Todo(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool 

def retry(times):
    def decorator(func):
        def inner(*args, **kwargs):
            for attempt in range (1, times+1):
                try:
                    return func(*args, **kwargs)
                except httpx.TimeoutException as e:
                    if attempt == times:
                        raise
                    print(e)
        return inner
    return decorator
    


@retry(times=3)
def fetch_todos(client, user_id):
    r = client.get("/todos", params={"userId": user_id})
    r.raise_for_status()
    return r.json()          # a list of dicts

def summarize_user(user_id):
    with httpx.Client(base_url="https://jsonplaceholder.typicode.com", timeout=5.0) as client:
        raw_todos = fetch_todos(client, user_id)

    valid = []
    for item in raw_todos:
        try:
            valid.append(Todo.model_validate(item))
        except ValidationError as e:
            logger.warning("skipping todo %s: %s", item.get("id"), e)

    completed = sum(1 for t in valid if t.completed)
    pending = len(valid) - completed
    
    # write JSON to data/summary_<user_id>.json
    result = {"user_id": user_id, "completed": completed, "pending": pending}
    json_path = base / f"summary_{user_id}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    # log: fetched N, valid N, completed N
    logger.info("fetched %d, valid %d, completed %d",
        len(raw_todos), len(valid), completed)

summarize_user(1)
summarize_user(2)