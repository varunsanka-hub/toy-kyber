
"""
Educational toy encapsulation.

This is not standardized or production-secure ML-KEM.
"""

import hashlib

from .cbd import cbd_poly
from .encoding import encode_message
from .module_lwe import (
    encapsulation_u,
    encapsulation_v,
    random_poly_vector,
)


def encapsulate(public_key, message_bits):
    """
    Create a toy ciphertext and shared secret.

    Returns:
        ciphertext: (u, v)
        shared_secret: 32-byte digest
    """
    A, t = public_key

    # Fresh small random values for this encapsulation.
    r = random_poly_vector()
    e1 = random_poly_vector()
    e2 = cbd_poly()

    # Encode the message as a polynomial.
    message_poly = encode_message(message_bits)

    # Construct the ciphertext.
    u = encapsulation_u(A, r, e1)
    v = encapsulation_v(t, r, e2, message_poly)

    # Toy shared-secret derivation.
    shared_secret = hashlib.sha256(bytes(message_bits)).digest()

    ciphertext = (u, v)
    return ciphertext, shared_secret
