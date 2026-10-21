import httpx
from pydantic import BaseModel, Field
from pydantic import ValidationError    

#First GET request
r = httpx.get("https://jsonplaceholder.typicode.com/todos/1")
print(r.status_code)
print(r.headers["content-type"])
print(r.json())

#Query parameter
r = httpx.get("https://jsonplaceholder.typicode.com/todos", params={"userId": 1})
print(len(r.json()))
print(r.url)

#Timeouts
try:
    httpx.get(r.url, timeout=0.001)
except httpx.TimeoutException as e:    
    print(e)

#Reuse a client
import time, logging, functools, httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_transient(e):
    if isinstance(e, (httpx.TimeoutException, httpx.ConnectError)):
        return True
    if isinstance(e, httpx.HTTPStatusError):
        return e.response.status_code == 429 or e.response.status_code >= 500
    return False

def retry(times, delay=0.5):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if not is_transient(e) or attempt == times:
                        raise
                    wait = delay * 2 ** (attempt - 1)
                    logger.warning("attempt %d failed: %s, retrying in %.1fs", attempt, e, wait)
                    time.sleep(wait)
        return inner
    return decorator

@retry(times=3)
def fetch(client, todo_id):
    r = client.get(f"/todos/{todo_id}")
    r.raise_for_status()
    return r.json()

ids = [1, 2, 3, 5]
with httpx.Client(base_url="https://jsonplaceholder.typicode.com", timeout=5.0) as client:
    for todo_id in ids:
        print(fetch(client, todo_id)) 


#POST with JSON
r = httpx.post("https://jsonplaceholder.typicode.com/posts",
               json={"title": "hi", "body": "test", "userId": 1})
print(r.status_code, r.json())

#Validate the response with Pydantic
class Todo(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool
try:
    r = httpx.get("https://jsonplaceholder.typicode.com/todos/1")
    Todo.model_validate(r.json())
except ValidationError as e:
    print(e)