
"""
Educational toy decapsulation.

This is not standardized or production-secure ML-KEM.
"""

import hashlib

from .encoding import decode_message
from .module_lwe import vector_dot_product
from .poly import sub


def decapsulate(ciphertext, secret_key):
    """
    Recover the toy message and derive its shared secret.

    Returns:
        shared_secret: 32-byte digest
    """
    u, v = ciphertext

    # Compute s^T * u.
    secret_product = vector_dot_product(secret_key, u)

    # Remove the secret-dependent term from v.
    recovered_poly = sub(v, secret_product)

    # Decode the noisy polynomial.
    recovered_bits = decode_message(recovered_poly)

    # Match the toy derivation used by encapsulation.
    shared_secret = hashlib.sha256(
        bytes(recovered_bits)
    ).digest()

    return shared_secret
