import random

from kyber.keygen import keygen
from kyber.encapsulation import encapsulate
from kyber.params import PARAMS


def run_experiment(trials=100, key_seed=42, encapsulation_seed=123):
    if not isinstance(trials, int) or isinstance(trials, bool) or trials < 1:
        raise ValueError("trials must be a positive integer.")

    # Identical key seeds should produce identical key pairs.
    public_key_1, secret_key_1 = keygen(rng=random.Random(key_seed))
    public_key_2, secret_key_2 = keygen(rng=random.Random(key_seed))

    key_reproducible = (
        public_key_1 == public_key_2
        and secret_key_1 == secret_key_2
    )

    message = [i % 2 for i in range(PARAMS.n)]

    # Identical encapsulation seeds should produce identical outputs.
    ciphertext_1, shared_secret_1 = encapsulate(
        public_key_1,
        message,
        rng=random.Random(encapsulation_seed),
    )
    ciphertext_2, shared_secret_2 = encapsulate(
        public_key_1,
        message,
        rng=random.Random(encapsulation_seed),
    )

    encapsulation_reproducible = (
        ciphertext_1 == ciphertext_2
        and shared_secret_1 == shared_secret_2
    )

    # Check reproducibility over several independent seed pairs.
    reproducible_pairs = 0

    for i in range(trials):
        seed = key_seed + i
        pk1, sk1 = keygen(rng=random.Random(seed))
        pk2, sk2 = keygen(rng=random.Random(seed))

        if pk1 == pk2 and sk1 == sk2:
            reproducible_pairs += 1

    print("Toy-Kyber reproducibility report")
    print(f"Trials: {trials}")
    print(f"Key seed: {key_seed}")
    print(f"Encapsulation seed: {encapsulation_seed}")
    print(f"Polynomial modulus q: {PARAMS.q}")
    print(f"Polynomial length N: {PARAMS.n}")
    print(f"Key generation reproducible: {key_reproducible}")
    print(f"Encapsulation reproducible: {encapsulation_reproducible}")
    print(f"Reproducible key pairs: {reproducible_pairs}/{trials}")

    return {
        "key_reproducible": key_reproducible,
        "encapsulation_reproducible": encapsulation_reproducible,
        "reproducible_pairs": reproducible_pairs,
        "trials": trials,
    }


if __name__ == "__main__":
    run_experiment()
