"""
Educational Ring-LWE sample generation.

This is NOT a secure implementation of ML-KEM.
It is only used to understand the mathematics.

Ring:
    R_q = Z_q[X] / (X^N + 1)

Equation:
    b = a * s + e
"""

from .sampler import uniform_poly
from .cbd import cbd_poly
from .poly import add, schoolbook_mul


def ring_lwe_sample():
    """
    Generate one toy Ring-LWE sample.

    Equation:

        b = a * s + e

    where:

        a = uniformly random polynomial
        s = small secret polynomial
        e = small error polynomial
    """

    a = uniform_poly()
    s = cbd_poly()
    e = cbd_poly()

    a_times_s = schoolbook_mul(a, s)

    b = add(a_times_s, e)

    return a, s, e, b