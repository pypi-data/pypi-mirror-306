import pendulum
import pytest

from bbsky.data_cls import (
    URL,
    DateTime,
    structure,
    unstructure,
)


def test_url_conversion():
    url_str = "https://example.com/path?query=value"
    url_obj = structure(url_str, URL)
    assert isinstance(url_obj, URL)
    assert str(url_obj) == url_str

    unstructured_url = unstructure(url_obj)
    assert isinstance(unstructured_url, str)
    assert unstructured_url == url_str


def test_datetime_conversion():
    dt_str = "2023-04-15T12:30:45Z"
    dt_obj = structure(dt_str, DateTime)
    assert isinstance(dt_obj, DateTime)
    assert dt_obj.to_iso8601_string() == dt_str

    unstructured_dt = unstructure(dt_obj)
    assert isinstance(unstructured_dt, str)
    assert unstructured_dt == dt_str


@pytest.mark.parametrize(
    "url_str, expected",
    [
        ("", ""),  # Empty URL
        ("http://", "http://"),  # URL with only scheme
        ("https://example.com", "https://example.com"),  # URL with only scheme and host
        (
            "https://user:pass@example.com:8080/path?query=value#fragment",
            "https://user:pass@example.com:8080/path?query=value#fragment",
        ),  # More complex URL with all components
        ("mailto:user@example.com", "mailto:user@example.com"),  # mailto URL
        ("file:///path/to/file.txt", "file:///path/to/file.txt"),  # file URL
    ],
)
def test_url_structuring_and_unstructuring_edge_cases(url_str: str, expected: str) -> None:
    url_obj = structure(url_str, URL)
    assert str(url_obj) == expected
    assert unstructure(url_obj) == expected


@pytest.mark.parametrize(
    "dt_str, expected",
    [
        ("2023-04-15", "2023-04-15T00:00:00Z"),  # Date without time component
        ("2023-04-15 12:30:45", "2023-04-15T12:30:45Z"),  # Datetime without timezone (assumes UTC)
        ("2023-W16-6", "2023-04-22T00:00:00Z"),  # ISO week date
        ("20230415T123045Z", "2023-04-15T12:30:45Z"),  # Basic ISO 8601 format
    ],
)
def test_datetime_edge_cases(dt_str: str, expected: str) -> None:
    dt_obj = structure(dt_str, DateTime)
    assert dt_obj.to_iso8601_string() == expected
    assert unstructure(dt_obj) == expected


def test_current_time() -> None:
    now = pendulum.now("UTC")
    now_str = now.to_iso8601_string()
    parsed_now = structure(now_str, DateTime)
    assert parsed_now == now


def test_invalid_datetime_inputs() -> None:
    with pytest.raises(ValueError):
        structure("not a valid datetime", DateTime)
