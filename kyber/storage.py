
"""File storage helpers."""

from pathlib import Path

from .serialization import (
    serialize_public_key,
    deserialize_public_key,
    serialize_secret_key,
    deserialize_secret_key,
    serialize_ciphertext,
    deserialize_ciphertext,
)


def _write_text(path, content):
    Path(path).write_text(content, encoding="utf-8")


def _read_text(path):
    return Path(path).read_text(encoding="utf-8")


def save_public_key(path, public_key):
    _write_text(path, serialize_public_key(public_key))


def load_public_key(path):
    return deserialize_public_key(_read_text(path))


def save_secret_key(path, secret_key):
    _write_text(path, serialize_secret_key(secret_key))


def load_secret_key(path):
    return deserialize_secret_key(_read_text(path))


def save_ciphertext(path, ciphertext):
    _write_text(path, serialize_ciphertext(ciphertext))


def load_ciphertext(path):
    return deserialize_ciphertext(_read_text(path))
