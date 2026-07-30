import functools
import hashlib
import json
from collections.abc import Callable
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, time, timedelta
from typing import Any

from pydantic import BaseModel
from redis.asyncio import Redis

from infra.settings.settings import settings


def _init_redis_cache() -> Redis:
    redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
    )
    return redis


def _json_default(obj: Any) -> Any:
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    if isinstance(obj, BaseModel):
        return obj.model_dump(mode="json")
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return obj.total_seconds()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def cache_key(prefix: str, *args, **kwargs) -> str:
    key_data = json.dumps(
        {"args": args[1:], "kwargs": kwargs}, sort_keys=True, default=_json_default
    )
    key_hash = hashlib.sha256(key_data.encode()).hexdigest()[:16]
    return f"{prefix}:{key_hash}"


def cached(prefix: str, ttl: int = 300):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            redis = _init_redis_cache()
            key = cache_key(prefix, *args, **kwargs)
            cached_result = await redis.get(key)

            print(
                f"[CACHE] key={key}, cache_hit={cached_result is not None}", flush=True
            )

            if cached_result is not None:
                return json.loads(cached_result)

            result = await func(*args, **kwargs)

            await redis.setex(key, ttl, json.dumps(result, default=_json_default))

            return result

        return wrapper

    return decorator
