from db import db, metadata, sqlalchemy
from sqlalchemy.sql import func

photos = sqlalchemy.Table(
    "photos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(
        36), primary_key=True, index=True, unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime,
                      nullable=False, default=func.now()),
    sqlalchemy.Column("status", sqlalchemy.SmallInteger, nullable=False),
    sqlalchemy.Column("owner", sqlalchemy.String(36), index=True, nullable=False),
    sqlalchemy.ForeignKeyConstraint(["owner"], ["users.id"])
)


class Photos:
    @classmethod
    async def get_by_id(cls, id):
        query = photos.select().where(photos.c.id == id)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def get_by_owner(cls, owner: str, offset: int = 0, limit: int = 100):
        query = photos.select().where(photos.c.owner == owner).limit(limit).offset(offset)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def insert(cls, **data):
        query = photos.insert().values(**data)
        return await db.execute(query)