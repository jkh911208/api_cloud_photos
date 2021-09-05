from db import db, metadata, sqlalchemy
from sqlalchemy.sql import func

feedback = sqlalchemy.Table(
    "feedback",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(
        36), primary_key=True, unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime,
                      nullable=False, default=func.now()),
    sqlalchemy.Column("feedback", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("owner", sqlalchemy.String(36), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.SmallInteger, nullable=False),
    sqlalchemy.ForeignKeyConstraint(["owner"], ["users.id"])
)


class Feedback:
    @classmethod
    async def insert(cls, **data):
        query = feedback.insert().values(**data)
        return await db.execute(query)
