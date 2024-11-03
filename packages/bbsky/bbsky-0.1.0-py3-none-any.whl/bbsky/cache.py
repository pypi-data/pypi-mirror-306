import hashlib
import json
import logging
from abc import abstractmethod
from pathlib import Path
from typing import Dict, Hashable, Optional, Protocol, TypeVar, Union

import redis
from click import UsageError

from bbsky.data_cls import TZ, DateTime, Duration

logger = logging.getLogger(__name__)

K_contra = TypeVar("K_contra", contravariant=True)
KH = TypeVar("KH", bound=Hashable)
V = TypeVar("V")


class Cache(Protocol[K_contra, V]):
    """
    A simple cache interface.
    """

    @abstractmethod
    def get(self, key: K_contra) -> Optional[V]:
        """Retrieve a value from the cache."""
        ...

    @abstractmethod
    def set(self, key: K_contra, value: V, ttl: Optional[int] = None) -> None:
        """Store a value in the cache with an optional TTL in seconds."""
        ...

    @abstractmethod
    def delete(self, key: K_contra) -> None:
        """Remove a value from the cache."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear all values from the cache."""
        ...


class InMemoryCache(Cache[KH, V]):
    """
    A simple in-memory cache with optional TTL support.

    Not thread-safe.
    Not suitable for large amounts of data.

    """

    def __init__(self):
        self._cache: Dict[KH, tuple[V, Optional[DateTime]]] = {}
        logger.info("Initialized InMemoryCache")

    def get(self, key: KH) -> Optional[V]:
        if key not in self._cache:
            logger.debug(f"Cache miss for key: {key}")
            return None
        value, expiry = self._cache[key]
        if expiry and DateTime.now(tz=TZ) > expiry:
            logger.info(f"Cache entry expired for key: {key}")
            del self._cache[key]
            return None
        logger.debug(f"Cache hit for key: {key}")
        return value

    def set(self, key: KH, value: V, ttl: Optional[int] = None) -> None:
        expiry = None
        if ttl:
            expiry = DateTime.now(tz=TZ) + Duration(seconds=ttl)
            logger.debug(f"Setting cache entry for key: {key} with TTL: {ttl} seconds")
        else:
            logger.debug(f"Setting cache entry for key: {key} without TTL")
        self._cache[key] = (value, expiry)

    def delete(self, key: KH) -> None:
        if key in self._cache:
            del self._cache[key]
            logger.info(f"Deleted cache entry for key: {key}")
        else:
            logger.debug(f"Attempted to delete non-existent cache entry for key: {key}")

    def clear(self) -> None:
        self._cache.clear()


class DiskCache(Cache[KH, V]):
    """
    A simple disk-based cache that stores values as JSON files

    The cache directory is created if it does not exist.
    Not thread-safe.
    Not suitable for large amounts of data.
    Not a terribly efficient implementation (lots of disk I/O).

    """

    def __init__(self, cache_dir: Union[str, Path]):
        self.cache_dir = Path(cache_dir) if isinstance(cache_dir, str) else cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized DiskCache with directory: {self.cache_dir}")

    def _key_to_path(self, key: KH) -> Path:
        # The cache key is hashed to avoid issues with invalid characters in the key
        hashed_key = hashlib.sha256(str(key).encode()).hexdigest()

        return self.cache_dir / f"{hashed_key}.json"

    def get(self, key: KH) -> Optional[V]:
        path = self._key_to_path(key)
        if not path.exists():
            logger.debug(f"Cache miss for key: {key}")
            return None
        data = json.loads(path.read_text())
        if data["expiry"] and DateTime.fromisoformat(data["expiry"]) < DateTime.now():
            logger.info(f"Cache entry expired for key: {key}")
            path.unlink()
            return None
        return data["value"]

    def set(self, key: KH, value: V, ttl: Optional[int] = None) -> None:
        path = self._key_to_path(key)
        expiry = None
        if ttl:
            expiry = (DateTime.now(tz=TZ) + Duration(seconds=ttl)).isoformat()
        data = {"value": value, "expiry": expiry}
        path.write_text(json.dumps(data))
        logger.debug(f"Set cache entry for key: {key} with expiry: {expiry}")

    def delete(self, key: KH) -> None:
        path = self._key_to_path(key)
        if path.exists():
            path.unlink()
            logger.info(f"Deleted cache entry for key: {key}")

    def clear(self) -> None:
        for path in self.cache_dir.iterdir():
            if path.is_file():
                path.unlink()
                logger.info(f"Cleared cache entry: {path}")


class RedisCache(Cache[KH, V]):
    """
    A Redis-backed cache implementation.

    It requires a running Redis server.
    """

    def __init__(self, client: redis.Redis, allow_clearing: bool = False) -> None:
        self.client = client
        self.allow_clearing = allow_clearing
        logger.info("Initialized RedisCache")

    @staticmethod
    def _serialize_key(key: KH) -> str:
        return json.dumps(key)

    @staticmethod
    def _serialize_value(value: V) -> str:
        return json.dumps(value)

    @staticmethod
    def _deserialize_value(value: Optional[bytes]) -> Optional[V]:
        if value is None:
            return None
        return json.loads(value.decode("utf-8"))

    def get(self, key: KH) -> Optional[V]:
        serialized_key = self._serialize_key(key)
        serialized_value = self.client.get(serialized_key)
        value = self._deserialize_value(serialized_value)  # type: ignore
        if value is None:
            logger.debug(f"Cache miss for key: {key}")
        else:
            logger.debug(f"Cache hit for key: {key}")
        return value

    def set(self, key: KH, value: V, ttl: Optional[int] = None) -> None:
        serialized_key = self._serialize_key(key)
        serialized_value = self._serialize_value(value)
        if ttl:
            self.client.setex(serialized_key, ttl, serialized_value)
        else:
            self.client.set(serialized_key, serialized_value)

    def delete(self, key: KH) -> None:
        serialized_key = self._serialize_key(key)
        self.client.delete(serialized_key)

    def clear(self) -> None:
        if not self.allow_clearing:
            raise UsageError("Clearing the cache is not allowed for this instance of RedisCache")
        self.client.flushdb()  # type: ignore
        logger.info("Cleared Redis cache")
