import random

from kyber.keygen import keygen
from kyber.encapsulation import encapsulate
from kyber.decapsulation import decapsulate
from kyber.encoding import decode_message
from kyber.module_lwe import vector_dot_product
from kyber.poly import sub
from kyber.params import PARAMS


def run_experiment(trials=1000, seed=20261022):
    if not isinstance(trials, int) or isinstance(trials, bool) or trials < 1:
        raise ValueError("trials must be a positive integer.")

    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("seed must be an integer.")

    rng = random.Random(seed)

    public_key, secret_key = keygen()

    secret_matches = 0
    message_matches = 0

    for _ in range(trials):
        message = [
            rng.randrange(2)
            for _ in range(PARAMS.n)
        ]

        ciphertext, sender_secret = encapsulate(public_key, message)
        receiver_secret = decapsulate(ciphertext, secret_key)

        if sender_secret == receiver_secret:
            secret_matches += 1

        u, v = ciphertext
        recovered_poly = sub(v, vector_dot_product(secret_key, u))
        recovered_message = decode_message(recovered_poly)

        if recovered_message == message:
            message_matches += 1

    print("Toy-Kyber seeded-input diagnostic")
    print(f"Trials: {trials}")
    print(f"Message-input seed: {seed}")
    print(f"Modulus q: {PARAMS.q}")
    print(f"Polynomial length N: {PARAMS.n}")
    print(f"Shared-secret matches: {secret_matches}/{trials}")
    print(f"Message recoveries: {message_matches}/{trials}")
    print(f"Observed message-recovery rate: "
          f"{100 * message_matches / trials:.2f}%")
    print()
    print("Note: message inputs are seeded; cryptographic randomness")
    print("from key generation and encapsulation is not seeded.")

    return {
        "trials": trials,
        "seed": seed,
        "secret_matches": secret_matches,
        "message_matches": message_matches,
    }


if __name__ == "__main__":
    run_experiment()
