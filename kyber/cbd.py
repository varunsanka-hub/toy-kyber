"""
Centered Binomial Distribution sampler
for the educational toy ML-KEM implementation.
"""

import random

from .params import PARAMS


N = PARAMS.n


def cbd_coefficient(eta=2):
    """
    Generate one coefficient from a centered
    binomial distribution.

    For eta = 2:

        X = (a1 + a2) - (b1 + b2)

    where all ai and bi are random bits.
    """

    a = sum(random.randint(0, 1) for _ in range(eta))
    b = sum(random.randint(0, 1) for _ in range(eta))

    return a - b


def cbd_poly(eta=2):
    """
    Generate a polynomial whose coefficients
    are sampled independently from the CBD.
    """

    return [
        cbd_coefficient(eta)
        for _ in range(N)
    ]