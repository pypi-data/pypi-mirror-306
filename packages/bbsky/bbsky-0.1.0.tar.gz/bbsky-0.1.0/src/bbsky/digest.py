import base64
import hashlib
from enum import Enum
from pathlib import Path
from typing import BinaryIO, ClassVar, Union

from attrs import define, field


class SupportedAlgorithms(Enum):
    """Supported cryptographic algorithms."""

    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"


def is_supported_algorithm(algorithm: str) -> bool:
    """Check if an algorithm is supported."""
    return algorithm in [v.value for v in SupportedAlgorithms.__members__.values()]


def _validate_algo(value: str):
    if not is_supported_algorithm(value):
        raise ValueError(f"Unsupported algorithm: {value}")


@define(frozen=True)
class Digest:
    """A cryptographic digest type."""

    algorithm: str = field(init=True, validator=lambda _, __, value: _validate_algo(value))
    value: bytes = field(init=True)

    # Standard block size for file reading
    BLOCK_SIZE: ClassVar[int] = 65536

    @property
    def sri(self) -> str:
        """Generate a Subresource Integrity (SRI) string."""
        return f"{self.algorithm}-{self.base64digest()}"

    @classmethod
    def from_file(cls, file: Union[str, Path, BinaryIO], algorithm: str = "sha256") -> "Digest":
        """Create a Digest from a file path or file-like object."""
        hasher = hashlib.new(algorithm)

        if isinstance(file, (str, Path)):
            with open(file, "rb") as f:
                return cls._hash_fileobj(f, hasher)  # type: ignore
        else:
            return cls._hash_fileobj(file, hasher)  # type: ignore

    @classmethod
    def from_data(cls, data: Union[str, bytes], algorithm: str = "sha256", encoding: str = "utf-8") -> "Digest":
        """Create a Digest from bytes or string data."""

        _validate_algo(algorithm)

        hasher = hashlib.new(algorithm)

        if isinstance(data, str):
            data = data.encode(encoding)

        hasher.update(data)
        return cls(algorithm=algorithm, value=hasher.digest())

    @classmethod
    def _hash_fileobj(cls, fileobj: BinaryIO, hasher: "_hashlib.HASH") -> "Digest":  # type: ignore # noqa: F821
        """Helper method to hash a file object."""
        for chunk in iter(lambda: fileobj.read(cls.BLOCK_SIZE), b""):
            hasher.update(chunk)  # type: ignore
        return cls(algorithm=hasher.name, value=hasher.digest())  # type: ignore

    def hexdigest(self) -> str:
        """Return the digest as a hexadecimal string."""
        return self.value.hex()

    def base64digest(self) -> str:
        """Return the digest as a base64 encoded string."""
        return base64.b64encode(self.value).decode("ascii")

    def __str__(self) -> str:
        return self.hexdigest()
