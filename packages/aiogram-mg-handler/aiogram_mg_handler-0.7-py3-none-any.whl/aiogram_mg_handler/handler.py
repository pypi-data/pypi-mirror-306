"""
Fork of aiogram-media-group
https://pypi.org/project/aiogram-media-group
"""

import asyncio

from functools import wraps
from typing import Callable, Optional
from aiogram import types, Dispatcher

from . import AIOGRAM_VERSION
from .storages.base import BaseStorage
from .storages.memory import MemoryStorage

if AIOGRAM_VERSION == 3:
    STORAGE = {}

elif AIOGRAM_VERSION == 2:
    from aiogram.dispatcher.storage import BaseStorage as AiogramBaseStorage
    from aiogram.contrib.fsm_storage.memory import MemoryStorage as AiogramMemoryStorage

    MONGO_INSTALLED = False
    REDIS_INSTALLED = False

    try:
        from motor import motor_asyncio
        from aiogram.contrib.fsm_storage.mongo import MongoStorage as AiogramMongoStorage
        from .storages.mongo import MongoStorage
        MONGO_INSTALLED = True
    except ModuleNotFoundError:
        pass

    try:
        import aioredis
        from aiogram.contrib.fsm_storage.redis import (
            RedisStorage as AiogramRedisStorage,
            RedisStorage2 as AiogramRedis2Storage,
        )
        from .storages.redis import RedisStorage
        REDIS_INSTALLED = True
    except ModuleNotFoundError:
        pass


    async def _wrap_storage(storage: AiogramBaseStorage, prefix: str, ttl: int):
        storage_type = type(storage)
        
        if storage_type is AiogramMemoryStorage:
            return MemoryStorage(data=storage.data, prefix=prefix)
        
        if MONGO_INSTALLED and storage_type is AiogramMongoStorage:
            mongo: motor_asyncio.AsyncIOMotorDatabase = await storage.get_db()
            return MongoStorage(db=mongo, prefix=prefix, ttl=ttl)
        
        if REDIS_INSTALLED:
            if storage_type is AiogramRedisStorage:
                connection: aioredis.RedisConnection = await storage.redis()
                return RedisStorage(connection=connection, prefix=prefix, ttl=ttl)
            elif storage_type is AiogramRedis2Storage:
                redis: aioredis.Redis = await storage.redis()
                return RedisStorage(connection=redis.connection, prefix=prefix, ttl=ttl)
        
        raise ValueError(f"{storage_type} is unsupported storage")


async def _on_media_group_received(media_group_id: str, storage: BaseStorage, callback, *args, **kwargs):
    messages = await storage.get_media_group_messages(media_group_id)
    await storage.delete_media_group(media_group_id)
    return await callback(messages, *args, **kwargs)


def media_group_handler(
    func: Optional[Callable] = None,
    only_album: bool = True,
    receive_timeout: float = 1.0,
    storage_prefix: str = "media_group_handler",
    storage_driver: Optional[BaseStorage] = None,
    loop=None
):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message: types.Message, *args, **kwargs):
            if only_album and message.media_group_id is None:
                return await handler(message, *args, **kwargs)
            elif message.media_group_id is None:
                return await handler([message], *args, **kwargs)

            event_loop = asyncio.get_running_loop() if loop is None else loop
            ttl = max(int(receive_timeout * 2), 1)
            
            storage = storage_driver or (await _wrap_storage(
                Dispatcher.get_current().storage, storage_prefix, ttl
            ) if AIOGRAM_VERSION == 2 else MemoryStorage(STORAGE, prefix=''))

            if await storage.set_media_group_as_handled(message.media_group_id):
                event_loop.call_later(
                    receive_timeout,
                    lambda: asyncio.create_task(
                        _on_media_group_received(message.media_group_id, storage, handler, *args, **kwargs)
                    ),
                )

            await storage.append_message_to_media_group(message.media_group_id, message)

        return wrapper

    return decorator(func) if callable(func) else decorator
