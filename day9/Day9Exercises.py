#1. Your first coroutine

import asyncio

async def hello():
    print("start")
    await asyncio.sleep(1)
    print("end")
    return "done"

print(hello())              # what does this print?
result = asyncio.run(hello())
print(result)

#2. Sequential vs concurrent
import time

async def fetch(name, seconds):
    print(f"{name} start")
    await asyncio.sleep(seconds)
    #time.sleep(seconds)
    print(f"{name} end")
    return name

async def sequential():
    await fetch("a", 1)
    await fetch("b", 1)
    await fetch("c", 1)

async def concurrent():
    results = await asyncio.gather(fetch("a", 1), fetch("b", 1), fetch("c", 1))
    print(results)

for fn in (sequential, concurrent):
    start = time.perf_counter()
    asyncio.run(fn())
    print(fn.__name__, round(time.perf_counter() - start, 1), "seconds")

#Real concurrent Http
import httpx

async def fetchTodos(client, userId):
    r = await client.get(f"/todos/{userId}")
    r.raise_for_status()
    return r.json()

async def main():
    async with httpx.AsyncClient(base_url = "https://jsonplaceholder.typicode.com", timeout=5.0) as client:
        todos = await asyncio.gather(*(fetchTodos(client, i) for i in range(1, 11)))
    print(len(todos))

asyncio.run(main())

#5. Errors in gather
async def mainGatherWithExp():
    todos = []
    async with httpx.AsyncClient(base_url = "https://jsonplaceholder.typicode.com", timeout=5.0) as client:
        ids = list (range(1, 11)) + [999999999]
        todos = await asyncio.gather(*(fetchTodos(client, i) for i in ids), 
                                     return_exceptions = True) #fixes it
        """try:
            todos = await asyncio.gather(*(fetchTodos(client, i) for i in ids))
        except httpx.HTTPError as e:
            print(f"Error fetching todos: {e}")""" 
    print(len(todos))

asyncio.run(mainGatherWithExp())



# 6. Limiting concurrency

async def mainWithSemaphore():
    semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent requests

    async def fetchWithSemaphore(client, userId):
        async with semaphore:
            return await fetchTodos(client, userId)

    async with httpx.AsyncClient(base_url="https://jsonplaceholder.typicode.com", timeout=5.0) as client:
        todos = await asyncio.gather(*(fetchWithSemaphore(client, i) for i in range(1, 21)))
    print(len(todos))


asyncio.run(mainWithSemaphore())

#7. Retrying failed requests
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
        async def inner(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if not is_transient(e) or attempt == times:
                        raise
                    wait = delay * 2 ** (attempt - 1)
                    logger.warning("attempt %d failed: %s, retrying in %.1fs", attempt, e, wait)
                    await asyncio.sleep(wait)
        return inner
    return decorator                      

#8. Timeouts for the whole task

async def timeoutTask():
    try: 
        result = await asyncio.wait_for(concurrent(), timeout=0.001)
    except asyncio.TimeoutError as e:
        print("Task timed out")

print(asyncio.run(timeoutTask()))

@retry(times=3)
async def fetch_status(code):
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(f"https://httpbin.org/status/{code}")
        r.raise_for_status()
        return r.status_code

async def retryDemo():
    for code in (200, 404, 503):
        try:
            print(code, "->", await fetch_status(code))
        except httpx.HTTPStatusError as e:
            print(code, "-> failed:", e.response.status_code)

asyncio.run(retryDemo())