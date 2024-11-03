from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from bbsky.cache import InMemoryCache
from bbsky.data_cls import TZ


@pytest.fixture
def cache() -> InMemoryCache:
    return InMemoryCache()


def test_set_and_get(cache: InMemoryCache[str, str]) -> None:
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"


def test_get_nonexistent_key(cache) -> None:
    assert cache.get("nonexistent") is None


def test_set_overwrites_existing_value(cache) -> None:
    cache.set("key1", "value1")
    cache.set("key1", "value2")
    assert cache.get("key1") == "value2"


def test_delete_existing_key(cache) -> None:
    cache.set("key1", "value1")
    cache.delete("key1")
    assert cache.get("key1") is None


def test_delete_nonexistent_key(cache) -> None:
    cache.delete("nonexistent")  # Should not raise an exception


def test_clear(cache):
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear()
    assert cache.get("key1") is None
    assert cache.get("key2") is None


@pytest.mark.parametrize(
    "key,value", [(42, "int_key"), (3.14, "float_key"), ((1337, 824), "tuple_key"), ("string", "string_key")]
)
def test_hashable_keys(cache, key, value):
    cache.set(key, value)
    assert cache.get(key) == value


def test_unhashable_key_raises_error(
    cache: InMemoryCache,
) -> None:
    with pytest.raises(TypeError):
        cache.set([1, 2, 3], "list_key")


@patch("bbsky.cache.DateTime")
def test_ttl_not_expired(mock_datetime: patch, cache: InMemoryCache[str, str]) -> None:
    mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=TZ)
    mock_datetime.now.return_value = mock_now

    cache.set("key1", "value1", ttl=3600)  # 1 hour TTL

    # Fast-forward time by 30 minutes
    mock_datetime.now.return_value = mock_now + timedelta(minutes=30)

    assert cache.get("key1") == "value1"


@patch("bbsky.cache.DateTime")
def test_ttl_expired(mock_datetime: patch, cache: InMemoryCache[str, str]) -> None:
    mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=TZ)
    mock_datetime.now.return_value = mock_now

    cache.set("key1", "value1", ttl=3600)  # 1 hour TTL

    # Fast-forward time by 2 hours
    mock_datetime.now.return_value = mock_now + timedelta(hours=2)

    assert cache.get("key1") is None


@patch("bbsky.cache.DateTime")
def test_mixed_ttl(mock_datetime: patch, cache: InMemoryCache[str, str]) -> None:
    mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=TZ)
    mock_datetime.now.return_value = mock_now

    cache.set("key1", "value1", ttl=3600)  # 1 hour TTL
    cache.set("key2", "value2")  # No TTL

    # Fast-forward time by 2 hours
    mock_datetime.now.return_value = mock_now + timedelta(hours=2)

    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"


def test_large_number_of_items(cache: InMemoryCache[str, str]) -> None:
    for i in range(10000):
        cache.set(f"key{i}", f"value{i}")

    assert len(cache._cache) == 10000
    assert cache.get("key9999") == "value9999"
