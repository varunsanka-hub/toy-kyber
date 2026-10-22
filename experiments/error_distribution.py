
import secrets
from collections import Counter

from kyber.encapsulation import encapsulate
from kyber.encoding import decode_message, encode_message
from kyber.keygen import keygen
from kyber.module_lwe import vector_dot_product
from kyber.params import PARAMS
from kyber.poly import sub

Q = PARAMS.q
N = PARAMS.n


def centered_coefficients(poly):
    """Convert residues modulo Q to centered integer representatives."""
    return [
        coefficient if coefficient <= Q // 2 else coefficient - Q
        for coefficient in poly
    ]


def run_experiment(trials=1000):
    if not isinstance(trials, int) or isinstance(trials, bool) or trials < 1:
        raise ValueError("trials must be a positive integer.")

    public_key, secret_key = keygen()

    absolute_errors = []
    error_counts = Counter()
    failures = 0

    for _ in range(trials):
        message = [secrets.randbelow(2) for _ in range(N)]
        ciphertext, _ = encapsulate(public_key, message)
        u, v = ciphertext

        # Reproduce the polynomial calculated during decapsulation.
        secret_product = vector_dot_product(secret_key, u)
        recovered_poly = sub(v, secret_product)

        # Calculate the error relative to the encoded message.
        message_poly = encode_message(message)
        error_poly = sub(recovered_poly, message_poly)
        signed_errors = centered_coefficients(error_poly)

        # Store absolute magnitudes across all coefficients and trials.
        for error in signed_errors:
            magnitude = abs(error)
            absolute_errors.append(magnitude)
            error_counts[magnitude] += 1

        if decode_message(recovered_poly) != message:
            failures += 1

    total_coefficients = len(absolute_errors)

    print("Toy Kyber error-distribution experiment")
    print(f"Modulus q: {Q}")
    print(f"Polynomial degree: {N}")
    print(f"Trials: {trials}")
    print(f"Error coefficients measured: {total_coefficients}")
    print(f"Mean absolute error: {sum(absolute_errors) / total_coefficients:.3f}")
    print(f"Maximum absolute error: {max(absolute_errors)}")
    print(f"Message recovery failures: {failures}")
    print(f"Observed recovery success rate: {100 * (trials - failures) / trials:.2f}%")

    print("\nError magnitude frequency (top 15):")
    for magnitude, count in sorted(
        error_counts.items(),
        key=lambda item: (-item[1], item[0])
    )[:15]:
        print(f"|error| = {magnitude:>3}: {count:>6} ({100 * count / total_coefficients:.2f}%)")

    return {
        "trials": trials,
        "mean_absolute_error": sum(absolute_errors) / total_coefficients,
        "maximum_absolute_error": max(absolute_errors),
        "failures": failures,
        "error_counts": error_counts,
    }


if __name__ == "__main__":
    run_experiment()
