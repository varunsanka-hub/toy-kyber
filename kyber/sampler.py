
"""
Random polynomial sampling for the educational
toy ML-KEM implementation.
"""

import secrets

from .params import PARAMS


N = PARAMS.n
Q = PARAMS.q


def uniform_coefficient(rng=None):
    """Generate one coefficient in Z_q.

    By default, use cryptographic randomness.
    An optional RNG can be supplied for reproducible diagnostics.
    """
    if rng is None:
        return secrets.randbelow(Q)

    return rng.randrange(Q)


def uniform_poly(rng=None):
    """Generate a polynomial with N coefficients in Z_q."""
    return [
        uniform_coefficient(rng)
        for _ in range(N)
    ]
