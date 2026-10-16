
"""
Centered Binomial Distribution sampler
for the educational toy ML-KEM implementation.
"""

import secrets

from .params import PARAMS


N = PARAMS.n


def cbd_coefficient(eta=2):
    """
    Generate one coefficient from a centered binomial
    distribution using independent random bits.
    """
    if not isinstance(eta, int) or isinstance(eta, bool) or eta < 1:
        raise ValueError("eta must be a positive integer.")

    a = sum(secrets.randbits(1) for _ in range(eta))
    b = sum(secrets.randbits(1) for _ in range(eta))

    return a - b


def cbd_poly(eta=2):
    """Generate a polynomial with independently sampled CBD coefficients."""
    return [
        cbd_coefficient(eta)
        for _ in range(N)
    ]
