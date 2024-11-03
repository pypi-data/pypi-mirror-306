import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Hashable
from unittest.mock import patch

import pytest

from bbsky.cache import DiskCache
from bbsky.data_cls import TZ


@pytest.fixture
def cache_dir(tmpdir: Path) -> Path:
    return Path(tmpdir)


@pytest.fixture
def cache(cache_dir: Path) -> DiskCache:
    return DiskCache(cache_dir)


def test_init_creates_directory(tmpdir: Path) -> None:
    cache_dir = Path(tmpdir) / "new_cache_dir"
    DiskCache(cache_dir)
    assert cache_dir.exists() and cache_dir.is_dir()


def test_set_and_get(cache: DiskCache[str, str]) -> None:
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"


def test_get_nonexistent_key(cache: DiskCache[str, str]) -> None:
    assert cache.get("nonexistent") is None


def test_set_overwrites_existing_value(cache: DiskCache[str, str]) -> None:
    cache.set("key1", "value1")
    cache.set("key1", "value2")
    assert cache.get("key1") == "value2"


def test_delete_existing_key(cache: DiskCache[str, str]) -> None:
    cache.set("key1", "value1")
    cache.delete("key1")
    assert cache.get("key1") is None


def test_delete_nonexistent_key(cache: DiskCache[str, str]) -> None:
    cache.delete("nonexistent")  # Should not raise an exception


def test_clear(cache: DiskCache[str, str]) -> None:
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear()
    assert cache.get("key1") is None
    assert cache.get("key2") is None


@pytest.mark.parametrize(
    "key,value",
    [
        ("string_key", "string_value"),
        ("int_key", 42),
        ("float_key", 3.14),
        ("bool_key", True),
        ("list_key", [1, 2, 3]),
        ("dict_key", {"a": 1, "b": 2}),
    ],
)
def test_various_value_types(
    cache: DiskCache[str, Hashable],
    key: str,
    value: Hashable,
) -> None:
    cache.set(key, value)
    assert cache.get(key) == value


def test_non_string_key(cache: DiskCache[int, str]) -> None:
    cache.set(42, "int_key_value")
    assert cache.get(42) == "int_key_value"


@patch("bbsky.cache.DateTime")
def test_ttl_not_expired(mock_datetime: patch, cache: DiskCache[str, str]) -> None:
    mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=TZ)
    mock_datetime.now.return_value = mock_now
    mock_datetime.fromisoformat.return_value = mock_now + timedelta(hours=1)

    cache.set("key1", "value1", ttl=3600)  # 1 hour TTL

    # Advance time by 30 minutes
    mock_datetime.now.return_value = mock_now + timedelta(minutes=30)

    assert cache.get("key1") == "value1"


@patch("bbsky.cache.DateTime")
def test_ttl_expired(mock_datetime: patch, cache: DiskCache[str, str]) -> None:
    mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=TZ)
    mock_datetime.now.return_value = mock_now
    mock_datetime.fromisoformat.return_value = mock_now + timedelta(hours=1)

    cache.set("key1", "value1", ttl=3600)  # 1 hour TTL

    # Advance time by 2 hours
    mock_datetime.now.return_value = mock_now + timedelta(hours=2)

    assert cache.get("key1") is None


def test_file_permission_error(cache: DiskCache[str, str], monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_write_text(self, content):
        raise PermissionError("Permission denied")

    monkeypatch.setattr(Path, "write_text", mock_write_text)

    with pytest.raises(PermissionError):
        cache.set("key1", "value1")


def test_json_serialization_error(cache) -> None:
    with pytest.raises(TypeError):
        cache.set("key1", set([1, 2, 3]))  # Sets are not JSON serializable


def test_corrupted_json_file(cache, cache_dir) -> None:
    key = "corrupted_key"
    file_path = cache._key_to_path(key)
    file_path.write_text("This is not valid JSON")

    with pytest.raises(json.JSONDecodeError):
        cache.get(key)


def test_large_number_of_items(cache) -> None:
    for i in range(1000):
        cache.set(f"key{i}", f"value{i}")

    assert cache.get("key999") == "value999"


def test_key_with_special_characters(cache) -> None:
    key = "special!@#$%^&*()_+{}[]|\\:;\"'<>,.?/~`"
    value = "special_value"
    cache.set(key, value)
    assert cache.get(key) == value


@pytest.mark.parametrize("cache_dir", [Path("/tmp/test_cache"), "/tmp/test_cache"])
def test_cache_dir_types(cache_dir, tmpdir) -> None:
    cache = DiskCache(cache_dir)
    assert isinstance(cache.cache_dir, Path)


def test_complex_hashable_key(cache) -> None:
    complex_key = ("tuple", "key", 42)
    cache.set(complex_key, "complex_value")
    assert cache.get(complex_key) == "complex_value"


def test_object_as_key(cache) -> None:
    class TestObject:
        def __init__(self, value):
            self.value = value

        def __hash__(self):
            return hash(self.value)

        def __eq__(self, other):
            return isinstance(other, TestObject) and self.value == other.value

    obj_key = TestObject("test")
    cache.set(obj_key, "object_value")
    assert cache.get(obj_key) == "object_value"


def test_long_key(cache) -> None:
    long_key = "a" * 1000  # A very long string key
    cache.set(long_key, "long_key_value")
    assert cache.get(long_key) == "long_key_value"


def test_key_consistency(cache) -> None:
    key = ("complex", "tuple", "key")
    cache.set(key, "tuple_value")
    assert cache.get(key) == "tuple_value"
    cache.delete(key)
    assert cache.get(key) is None
