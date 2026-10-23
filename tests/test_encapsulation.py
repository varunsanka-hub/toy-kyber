
import pytest
import random
from kyber.encapsulation import encapsulate
from kyber.keygen import keygen
from kyber.params import PARAMS
from kyber.poly import N 

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


import random


def test_random_messages_round_trip():
    for _ in range(100):
        public_key, secret_key = keygen()

        message_bits = [
            random.randint(0, 1) for _ in range(PARAMS.n)
        ]

        ciphertext, sender_secret = encapsulate(
            public_key, message_bits
        )
        receiver_secret = decapsulate(ciphertext, secret_key)

        assert receiver_secret == sender_secret


def test_decapsulation_reliability_over_100_trials():
    successes = 0
    trials = 100

    for _ in range(trials):
        public_key, secret_key = keygen()
        message_bits = [
            random.randint(0, 1) for _ in range(PARAMS.n)
        ]

        ciphertext, sender_secret = encapsulate(
            public_key, message_bits
        )
        receiver_secret = decapsulate(ciphertext, secret_key)

        if receiver_secret == sender_secret:
            successes += 1

    print(f"\nDecapsulation reliability: {successes}/{trials}")
    assert successes == trials


def test_decapsulation_recovers_message_repeatedly():
    for _ in range(100):
        public_key, secret_key = keygen()
        message_bits = [
            random.randint(0, 1) for _ in range(PARAMS.n)
        ]

        ciphertext, sender_secret = encapsulate(
            public_key, message_bits
        )
        receiver_secret = decapsulate(ciphertext, secret_key)

        assert receiver_secret == sender_secret

from kyber.module_lwe import vector_dot_product
from kyber.poly import sub
from kyber.encoding import encode_message

def test_residual_polynomial_has_correct_length():
    public_key, secret_key = keygen()
    message_bits = [0, 1] * (PARAMS.n // 2)

    ciphertext, _ = encapsulate(public_key, message_bits)
    u, v = ciphertext

    secret_product = vector_dot_product(secret_key, u)
    recovered_poly = sub(v, secret_product)

    assert len(recovered_poly) == PARAMS.n
    assert all(0 <= coefficient < PARAMS.q for coefficient in recovered_poly)

def modular_distance(a, b, q):
    """Return the shortest distance between two residues modulo q."""
    difference = (a - b) % q
    return min(difference, q - difference)

def test_modular_distance():
    assert modular_distance(10, 12, PARAMS.q) == 2
    assert modular_distance(0, PARAMS.q - 1, PARAMS.q) == 1
    assert modular_distance(100, 100, PARAMS.q) == 0

def test_residual_noise_stays_within_decoding_margin():
    public_key, secret_key = keygen()
    message_bits = [0, 1] * (PARAMS.n // 2)

    ciphertext, _ = encapsulate(public_key, message_bits)
    u, v = ciphertext

    secret_product = vector_dot_product(secret_key, u)
    recovered_poly = sub(v, secret_product)
    encoded_message = encode_message(message_bits)

    distances = [
        modular_distance(recovered, encoded, PARAMS.q)
        for recovered, encoded in zip(recovered_poly, encoded_message)
    ]

    print(f"\nResidual coefficient distances: {distances}")
    print(f"Maximum residual distance: {max(distances)}")

    assert max(distances) < PARAMS.q // 4

def test_maximum_residual_distance_over_100_trials():
    random.seed(2026)
    worst_distance = 0
    trials = 100

    for _ in range(trials):
        public_key, secret_key = keygen()
        message_bits = [
            random.randint(0, 1) for _ in range(PARAMS.n)
        ]

        ciphertext, _ = encapsulate(public_key, message_bits)
        u, v = ciphertext

        secret_product = vector_dot_product(secret_key, u)
        recovered_poly = sub(v, secret_product)
        encoded_message = encode_message(message_bits)

        distances = [
            modular_distance(recovered, encoded, PARAMS.q)
            for recovered, encoded in zip(
                recovered_poly, encoded_message
            )
        ]

        worst_distance = max(worst_distance, max(distances))

    print(f"\nWorst residual distance over {trials} trials: {worst_distance}")
    print(f"Decoding boundary: {PARAMS.q // 4}")

    assert worst_distance < PARAMS.q // 4
from kyber.keygen import keygen
from kyber.encapsulation import encapsulate
from kyber.decapsulation import decapsulate


def test_full_encapsulation_decapsulation_flow():
    public_key, secret_key = keygen()

    message = [
        0, 1, 1, 0,
        1, 0, 0, 1,
        1, 1, 0, 0,
        0, 1, 0, 1,
    ]

    ciphertext, sender_secret = encapsulate(public_key, message)
    receiver_secret = decapsulate(ciphertext, secret_key)

    assert len(sender_secret) == 32
    assert len(receiver_secret) == 32
    assert sender_secret == receiver_secret
def test_encapsulation_ciphertext_structure():
    public_key, _ = keygen()

    message = [0, 1] * (N // 2)
    ciphertext, shared_secret = encapsulate(public_key, message)

    u, v = ciphertext

    assert len(u) == 2
    assert all(len(poly) == N for poly in u)
    assert len(v) == N
    assert len(shared_secret) == 32    
@pytest.mark.parametrize(
    "message",
    [
        [0, 1, 2] + [0] * (PARAMS.n - 3),
        [0, -1] + [0] * (PARAMS.n - 2),
        [0, "1"] + [0] * (PARAMS.n - 2),
        [False, True] + [0] * (PARAMS.n - 2),
    ],
)
def test_encapsulate_rejects_invalid_message_bits(message):
    public_key, _ = keygen()

    with pytest.raises(ValueError):
        encapsulate(public_key, message)
@pytest.mark.parametrize(
    "public_key",
    [
        None,
        (),
        ([], []),
        ([[[0] * N]], [[0] * N]),
        (
            [
                [[0] * N, [0] * N],
                [[0] * N, [0] * (N - 1)],
            ],
            [[0] * N, [0] * N],
        ),
        (
            [
                [[0] * N, [0] * N],
                [[0] * N, [0] * N],
            ],
            [[0] * N],
        ),
    ],
)
def test_encapsulate_rejects_malformed_public_key(public_key):
    message = [0, 1] * (N // 2)

    with pytest.raises((ValueError, TypeError)):
        encapsulate(public_key, message) 
def test_encapsulate_rejects_non_sequence_matrix():
    public_key = (None, [[0] * N, [0] * N])
    message = [0, 1] * (N // 2)

    with pytest.raises(ValueError, match="matrix A"):
        encapsulate(public_key, message)


def test_encapsulate_rejects_non_sequence_vector():
    A = [
        [[0] * N, [0] * N],
        [[0] * N, [0] * N],
    ]
    public_key = (A, None)
    message = [0, 1] * (N // 2)

    with pytest.raises(ValueError, match="vector t"):
        encapsulate(public_key, message) 
def test_encapsulate_rejects_public_key_with_wrong_container_type():
    message = [0, 1] * (N // 2)

    with pytest.raises(ValueError, match="Public key"):
        encapsulate(None, message)


def test_encapsulate_rejects_public_key_with_wrong_length():
    message = [0, 1] * (N // 2)

    with pytest.raises(ValueError, match="Public key"):
        encapsulate(([],), message) 
def test_encapsulate_rejects_matrix_row_with_wrong_length():
    A = [
        [[0] * N],  # Only one polynomial; K = 2
        [[0] * N, [0] * N],
    ]
    t = [[0] * N, [0] * N]

    with pytest.raises(ValueError, match="Every row of A"):
        encapsulate((A, t), [0, 1] * (N // 2))


def test_encapsulate_rejects_public_vector_polynomial_with_wrong_length():
    A = [
        [[0] * N, [0] * N],
        [[0] * N, [0] * N],
    ]
    t = [[0] * N, [0] * (N - 1)]

    with pytest.raises(ValueError, match="Every polynomial in t"):
        encapsulate((A, t), [0, 1] * (N // 2))
                                         