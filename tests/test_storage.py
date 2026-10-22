from kyber.keygen import keygen
from kyber.encapsulation import encapsulate
from kyber.decapsulation import decapsulate

from kyber.storage import (
    save_public_key,
    load_public_key,
    save_secret_key,
    load_secret_key,
    save_ciphertext,
    load_ciphertext,
)


def test_public_key_file_round_trip(tmp_path):
    public_key, _ = keygen()
    path = tmp_path / "public_key.json"

    save_public_key(path, public_key)

    assert load_public_key(path) == public_key


def test_secret_key_file_round_trip(tmp_path):
    _, secret_key = keygen()
    path = tmp_path / "secret_key.json"

    save_secret_key(path, secret_key)

    assert load_secret_key(path) == secret_key


def test_ciphertext_file_round_trip(tmp_path):
    public_key, secret_key = keygen()
    message_bits = [1, 0, 1, 1, 0, 0, 1, 0,
                1, 1, 0, 1, 0, 0, 1, 0]
    ciphertext, _ = encapsulate(public_key, message_bits)
    path = tmp_path / "ciphertext.json"

    save_ciphertext(path, ciphertext)

    assert load_ciphertext(path) == ciphertext


def test_saved_files_work_end_to_end(tmp_path):
    public_key, secret_key = keygen()
    message_bits = [1, 0, 1, 1, 0, 0, 1, 0,
                1, 1, 0, 1, 0, 0, 1, 0]
    ciphertext, original_secret = encapsulate(public_key, message_bits)
    public_path = tmp_path / "public_key.json"
    secret_path = tmp_path / "secret_key.json"
    ciphertext_path = tmp_path / "ciphertext.json"

    save_public_key(public_path, public_key)
    save_secret_key(secret_path, secret_key)
    save_ciphertext(ciphertext_path, ciphertext)

    loaded_public_key = load_public_key(public_path)
    loaded_secret_key = load_secret_key(secret_path)
    loaded_ciphertext = load_ciphertext(ciphertext_path)

    recovered_secret = decapsulate(loaded_ciphertext, loaded_secret_key)

    assert loaded_public_key == public_key
    assert recovered_secret == original_secret

import pytest

from kyber.storage import (
    load_public_key,
    save_public_key,
)


def test_loading_missing_file_raises_error(tmp_path):
    path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_public_key(path)


def test_saving_to_missing_directory_raises_error(tmp_path):
    path = tmp_path / "missing_directory" / "public_key.json"
    public_key, _ = keygen()

    with pytest.raises(FileNotFoundError):
        save_public_key(path, public_key)
def test_loading_missing_file_raises_error(tmp_path):
    from kyber.storage import load_public_key

    path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_public_key(path)


def test_saving_to_missing_directory_raises_error(tmp_path):
    from kyber.storage import save_public_key
    from kyber.keygen import keygen

    public_key, _ = keygen()
    path = tmp_path / "missing_directory" / "public_key.json"

    with pytest.raises(FileNotFoundError):
        save_public_key(path, public_key)
