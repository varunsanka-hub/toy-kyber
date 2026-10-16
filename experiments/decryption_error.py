
"""Measure the decryption error in the educational toy ML-KEM."""

import secrets

from kyber.encapsulation import encapsulate
from kyber.encoding import decode_message, encode_message
from kyber.keygen import keygen
from kyber.module_lwe import vector_dot_product
from kyber.params import PARAMS
from kyber.poly import sub


Q = PARAMS.q
N = PARAMS.n


def centered_coefficients(poly):
    """Represent coefficients in the interval centered around zero."""
    return [
        coefficient if coefficient <= Q // 2 else coefficient - Q
        for coefficient in poly
    ]


def run_experiment(trials=1000):
    if not isinstance(trials, int) or isinstance(trials, bool) or trials < 1:
        raise ValueError("trials must be a positive integer.")

    public_key, secret_key = keygen()

    total_failures = 0
    largest_error_seen = 0
    example = None

    for trial in range(trials):
        message = [secrets.randbelow(2) for _ in range(N)]

        ciphertext, _ = encapsulate(public_key, message)
        u, v = ciphertext

        # Compute the polynomial recovered before message decoding.
        secret_product = vector_dot_product(secret_key, u)
        recovered_poly = sub(v, secret_product)

        # delta = recovered polynomial - encoded message (mod q).
        message_poly = encode_message(message)
        error_poly = sub(recovered_poly, message_poly)
        signed_error = centered_coefficients(error_poly)

        recovered_message = decode_message(recovered_poly)
        success = recovered_message == message

        if not success:
            total_failures += 1

        max_error = max(abs(x) for x in signed_error)
        largest_error_seen = max(largest_error_seen, max_error)

        if trial == 0:
            example = (
                message,
                signed_error,
                recovered_message,
                max_error,
            )

    print("Toy decryption-error experiment")
    print(f"q: {Q}, N: {N}")
    print(f"Trials: {trials}")
    print(f"Successful message recoveries: {trials - total_failures}")
    print(f"Failed message recoveries: {total_failures}")
    print(f"Observed success rate: {100 * (trials - total_failures) / trials:.2f}%")
    print(f"Largest absolute error coefficient observed: {largest_error_seen}")

    if example is not None:
        message, signed_error, recovered_message, max_error = example

        print("\nFirst-trial details")
        print(f"Original message: {message}")
        print(f"Recovered message: {recovered_message}")
        print(f"Signed error coefficients: {signed_error}")
        print(f"Maximum absolute error: {max_error}")
        print(f"Message recovered exactly: {message == recovered_message}")


if __name__ == "__main__":
    run_experiment()
