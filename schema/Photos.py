from db import db, metadata, sqlalchemy
from sqlalchemy.sql import func

photos = sqlalchemy.Table(
    "photos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(
        36), primary_key=True, index=True, unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime,
                      nullable=False, default=func.now()),
    sqlalchemy.Column("original_filename", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("original_datetime", sqlalchemy.DateTime,
                      nullable=False, default=func.now(), index=True),
    sqlalchemy.Column("original_make", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("original_model", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("original_width", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("original_height", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("new_filename", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("thumbnail", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("resize", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("md5", sqlalchemy.String, nullable=False, unique=False),
    sqlalchemy.Column("latitude", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("longitude", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("owner", sqlalchemy.String(36),
                      index=True, nullable=False),
    sqlalchemy.Column("status", sqlalchemy.SmallInteger, nullable=False),
    sqlalchemy.ForeignKeyConstraint(["owner"], ["users.id"])
)


class Photos:
    @classmethod
    async def get_by_id(cls, id):
        query = photos.select().where(photos.c.id == id)
        photo = await db.fetch_one(query)
        return dict(photo)

    @classmethod
    async def get_by_owner(cls, owner: str, offset: int = 0, limit: int = 100):
        query = photos.select().with_only_columns([photos.c.id, photos.c.original_datetime, photos.c.thumbnail, photos.c.resize]).where(
            photos.c.owner == owner).limit(limit).offset(offset).order_by(photos.c.original_datetime.desc())
        result = await db.fetch_all(query)
        return {"result": result}

    @classmethod
    async def check_redundant_file(cls, owner: str, md5: str):
        query = photos.select().where(photos.c.owner == owner).where(
            photos.c.md5 == md5).limit(1)
        result = await db.fetch_one(query)
        if result:
            return dict(result)
        return None

    @classmethod
    async def insert(cls, **data):
        query = photos.insert().values(**data)
        return await db.execute(query)
