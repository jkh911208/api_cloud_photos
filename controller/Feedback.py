from uuid import uuid4

from schema.Feedback import Feedback as feedback_table


class Feedback():
    def __init__(self):
        pass

    @staticmethod
    async def new_feedback(data):
        data["id"] = str(uuid4())
        data["status"] = 1
        await feedback_table.insert(**data)
