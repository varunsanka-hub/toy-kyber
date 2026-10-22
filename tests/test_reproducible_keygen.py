
import random

from kyber.keygen import keygen


def test_seeded_keygen_is_reproducible():
    public_key_1, secret_key_1 = keygen(rng=random.Random(42))
    public_key_2, secret_key_2 = keygen(rng=random.Random(42))

    assert public_key_1 == public_key_2
    assert secret_key_1 == secret_key_2


def test_different_seeds_produce_different_keys():
    public_key_1, secret_key_1 = keygen(rng=random.Random(42))
    public_key_2, secret_key_2 = keygen(rng=random.Random(43))

    assert (public_key_1, secret_key_1) != (public_key_2, secret_key_2)


def test_default_keygen_still_works():
    public_key, secret_key = keygen()

    assert len(public_key) == 2
    assert len(secret_key) == 2
