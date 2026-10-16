
"""
Measure observed message-recovery reliability in the toy scheme.
"""

import secrets

from kyber.keygen import keygen
from kyber.encapsulation import encapsulate
from kyber.decapsulation import decapsulate
from kyber.params import PARAMS


def run_experiment(trials=1000):
    if not isinstance(trials, int) or isinstance(trials, bool) or trials < 1:
        raise ValueError("trials must be a positive integer.")

    public_key, secret_key = keygen()

    successful = 0
    failed = 0

    for _ in range(trials):
        message = [
            secrets.randbelow(2)
            for _ in range(PARAMS.n)
        ]

        ciphertext, sender_secret = encapsulate(public_key, message)
        receiver_secret = decapsulate(ciphertext, secret_key)

        if sender_secret == receiver_secret:
            successful += 1
        else:
            failed += 1

    rate = 100 * successful / trials

    print("Toy message-recovery reliability experiment")
    print(f"Trials: {trials}")
    print(f"Polynomial modulus q: {PARAMS.q}")
    print(f"Polynomial length N: {PARAMS.n}")
    print(f"Successful recoveries: {successful}")
    print(f"Failed recoveries: {failed}")
    print(f"Observed success rate: {rate:.2f}%")

    return successful, failed


if __name__ == "__main__":
    run_experiment()
