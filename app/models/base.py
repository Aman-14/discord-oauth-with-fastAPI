import pydantic


class BaseModel(pydantic.BaseModel):
    @classmethod
    async def create(cls, **kwargs):
        model = cls(**kwargs)
        await cls.collection.insert_one(model.dict())
        return model

    @classmethod
    async def find_one(cls, query):
        res = await cls.collection.find_one(query)
        return cls(**res) if res else None

    @classmethod
    async def find(cls, query):
        async for item in cls.collection.find(query):
            yield cls(**item)
