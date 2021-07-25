import pydantic
from bson import ObjectId


class BaseModel(pydantic.BaseModel):
    _id: ObjectId

    @property
    def created_at(self):
        return self._id.generation_time

    @classmethod
    async def create(cls, **kwargs):
        model = cls(**kwargs)
        await cls.collection.insert_one(model.dict())
        return model

    @classmethod
    async def find_one(cls, query):
        return await cls.collection.find_one(query)

    @classmethod
    async def find(cls, query):
        async for item in cls.collection.find(query):
            yield item
