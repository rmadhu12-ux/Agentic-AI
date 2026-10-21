import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
print(bool(api_key))     # prints True or False, never the key itself