import os

PRODUCTION = bool(os.getenv("PRODUCTION", default=False))
