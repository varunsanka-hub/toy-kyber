import hashlib

from .encoding import decode_message
from .module_lwe import K, N, vector_dot_product
from .poly import sub


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
            raise ValueError("Every secret-key polynomial must have N coefficients.")

    # Validate ciphertext component u.
    if not isinstance(u, (tuple, list)) or len(u) != K:
        raise ValueError("Ciphertext component u must contain exactly K polynomials.")

    for poly in u:
        if not isinstance(poly, (tuple, list)) or len(poly) != N:
            raise ValueError("Every polynomial in u must have N coefficients.")

    # Validate ciphertext component v.
    if not isinstance(v, (tuple, list)) or len(v) != N:
        raise ValueError("Ciphertext component v must have N coefficients.")

    # Recover the encoded message.
    secret_product = vector_dot_product(secret_key, u)
    recovered_poly = sub(v, secret_product)
    recovered_bits = decode_message(recovered_poly)

    # Educational toy derivation; not standardized ML-KEM.
    shared_secret = hashlib.sha256(bytes(recovered_bits)).digest()

    return shared_secret
