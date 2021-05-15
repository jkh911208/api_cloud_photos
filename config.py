import os

PRODUCTION = os.getenv("PRODUCTION", default=False)
SECRET = os.getenv("SECRET", default=None)
STORE_PATH = os.getenv("STORE_PATH", default=".")
