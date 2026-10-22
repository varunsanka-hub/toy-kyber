
import random

from kyber.keygen import keygen
from kyber.encapsulation import encapsulate
from kyber.params import PARAMS


def test_seeded_encapsulation_is_reproducible():
    public_key, _ = keygen(rng=random.Random(100))
    message = [i % 2 for i in range(PARAMS.n)]

    ciphertext1, secret1 = encapsulate(
        public_key, message, rng=random.Random(200)
    )
    ciphertext2, secret2 = encapsulate(
        public_key, message, rng=random.Random(200)
    )

    assert ciphertext1 == ciphertext2
    assert secret1 == secret2


def test_seeded_encapsulation_recovers_message():
    public_key, secret_key = keygen(rng=random.Random(100))
    message = [i % 2 for i in range(PARAMS.n)]

    ciphertext, sender_secret = encapsulate(
        public_key, message, rng=random.Random(200)
    )

    from kyber.decapsulation import decapsulate
    from kyber.module_lwe import vector_dot_product
    from kyber.poly import sub
    from kyber.encoding import decode_message

    receiver_secret = decapsulate(ciphertext, secret_key)

    u, v = ciphertext
    recovered_poly = sub(v, vector_dot_product(secret_key, u))
    recovered_message = decode_message(recovered_poly)

    assert recovered_message == message
    assert receiver_secret == sender_secret
