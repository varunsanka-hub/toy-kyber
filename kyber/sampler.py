
"""
Random polynomial sampling for the educational
toy ML-KEM implementation.
"""

import secrets

from .params import PARAMS


N = PARAMS.n
Q = PARAMS.q


def uniform_coefficient():
    """Generate one uniformly random coefficient in Z_q."""
    return secrets.randbelow(Q)


def uniform_poly():
    """Generate a polynomial with N coefficients in Z_q."""
    return [
        uniform_coefficient()
        for _ in range(N)
    ]
