import os

PRODUCTION = os.getenv("PRODUCTION").lower() in {'true', '1'}
SECRET = os.getenv("SECRET", default="secret")
STORE_PATH = os.getenv("STORE_PATH", default=".")
APP_SECRET = os.getenv("APP_SECRET")
