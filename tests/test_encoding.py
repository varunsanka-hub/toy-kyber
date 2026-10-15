
import pytest

from kyber.encoding import encode_message, decode_message
from kyber.params import PARAMS
from kyber.poly import N 

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


def test_decode_message_recovers_all_zero_bits():
    bits = [0] * PARAMS.n
    encoded = encode_message(bits)

    assert decode_message(encoded) == bits


def test_decode_message_recovers_all_one_bits():
    bits = [1] * PARAMS.n
    encoded = encode_message(bits)

    assert decode_message(encoded) == bits


def test_decode_message_recovers_bits_with_noise():
    bits = [0, 1] * (PARAMS.n // 2)
    encoded = encode_message(bits)

    for noise in (-10, -2, 2, 10):
        noisy = [
            (coefficient + noise) % PARAMS.q
            for coefficient in encoded
        ]

        assert decode_message(noisy) == bits


def test_decode_message_with_noise_near_encoded_values():
    bits = [0, 1] * (PARAMS.n // 2)
    encoded = encode_message(bits)

    # These perturbations are small compared with q/4.
    noise = [10 if bit == 0 else -10 for bit in bits]
    noisy = [
        (coefficient + perturbation) % PARAMS.q
        for coefficient, perturbation in zip(encoded, noise)
    ]

    assert decode_message(noisy) == bits

def test_message_encoding_round_trip():
    message = [
        0, 1, 1, 0,
        1, 0, 0, 1,
        1, 1, 0, 0,
        0, 1, 0, 1,
    ]

    encoded = encode_message(message)
    decoded = decode_message(encoded)

    assert decoded == message 
import pytest
from kyber.encoding import encode_message


def test_encode_message_rejects_wrong_length():
    with pytest.raises(ValueError):
        encode_message([0, 1, 0])


def test_encode_message_rejects_invalid_bits():
    message = [0] * N
    message[3] = 2

    with pytest.raises(ValueError):
        encode_message(message)    
from kyber.encoding import decode_message


def test_decode_message_rejects_wrong_length():
    with pytest.raises(ValueError):
        decode_message([0, 1, 2])
