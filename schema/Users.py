from db import db, metadata, sqlalchemy
from sqlalchemy.sql import func

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(
        36), primary_key=True, index=True, unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime,
                      nullable=False, default=func.now()),
    sqlalchemy.Column("username", sqlalchemy.String,
                      nullable=False, unique=True, index=True),
    sqlalchemy.Column("password", sqlalchemy.String(128), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.SmallInteger, nullable=False)
)


class Users:
    @classmethod
    async def get_by_id(cls, id):
        query = users.select().where(users.c.id == id)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def get_by_username(cls, username):
        query = users.select().where(users.c.username == username)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def insert(cls, **data):
        query = users.insert().values(**data)
        return await db.execute(query)
