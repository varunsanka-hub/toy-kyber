
import pytest

from kyber.encoding import encode_message
from kyber.params import PARAMS


def test_encode_message():
    bits = [0, 1] * (PARAMS.n // 2)

    encoded = encode_message(bits)

    assert len(encoded) == PARAMS.n
    assert encoded[0] == 0
    assert encoded[1] == PARAMS.q // 2


def test_encode_message_rejects_wrong_length():
    with pytest.raises(ValueError):
        encode_message([0, 1])


def test_encode_message_rejects_invalid_bit():
    bits = [0] * PARAMS.n
    bits[0] = 2

    with pytest.raises(ValueError):
        encode_message(bits)


from kyber.encoding import decode_message


def test_encode_decode_round_trip():
    bits = [0, 1] * (PARAMS.n // 2)

    encoded = encode_message(bits)
    decoded = decode_message(encoded)

    assert decoded == bits


def test_decode_message_handles_small_noise():
    bits = [0, 1] * (PARAMS.n // 2)
    encoded = encode_message(bits)

    noisy = [
        (coefficient + (2 if bit else -2)) % PARAMS.q
        for coefficient, bit in zip(encoded, bits)
    ]

    assert decode_message(noisy) == bits
