from db import db, metadata, sqlalchemy
from sqlalchemy.sql import func

photos = sqlalchemy.Table(
    "photos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(
        36), primary_key=True, index=True, unique=True),
    sqlalchemy.Column("created", sqlalchemy.BigInteger,
                      nullable=False),
    sqlalchemy.Column("original_filename", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("original_datetime", sqlalchemy.BigInteger,
                      nullable=False, index=True),
    sqlalchemy.Column("original_make", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("original_model", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("original_width", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("original_height", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("original_filesize",
                      sqlalchemy.BigInteger, nullable=False),
    sqlalchemy.Column("new_filename", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("thumbnail", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("resize", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("md5", sqlalchemy.String, nullable=False, unique=False),
    sqlalchemy.Column("latitude", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("longitude", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("owner", sqlalchemy.String(36),
                      index=True, nullable=False),
    sqlalchemy.Column("status", sqlalchemy.SmallInteger, nullable=False),
    sqlalchemy.Column("duration", sqlalchemy.Float,
                      nullable=False, server_default="0.0"),
    sqlalchemy.UniqueConstraint("owner", "md5"),
    sqlalchemy.ForeignKeyConstraint(["owner"], ["users.id"])
)


class Photos:
    @classmethod
    async def get_by_id(cls, id):
        query = photos.select().where(photos.c.id == id)
        photo = await db.fetch_one(query)
        return dict(photo)

    @classmethod
    async def get_by_owner(cls, owner: str, created: int = 0, limit: int = 20):
        query = photos.select().with_only_columns([photos.c.id, photos.c.created, photos.c.thumbnail, photos.c.resize, photos.c.original_width, photos.c.original_height, photos.c.original_datetime, photos.c.md5, photos.c.duration]).where(
            photos.c.owner == owner).where(photos.c.created > created).limit(limit).order_by(photos.c.created)
        result = await db.fetch_all(query)
        return {"result": result}

    @classmethod
    async def check_redundant_file(cls, owner: str, md5: str):
        query = photos.select().where(photos.c.owner == owner).where(
            photos.c.md5 == md5)
        result = await db.fetch_one(query)
        if result:
            return dict(result)
        return None

    @classmethod
    async def insert(cls, **data):
        query = photos.insert().values(**data)
        return await db.execute(query)

    @classmethod
    async def delete(cls, id: str):
        query = photos.delete().where(photos.c.id == id)
        return await db.execute(query)
