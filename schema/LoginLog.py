from db import db, metadata, sqlalchemy
from sqlalchemy.sql import func

users = sqlalchemy.Table(
    "login_log",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(
        36), primary_key=True, unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime,
                      nullable=False, default=func.now()),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("status", sqlalchemy.SmallInteger, nullable=False)
)


class LoginLog:
    @classmethod
    async def insert(cls, **data):
        query = users.insert().values(**data)
        return await db.execute(query)
