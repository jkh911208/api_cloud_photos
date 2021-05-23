import os

PRODUCTION = bool(os.getenv("PRODUCTION", default=False))
SECRET = os.getenv("SECRET", default="secret")
STORE_PATH = os.getenv("STORE_PATH", default=".")
