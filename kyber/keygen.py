"""
Educational toy ML-KEM-style key generation.

This is NOT a secure implementation of ML-KEM.

It demonstrates the relationship:

    t = A*s + e

Public key:
    (A, t)

Secret key:
    s
"""

from .module_lwe import module_lwe_sample


def keygen():
    """
    Generate a toy public/private key pair.
    """
    A, s, e, t = module_lwe_sample()

    public_key = (A, t)
    secret_key = s

    return public_key, secret_key