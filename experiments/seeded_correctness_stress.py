import random

from kyber.keygen import keygen
from kyber.encapsulation import encapsulate
from kyber.decapsulation import decapsulate
from kyber.encoding import decode_message
from kyber.module_lwe import vector_dot_product
from kyber.poly import sub
from kyber.params import PARAMS


def run_experiment(
    trials=1000,
    key_seed=1000,
    message_seed=2000,
    encapsulation_seed=3000,
):
    """Test message recovery and shared-secret agreement."""

    for name, value in (
        ("trials", trials),
        ("key_seed", key_seed),
        ("message_seed", message_seed),
        ("encapsulation_seed", encapsulation_seed),
    ):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{name} must be an integer.")

    if trials < 1:
        raise ValueError("trials must be a positive integer.")

    message_matches = 0
    secret_matches = 0
    failures = []

    for i in range(trials):
        # Each trial gets its own deterministic RNG streams.
        public_key, secret_key = keygen(
            rng=random.Random(key_seed + i)
        )

        message_rng = random.Random(message_seed + i)
        message = [
            message_rng.randrange(2)
            for _ in range(PARAMS.n)
        ]

        ciphertext, sender_secret = encapsulate(
            public_key,
            message,
            rng=random.Random(encapsulation_seed + i),
        )

        receiver_secret = decapsulate(ciphertext, secret_key)

        u, v = ciphertext
        recovered_poly = sub(
            v,
            vector_dot_product(secret_key, u),
        )
        recovered_message = decode_message(recovered_poly)

        message_ok = recovered_message == message
        secret_ok = receiver_secret == sender_secret

        if message_ok:
            message_matches += 1

        if secret_ok:
            secret_matches += 1

        if not message_ok or not secret_ok:
            failures.append({
                "trial": i,
                "message_recovered": message_ok,
                "shared_secret_matches": secret_ok,
            })

    print("Toy-Kyber seeded correctness stress test")
    print(f"Trials: {trials}")
    print(f"Key seed base: {key_seed}")
    print(f"Message seed base: {message_seed}")
    print(f"Encapsulation seed base: {encapsulation_seed}")
    print(f"Message recoveries: {message_matches}/{trials}")
    print(f"Shared-secret agreements: {secret_matches}/{trials}")
    print(f"Failures: {len(failures)}")

    if failures:
        print("First failures:")
        for failure in failures[:10]:
            print(failure)

    return {
        "trials": trials,
        "message_matches": message_matches,
        "secret_matches": secret_matches,
        "failures": failures,
    }


if __name__ == "__main__":
    run_experiment()
