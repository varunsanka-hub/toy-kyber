
import json
import pytest

from kyber import keygen, encapsulate, decapsulate
from kyber.serialization import (
    serialize_public_key,
    deserialize_public_key,
    serialize_secret_key,
    deserialize_secret_key,
    serialize_ciphertext,
    deserialize_ciphertext,
)


def test_public_key_round_trip():
    public_key, _ = keygen()

    restored = deserialize_public_key(
        serialize_public_key(public_key)
    )

    assert restored == public_key


def test_secret_key_round_trip():
    _, secret_key = keygen()

    restored = deserialize_secret_key(
        serialize_secret_key(secret_key)
    )

    assert restored == secret_key


def test_ciphertext_round_trip():
    public_key, _ = keygen()
    message = [0, 1] * 8
    ciphertext, _ = encapsulate(public_key, message)

    restored = deserialize_ciphertext(
        serialize_ciphertext(ciphertext)
    )

    assert restored == ciphertext


def test_serialized_objects_work_end_to_end():
    public_key, secret_key = keygen()
    message = [1, 0] * 8

    ciphertext, sender_secret = encapsulate(public_key, message)

    restored_public = deserialize_public_key(
        serialize_public_key(public_key)
    )
    restored_secret = deserialize_secret_key(
        serialize_secret_key(secret_key)
    )
    restored_ciphertext = deserialize_ciphertext(
        serialize_ciphertext(ciphertext)
    )

    assert restored_public == public_key
    assert decapsulate(restored_ciphertext, restored_secret) == sender_secret


def test_rejects_invalid_json():
    with pytest.raises(ValueError, match="Invalid JSON"):
        deserialize_secret_key("{not valid json")


def test_rejects_wrong_format():
    wrong_format = json.dumps({
        "format": "toy-kyber-public-key",
        "version": 1,
        "data": {"s": [[0] * 16, [0] * 16]},
    })

    with pytest.raises(ValueError, match="format"):
        deserialize_secret_key(wrong_format)


def test_rejects_wrong_secret_key_shape():
    malformed = json.dumps({
        "format": "toy-kyber-secret-key",
        "version": 1,
        "data": {"s": [[0] * 16]},
    })

    with pytest.raises(ValueError, match="exactly K"):
        deserialize_secret_key(malformed)


def test_rejects_boolean_coefficients():
    malformed = json.dumps({
        "format": "toy-kyber-secret-key",
        "version": 1,
        "data": {"s": [[True] + [0] * 15, [0] * 16]},
    })

    with pytest.raises(ValueError, match="integers"):
        deserialize_secret_key(malformed)

def test_rejects_non_list_polynomial():
    from kyber.serialization import _validate_poly

    with pytest.raises(ValueError, match="list of N coefficients"):
        _validate_poly((0,) * 16, "poly")


def test_rejects_out_of_range_coefficient():
    from kyber.serialization import _validate_poly

    with pytest.raises(ValueError, match="out-of-range"):
        _validate_poly([3329] + [0] * 15, "poly")


def test_rejects_wrong_matrix_shape():
    from kyber.serialization import _validate_matrix

    with pytest.raises(ValueError, match="K x K"):
        _validate_matrix([[0] * 16], "A")


def test_rejects_wrong_matrix_row_shape():
    from kyber.serialization import _validate_matrix

    with pytest.raises(ValueError, match="K x K"):
        _validate_matrix(
            [[[0] * 16], [[0] * 16]],
            "A",
        )


def test_rejects_non_string_serialized_input():
    with pytest.raises(ValueError, match="JSON string"):
        deserialize_secret_key(None)


def test_rejects_json_non_object():
    with pytest.raises(ValueError, match="JSON object"):
        deserialize_secret_key("[]")


def test_rejects_unexpected_json_fields():
    serialized = json.dumps({
        "format": "toy-kyber-secret-key",
        "version": 1,
        "data": {"s": [[0] * 16, [0] * 16]},
        "extra": True,
    })

    with pytest.raises(ValueError, match="Unexpected serialized object fields"):
        deserialize_secret_key(serialized)


def test_rejects_unsupported_serialization_version():
    serialized = json.dumps({
        "format": "toy-kyber-secret-key",
        "version": 2,
        "data": {"s": [[0] * 16, [0] * 16]},
    })

    with pytest.raises(ValueError, match="Unsupported serialization version"):
        deserialize_secret_key(serialized)


def test_rejects_invalid_public_key_data_fields():
    serialized = json.dumps({
        "format": "toy-kyber-public-key",
        "version": 1,
        "data": {"wrong": []},
    })

    with pytest.raises(ValueError, match="Public-key data"):
        deserialize_public_key(serialized)


def test_rejects_invalid_secret_key_data_fields():
    serialized = json.dumps({
        "format": "toy-kyber-secret-key",
        "version": 1,
        "data": [],
    })

    with pytest.raises(ValueError, match="Secret-key data"):
        deserialize_secret_key(serialized)


def test_rejects_invalid_ciphertext_pair():
    from kyber.serialization import serialize_ciphertext

    with pytest.raises(ValueError, match="Ciphertext must contain"):
        serialize_ciphertext(([0] * 16,))


def test_rejects_invalid_ciphertext_data_fields():
    serialized = json.dumps({
        "format": "toy-kyber-ciphertext",
        "version": 1,
        "data": {"wrong": []},
    })

    with pytest.raises(ValueError, match="Ciphertext data"):
        deserialize_ciphertext(serialized)


def test_rejects_invalid_public_key_pair():
    with pytest.raises(ValueError, match="Public key must contain"):
        serialize_public_key(([0] * 16,))

def test_rejects_invalid_public_key_coefficient():
    from kyber.serialization import serialize_public_key

    A = [[[0] * 16 for _ in range(2)] for _ in range(2)]
    t = [[0] * 16 for _ in range(2)]
    A[0][0][0] = 3329  # q itself is outside [0, q-1].

    with pytest.raises(ValueError, match="out-of-range"):
        serialize_public_key((A, t))


def test_rejects_invalid_ciphertext_coefficient():
    from kyber.serialization import serialize_ciphertext

    u = [[0] * 16 for _ in range(2)]
    v = [0] * 16
    v[0] = 3329

    with pytest.raises(ValueError, match="out-of-range"):
        serialize_ciphertext((u, v))


def test_rejects_out_of_range_secret_key_coefficient():
    from kyber.serialization import serialize_secret_key

    secret_key = [[0] * 16 for _ in range(2)]
    secret_key[0][0] = 3329

    with pytest.raises(ValueError, match="out-of-range"):
        serialize_secret_key(secret_key)


def test_rejects_boolean_serialization_version():
    from kyber.serialization import deserialize_secret_key
    import json

    serialized = json.dumps({
        "format": "toy-kyber-secret-key",
        "version": True,
        "data": {"s": [[0] * 16, [0] * 16]},
    })

    with pytest.raises(ValueError, match="Unsupported serialization version"):
        deserialize_secret_key(serialized)
