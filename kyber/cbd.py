"""
Centered Binomial Distribution sampler
for the educational toy ML-KEM implementation.
"""

import random


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