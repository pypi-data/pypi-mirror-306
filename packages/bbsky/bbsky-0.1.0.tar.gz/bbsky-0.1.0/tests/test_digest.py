import base64
import hashlib
from io import BytesIO

import pytest

from bbsky.digest import Digest, SupportedAlgorithms, is_supported_algorithm


def test_supported_algorithms():
    """Test the SupportedAlgorithms enum and validation function."""
    assert is_supported_algorithm("sha256")
    assert is_supported_algorithm("sha384")
    assert is_supported_algorithm("sha512")
    assert not is_supported_algorithm("md5")
    assert not is_supported_algorithm("invalid")

    # Test enum values
    assert SupportedAlgorithms.SHA256.value == "sha256"
    assert SupportedAlgorithms.SHA384.value == "sha384"
    assert SupportedAlgorithms.SHA512.value == "sha512"


def test_create_digest_from_bytes():
    data = b"Hello, World!"
    digest = Digest.from_data(data)

    hasher = hashlib.sha256()
    hasher.update(data)
    assert digest.value == hasher.digest()
    assert digest.algorithm == SupportedAlgorithms.SHA256.value


def test_create_digest_from_string():
    text = "Hello, World!"
    digest = Digest.from_data(text)

    bytes_digest = Digest.from_data(text.encode())
    assert digest == bytes_digest


def test_create_digest_with_different_algorithms():
    data = b"Hello, World!"
    for algo in SupportedAlgorithms:
        digest = Digest.from_data(data, algorithm=algo.value)
        hasher = hashlib.new(algo.value)
        hasher.update(data)
        assert digest.value == hasher.digest()
        assert digest.algorithm == algo.value


def test_invalid_algorithm():
    with pytest.raises(ValueError) as exc_info:
        Digest.from_data(b"test", algorithm="invalid")
    assert "Unsupported algorithm" in str(exc_info.value)


def test_create_digest_from_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_content = b"Hello, World!"
    test_file.write_bytes(test_content)

    # Test with Path object
    digest1 = Digest.from_file(test_file)

    # Test with string path
    digest2 = Digest.from_file(str(test_file))

    # Test with file object
    with open(test_file, "rb") as f:
        digest3 = Digest.from_file(f)

    # Test with content directly
    digest4 = Digest.from_data(test_content)

    assert digest1 == digest2 == digest3 == digest4


def test_create_digest_from_large_file(tmp_path):
    test_file = tmp_path / "large.txt"
    test_content = b"x" * (Digest.BLOCK_SIZE + 1000)
    test_file.write_bytes(test_content)

    digest1 = Digest.from_file(test_file)
    digest2 = Digest.from_data(test_content)

    assert digest1 == digest2


def test_create_digest_from_filelike():
    content = b"Hello, World!"
    filelike = BytesIO(content)

    digest1 = Digest.from_file(filelike)
    digest2 = Digest.from_data(content)

    assert digest1 == digest2


def test_hexdigest():
    data = b"Hello, World!"
    digest = Digest.from_data(data)

    hasher = hashlib.sha256()
    hasher.update(data)
    assert digest.hexdigest() == hasher.hexdigest()


def test_base64digest():
    data = b"Hello, World!"
    digest = Digest.from_data(data)

    hasher = hashlib.sha256()
    hasher.update(data)
    expected = base64.b64encode(hasher.digest()).decode("ascii")
    assert digest.base64digest() == expected


def test_sri_property():
    data = b"Hello, World!"
    digest = Digest.from_data(data, algorithm=SupportedAlgorithms.SHA384.value)

    hasher = hashlib.sha384()
    hasher.update(data)
    expected = f"sha384-{base64.b64encode(hasher.digest()).decode('ascii')}"
    assert digest.sri == expected


def test_str_representation():
    data = b"Hello, World!"
    digest = Digest.from_data(data)
    assert str(digest) == digest.hexdigest()


def test_equality():
    data = b"Hello, World!"
    digest1 = Digest.from_data(data)
    digest2 = Digest.from_data(data)
    digest3 = Digest.from_data(b"Different")

    assert digest1 == digest2
    assert digest1 != digest3
    assert digest1 != "not a digest"


def test_different_encodings():
    text = "Hello, 世界"
    digest1 = Digest.from_data(text, encoding="utf-8")
    digest2 = Digest.from_data(text, encoding="utf-16")

    assert digest1 != digest2


@pytest.mark.parametrize("algorithm", [algo.value for algo in SupportedAlgorithms])
def test_each_supported_algorithm(algorithm):
    data = b"Hello, World!"
    digest = Digest.from_data(data, algorithm=algorithm)

    hasher = hashlib.new(algorithm)
    hasher.update(data)
    assert digest.value == hasher.digest()
    assert digest.algorithm == algorithm


def test_direct_instantiation():
    with pytest.raises(ValueError):
        Digest(algorithm="invalid", value=b"test")

    # Valid instantiation should work
    hasher = hashlib.sha256()
    hasher.update(b"test")
    digest = Digest(algorithm=SupportedAlgorithms.SHA256.value, value=hasher.digest())
    assert digest.algorithm == SupportedAlgorithms.SHA256.value
