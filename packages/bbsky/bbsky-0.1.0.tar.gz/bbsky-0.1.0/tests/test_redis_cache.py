import json
from unittest.mock import Mock, patch

import pytest

from bbsky.cache import RedisCache, UsageError


@pytest.fixture
def mock_redis():
    with patch("redis.Redis") as mock:
        yield mock


@pytest.fixture
def cache(mock_redis):
    return RedisCache(client=mock_redis)


def test_get(cache, mock_redis):
    mock_redis.get.return_value = json.dumps("value1").encode()
    assert cache.get("key1") == "value1"
    mock_redis.get.assert_called_once_with(json.dumps("key1"))


def test_get_nonexistent_key(cache, mock_redis):
    mock_redis.get.return_value = None
    assert cache.get("nonexistent") is None


def test_set(cache, mock_redis):
    cache.set("key1", "value1")
    mock_redis.set.assert_called_once_with(json.dumps("key1"), json.dumps("value1"))


def test_set_with_ttl(cache, mock_redis):
    cache.set("key1", "value1", ttl=60)
    mock_redis.setex.assert_called_once_with(json.dumps("key1"), 60, json.dumps("value1"))


def test_delete(cache, mock_redis):
    cache.delete("key1")
    mock_redis.delete.assert_called_once_with(json.dumps("key1"))


def test_clear_allowed(mock_redis):
    cache = RedisCache(client=mock_redis, allow_clearing=True)
    cache.clear()
    mock_redis.flushdb.assert_called_once()


def test_clear_not_allowed(cache):
    with pytest.raises(UsageError):
        cache.clear()


def test_complex_key(cache, mock_redis):
    complex_key = ("tuple", "key", 42)
    cache.set(complex_key, "complex_value")
    mock_redis.set.assert_called_once_with(json.dumps(complex_key), json.dumps("complex_value"))


@pytest.mark.parametrize(
    "key,value",
    [
        ("string_key", "string_value"),
        (42, "int_key_value"),
        (3.14, "float_key_value"),
        (("tuple", "key"), "tuple_value"),
        ({"dict": "key"}, "dict_value"),
    ],
)
def test_various_key_types(cache, mock_redis, key, value):
    cache.set(key, value)
    mock_redis.set.assert_called_once_with(json.dumps(key), json.dumps(value))


def test_serialization_error():
    class UnserializableObject:
        pass

    cache = RedisCache(client=Mock())
    with pytest.raises(TypeError):
        cache.set("key", UnserializableObject())


def test_allow_clearing_default():
    cache = RedisCache(client=Mock())
    assert not cache.allow_clearing


def test_allow_clearing_set():
    cache = RedisCache(client=Mock(), allow_clearing=True)
    assert cache.allow_clearing
