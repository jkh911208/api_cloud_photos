import uuid

from db import db, metadata, sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", UUID(as_uuid=True), primary_key=True, index=True, unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime, nullable=False, default=func.now()),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=False, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False)
)

class Users:
    @classmethod
    async def get(cls, id):
        query = users.select().where(users.c.id == id)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def create(cls, **user):
        query = users.insert().values(**user)
        user_id = await db.execute(query)
        return user_id
