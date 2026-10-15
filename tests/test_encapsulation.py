
import pytest

from kyber.encapsulation import encapsulate
from kyber.keygen import keygen
from kyber.params import PARAMS


def test_encapsulate():
    public_key, _ = keygen()
    message_bits = [0, 1] * (PARAMS.n // 2)

    ciphertext, shared_secret = encapsulate(
        public_key, message_bits
    )

    u, v = ciphertext

    assert len(u) == 2
    assert all(len(poly) == PARAMS.n for poly in u)
    assert len(v) == PARAMS.n
    assert isinstance(shared_secret, bytes)
    assert len(shared_secret) == 32


def test_encapsulate_rejects_invalid_message_length():
    public_key, _ = keygen()

    with pytest.raises(ValueError):
        encapsulate(public_key, [0, 1])


from kyber.decapsulation import decapsulate


def test_encapsulation_and_decapsulation_agree():
    public_key, secret_key = keygen()
    message_bits = [0, 1] * (PARAMS.n // 2)

    ciphertext, sender_secret = encapsulate(
        public_key, message_bits
    )

    receiver_secret = decapsulate(
        ciphertext, secret_key
    )

    assert receiver_secret == sender_secret


def test_multiple_messages_round_trip():
    public_key, secret_key = keygen()

    messages = [
        [0] * PARAMS.n,
        [1] * PARAMS.n,
        [0, 1] * (PARAMS.n // 2),
        [1, 0] * (PARAMS.n // 2),
    ]

    for message_bits in messages:
        ciphertext, sender_secret = encapsulate(
            public_key, message_bits
        )

        receiver_secret = decapsulate(
            ciphertext, secret_key
        )

        assert receiver_secret == sender_secret


def test_encapsulation_uses_fresh_randomness():
    public_key, _ = keygen()
    message_bits = [0, 1] * (PARAMS.n // 2)

    ciphertext1, _ = encapsulate(public_key, message_bits)
    ciphertext2, _ = encapsulate(public_key, message_bits)

    assert ciphertext1 != ciphertext2


def test_round_trip_for_all_zero_message():
    public_key, secret_key = keygen()
    message_bits = [0] * PARAMS.n

    ciphertext, sender_secret = encapsulate(
        public_key, message_bits
    )
    receiver_secret = decapsulate(
        ciphertext, secret_key
    )

    assert receiver_secret == sender_secret


def test_round_trip_for_all_one_message():
    public_key, secret_key = keygen()
    message_bits = [1] * PARAMS.n

    ciphertext, sender_secret = encapsulate(
        public_key, message_bits
    )
    receiver_secret = decapsulate(
        ciphertext, secret_key
    )

    assert receiver_secret == sender_secret


def test_repeated_encapsulation_decapsulation():
    message_bits = [0, 1] * (PARAMS.n // 2)

    for _ in range(50):
        public_key, secret_key = keygen()

        ciphertext, sender_secret = encapsulate(
            public_key, message_bits
        )

        receiver_secret = decapsulate(
            ciphertext, secret_key
        )

        assert receiver_secret == sender_secret
