
"""
Measure observed message-recovery reliability in the educational toy scheme.

This is an empirical experiment, not a proof of security or correctness.
"""

import secrets

from kyber.keygen import keygen
from kyber.encapsulation import encapsulate
from kyber.decapsulation import decapsulate
from kyber.encoding import decode_message
from kyber.params import PARAMS


def run_experiment(trials=1000):
    if not isinstance(trials, int) or isinstance(trials, bool) or trials < 1:
        raise ValueError("trials must be a positive integer.")

    public_key, secret_key = keygen()

    secret_matches = 0
    message_matches = 0
    secret_failures = 0
    message_failures = 0

    for _ in range(trials):
        message = [
            secrets.randbelow(2)
            for _ in range(PARAMS.n)
        ]

        ciphertext, sender_secret = encapsulate(public_key, message)
        receiver_secret = decapsulate(ciphertext, secret_key)

        if sender_secret == receiver_secret:
            secret_matches += 1
        else:
            secret_failures += 1

        # In this toy construction, ciphertext is (u, v).
        u, v = ciphertext
        from kyber.module_lwe import vector_dot_product
        from kyber.poly import sub

        recovered_poly = sub(v, vector_dot_product(secret_key, u))
        recovered_message = decode_message(recovered_poly)

        if recovered_message == message:
            message_matches += 1
        else:
            message_failures += 1

    print("Toy-Kyber reliability experiment")
    print(f"Trials: {trials}")
    print(f"Polynomial modulus q: {PARAMS.q}")
    print(f"Polynomial length N: {PARAMS.n}")
    print(f"Shared-secret matches: {secret_matches}")
    print(f"Shared-secret failures: {secret_failures}")
    print(f"Message recoveries: {message_matches}")
    print(f"Message-recovery failures: {message_failures}")
    print(f"Shared-secret agreement rate: {100 * secret_matches / trials:.2f}%")
    print(f"Message-recovery rate: {100 * message_matches / trials:.2f}%")

    return {
        "trials": trials,
        "secret_matches": secret_matches,
        "secret_failures": secret_failures,
        "message_matches": message_matches,
        "message_failures": message_failures,
    }


if __name__ == "__main__":
    run_experiment()
