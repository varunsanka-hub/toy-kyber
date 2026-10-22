
"""Verify the three contributions to the toy decryption error."""

import secrets

from kyber.cbd import cbd_poly
from kyber.encoding import decode_message, encode_message
from kyber.module_lwe import (
    module_lwe_sample,
    random_poly_vector,
    encapsulation_u,
    encapsulation_v,
    vector_dot_product,
)
from kyber.params import PARAMS
from kyber.poly import add, sub

Q = PARAMS.q
N = PARAMS.n


def centered(poly):
    """Represent modular coefficients as signed integers."""
    return [
        x if x <= Q // 2 else x - Q
        for x in poly
    ]


def max_abs(poly):
    return max(abs(x) for x in centered(poly))


def run_experiment(trials=1000):
    if not isinstance(trials, int) or isinstance(trials, bool) or trials < 1:
        raise ValueError("trials must be a positive integer.")

    mismatches = 0
    recovery_failures = 0
    largest_error = 0
    largest_contribution = 0

    for trial in range(trials):
        # Keep the key-generation error vector e for this experiment.
        A, s, e, t = module_lwe_sample()

        # Fresh encapsulation randomness.
        r = random_poly_vector()
        e1 = random_poly_vector()
        e2 = cbd_poly()

        message = [secrets.randbelow(2) for _ in range(N)]
        message_poly = encode_message(message)

        # Recreate the ciphertext using the existing helpers.
        u = encapsulation_u(A, r, e1)
        v = encapsulation_v(t, r, e2, message_poly)

        # Actual error obtained from the decapsulation equation.
        actual_recovered_poly = sub(v, vector_dot_product(s, u))
        actual_error = sub(actual_recovered_poly, message_poly)

        # Theoretical contributions:
        # delta = e^T*r + e2 - s^T*e1 (mod q).
        key_error_term = vector_dot_product(e, r)
        encapsulation_error_term = e2
        secret_error_term = vector_dot_product(s, e1)

        predicted_error = add(key_error_term, encapsulation_error_term)
        predicted_error = sub(predicted_error, secret_error_term)

        if actual_error != predicted_error:
            mismatches += 1

        if decode_message(actual_recovered_poly) != message:
            recovery_failures += 1

        largest_error = max(largest_error, max_abs(actual_error))

        largest_contribution = max(
            largest_contribution,
            max_abs(key_error_term),
            max_abs(encapsulation_error_term),
            max_abs(secret_error_term),
        )

        if trial == 0:
            example = (
                key_error_term,
                encapsulation_error_term,
                secret_error_term,
                actual_error,
                predicted_error,
            )

    print("Toy Kyber error-contribution experiment")
    print(f"q: {Q}, N: {N}")
    print(f"Trials: {trials}")
    print(f"Error-equation mismatches: {mismatches}")
    print(f"Message recovery failures: {recovery_failures}")
    print(f"Largest observed combined error: {largest_error}")
    print(f"Largest observed individual contribution: {largest_contribution}")

    print("\nFirst-trial example (centered coefficients)")
    labels = [
        "e^T * r",
        "e2",
        "s^T * e1",
        "Actual combined error",
        "Predicted combined error",
    ]

    for label, poly in zip(labels, example):
        print(f"{label}: {centered(poly)}")

    return mismatches, recovery_failures


if __name__ == "__main__":
    run_experiment()
