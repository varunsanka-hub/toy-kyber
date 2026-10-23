import hashlib

from .encoding import decode_message
from .module_lwe import K, N, vector_dot_product
from .params import PARAMS
from .poly import sub


Q = PARAMS.q


def _validate_coefficients(poly, name, centered=False):
    """Validate polynomial coefficient types and ranges."""

    for coefficient in poly:
        if (
            not isinstance(coefficient, int)
            or isinstance(coefficient, bool)
        ):
            raise ValueError(
                f"{name} coefficients must be integers."
            )

        if centered:
            valid = -(Q // 2) <= coefficient <= Q // 2
        else:
            valid = 0 <= coefficient < Q

        if not valid:
            raise ValueError(
                f"{name} contains an out-of-range coefficient."
            )


def decapsulate(ciphertext, secret_key):
    """
    Recover the message and derive the toy shared secret.

    Ciphertext:
        (u, v)

    Secret key:
        Vector of K polynomials.
    """

    # Validate the ciphertext container.
    if not isinstance(ciphertext, (tuple, list)) or len(ciphertext) != 2:
        raise ValueError("Ciphertext must contain exactly (u, v).")

    u, v = ciphertext

    # Validate the secret-key vector.
    if not isinstance(secret_key, (tuple, list)) or len(secret_key) != K:
        raise ValueError("Secret key must contain exactly K polynomials.")

    for poly in secret_key:
        if not isinstance(poly, (tuple, list)) or len(poly) != N:
            raise ValueError(
                "Every secret-key polynomial must have N coefficients."
            )

    # Validate ciphertext component u.
    if not isinstance(u, (tuple, list)) or len(u) != K:
        raise ValueError(
            "Ciphertext component u must contain exactly K polynomials."
        )

    for poly in u:
        if not isinstance(poly, (tuple, list)) or len(poly) != N:
            raise ValueError(
                "Every polynomial in u must have N coefficients."
            )

    # Validate ciphertext component v.
    if not isinstance(v, (tuple, list)) or len(v) != N:
        raise ValueError(
            "Ciphertext component v must have N coefficients."
        )

    # Validate coefficient types and ranges BEFORE polynomial arithmetic.
    for i, poly in enumerate(secret_key):
        _validate_coefficients(
            poly, f"secret_key[{i}]", centered=True
        )

    for i, poly in enumerate(u):
        _validate_coefficients(poly, f"u[{i}]")

    _validate_coefficients(v, "v")

    # Recover the encoded message.
    secret_product = vector_dot_product(secret_key, u)
    recovered_poly = sub(v, secret_product)
    recovered_bits = decode_message(recovered_poly)

    # Educational toy derivation; not standardized ML-KEM.
    shared_secret = hashlib.sha256(bytes(recovered_bits)).digest()

    return shared_secret
