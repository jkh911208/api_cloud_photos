import os

import sqlalchemy
from databases import Database

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_ADDRESS = os.getenv("POSTGRES_ADDRESS")


DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}:5432"

db = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
