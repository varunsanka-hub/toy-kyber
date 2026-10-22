
"""
Centered Binomial Distribution sampler
for the educational toy ML-KEM implementation.
"""

import secrets

from .params import PARAMS


N = PARAMS.n


def cbd_coefficient(eta=2, rng=None):
    """
    Generate one coefficient from a centered binomial
    distribution using independent random bits.

    By default, use cryptographic randomness.
    An optional RNG supports reproducible diagnostics.
    """
    if not isinstance(eta, int) or isinstance(eta, bool) or eta < 1:
        raise ValueError("eta must be a positive integer.")

    if rng is None:
        randbit = lambda: secrets.randbits(1)
    else:
        randbit = lambda: rng.getrandbits(1)

    a = sum(randbit() for _ in range(eta))
    b = sum(randbit() for _ in range(eta))

    return a - b


def cbd_poly(eta=2, rng=None):
    """Generate a polynomial with independently sampled CBD coefficients."""
    return [
        cbd_coefficient(eta, rng=rng)
        for _ in range(N)
    ]
