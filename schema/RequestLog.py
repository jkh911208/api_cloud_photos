from db import db, metadata, sqlalchemy
from sqlalchemy.sql import func

users = sqlalchemy.Table(
    "request_log",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(
        36), primary_key=True, unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime,
                      nullable=False, default=func.now()),
    sqlalchemy.Column("headers", sqlalchemy.JSON, nullable=False),
    sqlalchemy.Column("requested_time", sqlalchemy.BigInteger, nullable=False),
    sqlalchemy.Column("arrival_time", sqlalchemy.BigInteger, nullable=False),
    sqlalchemy.Column("time_difference", sqlalchemy.BigInteger, nullable=False)
)


class RequestLog:
    @classmethod
    async def insert(cls, **data):
        query = users.insert().values(**data)
        return await db.execute(query)
