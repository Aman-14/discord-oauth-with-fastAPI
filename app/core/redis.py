import functools
import pickle

import aioredis


def make_key(function, *args, **kwargs):
    name = function.__name__
    return f"{name}:{args[0]}"


class RedisCache:
    def __init__(self):
        self._pool = None
        self._initialized = False

    async def init(self):
        self._pool = await aioredis.create_redis_pool("redis://localhost")
        self._initialized = True

    @property
    def pool(self) -> aioredis.Redis:
        if not self._initialized:
            raise RuntimeError("Redis pool not initialized")
        return self._pool

    def close(self):
        if self._pool:
            self._pool.close()

    def cache(self, function):
        @functools.wraps(function)
        async def wrapper(*args, **kwargs):
            key = make_key(function, *args, **kwargs)
            value = await self.pool.get(key)
            # check if value exists in cache
            if value is None:
                value = await function(*args, **kwargs)
                # set the key
                await self.pool.setex(key, 5 * 60, pickle.dumps(value))
            else:
                value = pickle.loads(value)
            return value

        return wrapper


Redis = RedisCache()
