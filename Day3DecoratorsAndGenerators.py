import functools
import time
import random

"""1. *args
Write total(*numbers) that returns the sum of any number of arguments.
total(1, 2, 3) → 6, total() → 0"""

def total(*nums):
    x=0
    for n in nums:
        x += n
    print(x)        

total(7,4)

"""2. **kwargs
Write describe(**info) that prints each key and value on its own line.
describe(name="Asha", role="dev") → name: Asha and role: dev"""

def describe(**info):
    for key, values in info.items():
        print(f"{key}: {values}")

describe(name = "Asha", role="dev")

"""3. Default and keyword-only arguments
Write greet(name, *, greeting="Hello") so greeting must be passed by keyword.
greet("Asha") → Hello, Asha, and greet("Asha", greeting="Hi") → Hi, Asha. 
Then try greet("Asha", "Hi") and read the error."""

def greet(name, *, greeting="Hello"):
    print(f"{name}")

greet("Asha")
greet("Asha", greeting="Hi")
#greet("Asha", "Hi")

""" 4. Closure
Write make_multiplier(n) that returns a function multiplying its input by n.
double = make_multiplier(2), then double(5) → 10.
Java comparison: it's like a lambda that captures a variable."""

def make_multiplier(n):
    def multiply(x):
        return x * n
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double)
print(triple)

print(double(5))
print(triple(5))

"""5. Generator
Write countdown(n) using yield that produces n, n-1, ..., 1. 
Loop over it with for, then call next() on it manually.
Why this matters: generators stream data one item at a time, 
the same way LLM responses stream token by token."""

def countdown(n):
    while n > 0:
        print("Starting")
        yield n
        n -= 1    
for x in countdown(3):
    print(x)

"""6. Decorator: timing
Write a @timer decorator that prints how long a function took. Use time.perf_counter().
Skeleton to start from:"""

def timer(func):
    print("inside timer")
    def inner():
        print("Start")
        start = time.perf_counter()
        result = func(3) #calls original function test
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f}s")
        print("Finish")
        return result
    return inner

@timer
def test(x):
    print("final")

print("Testing")    
test()


"""Decorator: retry (the useful one)
Write @retry(times=3) that calls the function again if it raises an exception, and re-raises after the last attempt.
This one is a decorator that takes an argument, so it has three nested functions. 
Test it with a function that fails randomly, using random.random() < 0.7 to raise an error.
This is the same retry logic you built for Kafka consumers, and it's exactly what you'll wrap around LLM API calls."""

def retry(times):
    print("inside First")
    def timer(func):
        print("timer")
        @functools.wraps(func)
        def innerTwo():
            print("InnerOTwo")
            for attempt in range (1, times+1):
                try:
                    return func()
                except Exception as e:
                    print(f"Attempt failed {attempt}")
                    if attempt == times:
                        raise
            print("Finish")
        return innerTwo
    return timer

@retry(times = 3)
def test():
    if random.random() < 0.7:          # fails 70% of the time
        raise ValueError("random failure")
    return "ok"

print("Testing")  
t = test()
print(test.__name__) 
print(t)
